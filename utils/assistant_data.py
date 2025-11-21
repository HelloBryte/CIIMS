"""
Utility helpers that implement the SQL-agent workflow for the CIIMS AI assistant.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple

from utils.database_helper import execute_query
from utils.logging_config import get_logger

logger = get_logger(__name__)

SENSITIVE_KEYWORDS = {"password", "passcode", "credential"}
SQL_BLOCKLIST = ["DELETE", "UPDATE", "INSERT", "DROP", "ALTER", "TRUNCATE"]
PLACEHOLDERS = ["{{CURRENT_USER_ID}}", "{{CURRENT_USER_NAME}}"]

SCHEMA_DEFINITION: Dict[str, Dict[str, Any]] = {
    "items": {
        "columns": ["item_id", "item_name", "item_category", "item_quantity", "remark"],
        "description": "Inventory catalog",
    },
    "borrows": {
        "columns": [
            "borrow_id",
            "item_id",
            "user_id",
            "borrow_time",
            "return_deadline",
            "return_time",
            "return_status",
        ],
        "description": "Borrow transactions between users and items",
    },
    "users": {
        "columns": ["user_id", "user_name", "user_role", "user_phone"],
        "description": "User directory with roles and phone numbers",
    },
}

ROLE_ACCESS: Dict[str, List[str]] = {
    "admin": ["items", "borrows", "users"],
    "user": ["items", "borrows"],
}


def evaluate_prompt(prompt: str, user_role: str) -> Dict[str, Any]:
    """
    Lightweight guardrails for experimental builds.
    Currently we don't block any requests, just return a pass-through flag.
    """
    # For this experimental desktop build we keep checks minimal.
    return {"blocked": False}


def build_runtime_context(user_role: str, user_name: str) -> str:
    """
    Generate schema + instruction text that teaches the model how to behave like a SQL agent.
    """
    allowed_tables = ROLE_ACCESS.get(user_role, ROLE_ACCESS["user"])
    schema_lines: List[str] = []
    for table in allowed_tables:
        meta = SCHEMA_DEFINITION[table]
        schema_lines.append(
            f"- {table}({', '.join(meta['columns'])}): {meta['description']}"
        )

    schema_text = "\n".join(schema_lines)
    instructions = f"""
You are CIIMS-Sherlock, a read-only SQL planner. Always respond with JSON.

Required JSON keys:
  - "intent": short sentence describing the goal (in English).
  - "proposed_sql": SQL string (SELECT only) or "" if no query is required.
  - "explanation": brief rationale (in English).
  - "answer": optional natural-language reply when you already have enough info (MUST be in user's language - 用用户提问的语言回复).

IMPORTANT: Always respond in the same language as the user's question for the "answer" field. 
If user asks in Chinese, provide Chinese answer. If user asks in English, provide English answer.
JSON keys and SQL must remain in English.

If you produce SQL:
  1. Only use SELECT statements against the tables you are allowed to read.
  2. Never include destructive keywords (DELETE/UPDATE/INSERT/etc.).
  3. When referencing the signed-in user, inject placeholders {PLACEHOLDERS}.
     Example: WHERE user_id = {{CURRENT_USER_ID}}
  4. Keep LIMIT <= 50 to avoid giant result sets.
  5. Use fuzzy search for semantic matching:
     - For "books", "reading", "study materials": use LIKE '%book%' OR item_category IN ('books', 'textbooks', 'reference')
     - For "laptop", "computer": use LIKE '%laptop%' OR LIKE '%computer%' OR item_category IN ('electronics', 'computers')
     - For "camera", "photo": use LIKE '%camera%' OR item_category IN ('electronics', 'photography')
     - For "lab equipment", "research": use LIKE '%lab%' OR item_category IN ('equipment', 'tools')
     - Always search both item_name and item_category columns with OR conditions
     - Use LOWER() function for case-insensitive matching

Fuzzy search examples:
- "I want to borrow books" → WHERE LOWER(item_name) LIKE '%book%' OR LOWER(item_category) LIKE '%book%'
- "Need a laptop for class" → WHERE LOWER(item_name) LIKE '%laptop%' OR LOWER(item_category) IN ('electronics', 'computers')
- "Looking for camera equipment" → WHERE LOWER(item_name) LIKE '%camera%' OR LOWER(item_category) LIKE '%photo%'

Signed-in user -> name: {user_name}, role: {user_role}.
Accessible tables:
{schema_text}
"""
    return instructions.strip()


def extract_sql_payload(text: str) -> Dict[str, Any]:
    """
    Attempt to parse the JSON object returned by the model.
    """
    if not text:
        return {}

    candidate = text.strip()

    # Handle fenced code blocks
    fence_match = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```", candidate, re.DOTALL | re.IGNORECASE
    )
    if fence_match:
        candidate = fence_match.group(1)

    if candidate.count("{") > 1:
        start = candidate.find("{")
        end = candidate.rfind("}")
        candidate = candidate[start : end + 1]

    try:
        payload = json.loads(candidate)
        if isinstance(payload, dict):
            return payload
    except json.JSONDecodeError:
        logger.debug("Failed to decode assistant JSON payload: %s", candidate)
    return {}


def validate_sql(sql: str, user_role: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that SQL is read-only and scoped to permitted tables.
    """
    if not sql:
        return False, "Empty SQL string"

    statement = sql.strip().rstrip(";")
    upper_stmt = statement.upper()

    if not upper_stmt.startswith("SELECT"):
        return False, "Only SELECT statements are allowed"

    for keyword in SQL_BLOCKLIST:
        if keyword in upper_stmt:
            return False, f"Keyword '{keyword}' is not allowed"

    tables = _extract_tables(statement)
    allowed = set(ROLE_ACCESS.get(user_role, ROLE_ACCESS["user"]))
    if not tables.issubset(allowed):
        forbidden = ", ".join(sorted(tables - allowed))
        return False, f"Forbidden table(s): {forbidden}"

    if " LIMIT " not in upper_stmt and not upper_stmt.endswith("LIMIT"):
        # Encourage bounded queries; append limit if missing
        statement = f"{statement} LIMIT 50"

    return True, statement


def execute_safe_sql(sql: str, user_role: str, user_name: str) -> List[Dict[str, Any]]:
    """
    Replace placeholders, run the query, and return dictionary rows.
    """
    ok, message = validate_sql(sql, user_role)
    if not ok:
        raise ValueError(message or "Invalid SQL")

    prepared_sql = message  # message holds normalized statement when ok is True
    placeholder_values = _resolve_placeholders(user_name)

    for key, value in placeholder_values.items():
        prepared_sql = prepared_sql.replace(key, value)

    rows = execute_query(prepared_sql, dictionary=True)
    return rows or []


def build_result_system_message(sql: str, rows: List[Dict[str, Any]]) -> str:
    """
    Convert query results into a compact system message that can be fed back to the model.
    """
    preview_rows = rows[:10]
    if not preview_rows:
        return f"SQL query executed: {sql}\nResult: no rows returned."

    headers = list(preview_rows[0].keys())
    lines = [" | ".join(headers)]
    for row in preview_rows:
        line = " | ".join(str(row.get(col, "")) for col in headers)
        lines.append(line)

    more = ""
    if len(rows) > len(preview_rows):
        more = f"\n... truncated {len(rows) - len(preview_rows)} additional row(s)."

    table_text = "\n".join(lines)
    return f"SQL query executed: {sql}\nRows:\n{table_text}{more}"


def _extract_tables(sql: str) -> set:
    pattern = re.compile(
        r"\bFROM\s+([a-z_][a-z0-9_]*)|\bJOIN\s+([a-z_][a-z0-9_]*)", re.IGNORECASE
    )
    matches = pattern.findall(sql)
    tables = set()
    for left, right in matches:
        table = left or right
        if table:
            tables.add(table.lower())
    return tables


def _resolve_placeholders(user_name: str) -> Dict[str, str]:
    mapping = {"{{CURRENT_USER_NAME}}": user_name}
    user_id = _lookup_user_id(user_name)
    mapping["{{CURRENT_USER_ID}}"] = str(user_id or -1)
    return mapping


def _lookup_user_id(user_name: str) -> Optional[int]:
    try:
        rows = execute_query(
            "SELECT user_id FROM users WHERE user_name = %s",
            (user_name,),
            dictionary=True,
        )
        if rows:
            return int(rows[0]["user_id"])
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Failed to look up user id: %s", exc)
    return None
