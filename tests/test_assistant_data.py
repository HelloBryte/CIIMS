"""
Unit tests for utils/assistant_data.py.

These cover the AI assistant's SQL guardrails: the SELECT-only allowlist,
the destructive-keyword blocklist, and the per-role table RBAC enforced by
validate_sql(). They also cover extract_sql_payload()'s JSON parsing of
model output, since a fuzzy match here fails open and returns {} (no
exception) if the payload doesn't parse.

No database connection is required: validate_sql() and
extract_sql_payload() are pure functions and never touch the DB
(execute_safe_sql is the DB-touching wrapper, not tested here).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.assistant_data import extract_sql_payload, validate_sql  # noqa: E402


class TestValidateSql:
    def test_select_is_allowed(self):
        ok, result = validate_sql("SELECT * FROM items", "user")
        assert ok is True
        assert result == "SELECT * FROM items LIMIT 50"

    def test_existing_limit_is_preserved(self):
        ok, result = validate_sql("SELECT * FROM items LIMIT 10", "user")
        assert ok is True
        assert result == "SELECT * FROM items LIMIT 10"

    def test_empty_sql_is_rejected(self):
        ok, message = validate_sql("", "user")
        assert ok is False
        assert message == "Empty SQL string"

    def test_non_select_is_rejected(self):
        ok, message = validate_sql("DELETE FROM items", "admin")
        assert ok is False
        assert "Only SELECT" in message

    def test_blocklisted_keyword_inside_select_is_rejected(self):
        # DROP appears in the statement even though it starts with SELECT.
        ok, message = validate_sql(
            "SELECT * FROM items; DROP TABLE items", "admin"
        )
        assert ok is False
        assert "DROP" in message

    def test_user_role_cannot_read_users_table(self):
        ok, message = validate_sql("SELECT * FROM users", "user")
        assert ok is False
        assert "users" in message

    def test_admin_role_can_read_users_table(self):
        ok, result = validate_sql("SELECT * FROM users", "admin")
        assert ok is True
        assert "users" in result

    def test_unknown_role_falls_back_to_user_access(self):
        ok, message = validate_sql("SELECT * FROM users", "some_unknown_role")
        assert ok is False
        assert "users" in message

    def test_join_table_is_subject_to_rbac(self):
        ok, message = validate_sql(
            "SELECT * FROM items JOIN users ON items.item_id = users.user_id",
            "user",
        )
        assert ok is False
        assert "users" in message


class TestExtractSqlPayload:
    def test_plain_json_object(self):
        text = '{"intent": "list items", "proposed_sql": "SELECT 1"}'
        payload = extract_sql_payload(text)
        assert payload["intent"] == "list items"
        assert payload["proposed_sql"] == "SELECT 1"

    def test_fenced_json_block(self):
        text = '```json\n{"intent": "count borrows"}\n```'
        payload = extract_sql_payload(text)
        assert payload == {"intent": "count borrows"}

    def test_json_with_surrounding_prose_and_nested_object(self):
        # The brace-trimming fallback only kicks in once more than one "{"
        # is present (e.g. a nested object), so it's exercised here.
        text = (
            'Sure, here you go:\n'
            '{"intent": "hello", "meta": {"lang": "en"}}\n'
            'Let me know if needed.'
        )
        payload = extract_sql_payload(text)
        assert payload == {"intent": "hello", "meta": {"lang": "en"}}

    def test_single_brace_json_with_surrounding_prose_is_not_extracted(self):
        # Documents current behavior: with only one "{", the brace-trimming
        # fallback never triggers, so a lone JSON object embedded in prose
        # fails to parse and the function safely returns {}.
        text = 'Sure, here you go:\n{"intent": "hello"}\nLet me know if needed.'
        assert extract_sql_payload(text) == {}

    def test_empty_input_returns_empty_dict(self):
        assert extract_sql_payload("") == {}
        assert extract_sql_payload(None) == {}

    def test_unparseable_text_returns_empty_dict_instead_of_raising(self):
        assert extract_sql_payload("not json at all") == {}
