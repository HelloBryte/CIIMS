"""
AI assistant service for CIIMS using OpenRouter (OpenAI-compatible API)
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import httpx

from config import Config
from utils.logging_config import get_logger
from utils.project_knowledge import get_project_context

logger = get_logger(__name__)


class AssistantServiceError(Exception):
    """Custom exception for assistant related errors"""


class AssistantService:
    """Service layer for interacting with the OpenRouter-powered assistant"""

    def __init__(self) -> None:
        self._ensure_proxy()
        self.client = httpx.Client(
            timeout=60,
            follow_redirects=True,
        )
        self.endpoint = f"{Config.OPENROUTER_BASE_URL.rstrip('/')}/chat/completions"
        self.project_context = (
            "You are CIIMS-Sherlock, the embedded AI copilot inside the Campus "
            "Intelligent Inventory Management System desktop app.\n\n"
            f"{get_project_context()}\n\n"
            "General instructions:\n"
            "- Stay within the CIIMS scope (inventory, borrowing, login, basic troubleshooting).\n"
            "- Be concise and practical; prioritize clear step-by-step answers when needed.\n"
            "- You may propose read-only SQL queries based on the schema, but the app will decide whether to run them.\n"
            "- You can interpret image URLs by describing their contents, and you can provide speech-like responses "
            "using natural language or SSML snippets when the user asks you to 'speak'.\n"
            "- Whenever helpful, reference concrete files or modules (e.g., ui/screens/main_window.py) from the context.\n"
            "- IMPORTANT: Always respond in the same language as the user's question (支持中文和英文，用用户提问的语言回复)."
        )

    def _ensure_proxy(self) -> None:
        """Guarantee API requests go through the required proxy"""
        if not Config.PROXY_URL:
            return

        for env_name in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
            if not os.getenv(env_name):
                os.environ[env_name] = Config.PROXY_URL
                logger.info(
                    "Configured %s for AI assistant proxy (%s)",
                    env_name,
                    Config.PROXY_URL,
                )

    def _build_headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        if Config.OPENROUTER_REFERER:
            headers["HTTP-Referer"] = Config.OPENROUTER_REFERER
        if Config.OPENROUTER_TITLE:
            headers["X-Title"] = Config.OPENROUTER_TITLE
        return headers

    def _build_messages(
        self,
        history: List[Dict[str, Any]],
        runtime_context: str = "",
    ) -> List[Dict[str, Any]]:
        system_prompt = self.project_context
        if runtime_context:
            system_prompt += (
                "\n\nRuntime context from the CIIMS app:\n" f"{runtime_context.strip()}"
            )

        messages: List[Dict[str, Any]] = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        return messages

    def classify_intent(self, user_input: str) -> Dict[str, Any]:
        """Classify whether user input requires database query or general Q&A"""
        classification_prompt = f"""
Classify this user request for CIIMS (library management system):

User input: "{user_input}"

Return JSON with:
- "intent_type": "database_query" if asking about data, records, statistics, inventory counts, borrowing history, etc.
- "intent_type": "general_qa" if asking about how-to, troubleshooting, explanations, system info, etc.
- "confidence": 0.0-1.0
- "reasoning": brief explanation

Examples:
"How many books are available?" -> database_query
"How do I return an item?" -> general_qa
"Show my borrowing history" -> database_query
"Why can't I login?" -> general_qa
"""

        messages = [
            {
                "role": "system",
                "content": "You are an intent classifier. Respond only with valid JSON.",
            },
            {"role": "user", "content": classification_prompt},
        ]

        try:
            payload = {
                "model": Config.OPENROUTER_MODEL,
                "messages": messages,
                "response_format": {"type": "json_object"},
            }
            response = self.client.post(
                self.endpoint,
                headers=self._build_headers(),
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            choices = data.get("choices") or []
            if not choices:
                return {
                    "intent_type": "general_qa",
                    "confidence": 0.5,
                    "reasoning": "Failed to classify, defaulting to general",
                }

            content = choices[0].get("message", {}).get("content", "{}")
            import json

            result = json.loads(content)

            # Validate and normalize
            intent_type = result.get("intent_type", "general_qa")
            if intent_type not in ["database_query", "general_qa"]:
                intent_type = "general_qa"

            return {
                "intent_type": intent_type,
                "confidence": float(result.get("confidence", 0.5)),
                "reasoning": result.get("reasoning", "No reasoning provided"),
            }

        except Exception as exc:
            logger.warning("Intent classification failed: %s", exc)
            return {
                "intent_type": "general_qa",
                "confidence": 0.3,
                "reasoning": "Classification failed, defaulting to general",
            }

    def ask(
        self,
        history: List[Dict[str, Any]],
        runtime_context: str = "",
        reasoning_enabled: bool = False,
    ) -> Dict[str, Optional[Any]]:
        """Send the chat completion request and return the assistant reply plus metadata"""
        try:
            messages = self._build_messages(history, runtime_context)
            logger.debug("Sending %d messages to AI assistant", len(messages))
            payload: Dict[str, Any] = {
                "model": Config.OPENROUTER_MODEL,
                "messages": messages,
            }
            if reasoning_enabled:
                payload["reasoning"] = {"enabled": True}
            response = self.client.post(
                self.endpoint,
                headers=self._build_headers(),
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            choices = data.get("choices") or []
            if not choices:
                raise AssistantServiceError("Assistant returned no choices")
            response_message = choices[0].get("message") or {}
            content = response_message.get("content")
            if not content:
                raise AssistantServiceError("Assistant returned empty response")
            reasoning_details = response_message.get("reasoning_details")
            return {
                "content": content.strip(),
                "reasoning_details": reasoning_details,
            }
        except httpx.HTTPError as exc:
            logger.exception("HTTP error while calling AI assistant: %s", exc)
            raise AssistantServiceError(str(exc)) from exc
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("AI assistant request failed: %s", exc)
            raise AssistantServiceError(str(exc)) from exc
