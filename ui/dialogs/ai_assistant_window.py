"""
In-app AI assistant dialog for CIIMS
"""

from __future__ import annotations

import html
from typing import Any, Callable, Dict, List, Optional

from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ui.base import AppleStyle
from utils.assistant_service import AssistantService, AssistantServiceError
from utils import assistant_data


class AssistantWorker(QThread):
    """Background worker that keeps the UI responsive during API calls"""

    finished = Signal(dict)
    failed = Signal(str)

    def __init__(
        self,
        service: AssistantService,
        history: List[Dict[str, Any]],
        runtime_context: str,
        user_name: str,
        user_role: str,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.service = service
        # Copy history to avoid accidental mutations across threads
        self.history = [message.copy() for message in history]
        self.runtime_context = runtime_context
        self.user_name = user_name
        self.user_role = user_role

    def run(self) -> None:
        try:
            latest_prompt = self._get_latest_user_prompt()

            # Step 1: Classify intent
            intent_result = self.service.classify_intent(latest_prompt)
            intent_type = intent_result.get("intent_type", "general_qa")

            if intent_type == "database_query":
                # Route to database query handler
                result = self._handle_database_query()
            else:
                # Route to general Q&A handler
                result = self._handle_general_qa()

            self.finished.emit(result)

        except AssistantServiceError as exc:
            self.failed.emit(str(exc))
        except Exception as exc:  # pylint: disable=broad-except
            self.failed.emit(str(exc))

    def _handle_general_qa(self) -> Dict[str, Any]:
        """Handle general questions without SQL generation"""
        try:
            # Use the regular assistant context for general questions
            runtime_context = self._context_provider() if self._context_provider else ""

            reply = self.service.ask(
                self.history,
                runtime_context,
                reasoning_enabled=False,
            )

            # Add to history
            self.history.append(
                {"role": "assistant", "content": reply.get("content", "")}
            )
            return reply

        except Exception as exc:
            return {
                "content": f"Failed to get answer: {str(exc)}",
                "reasoning_details": None,
            }

    def _handle_database_query(self) -> Dict[str, Any]:
        """Handle database queries with SQL generation and validation"""
        try:
            # Build SQL-specific context
            sql_context = assistant_data.build_runtime_context(
                self.user_role, self.user_name
            )
            if self.runtime_context:
                sql_context = f"{sql_context}\n\nRuntime note:\n{self.runtime_context}"

            # Get SQL proposal from AI
            first_reply = self.service.ask(
                self.history,
                sql_context,
                reasoning_enabled=False,
            )

            content = first_reply.get("content", "")
            payload = assistant_data.extract_sql_payload(content)
            proposed_sql = (
                (payload.get("proposed_sql") or "").strip()
                if isinstance(payload, dict)
                else ""
            )

            if proposed_sql:
                # Execute SQL and format results
                follow_up = self._handle_sql_follow_up(
                    proposed_sql,
                    sql_context,
                    first_reply,
                )
                return follow_up
            else:
                # No SQL needed, return the general response
                self.history.append({"role": "assistant", "content": content})
                return first_reply

        except Exception as exc:
            return {
                "content": f"Database query failed: {str(exc)}",
                "reasoning_details": None,
            }

    def _get_latest_user_prompt(self) -> str:
        for message in reversed(self.history):
            if message.get("role") == "user":
                return str(message.get("content") or "")
        return ""

    def _handle_sql_follow_up(
        self,
        sql: str,
        runtime_context: str,
        first_reply: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate, execute, and summarize SQL proposed by the model.
        """
        try:
            rows = assistant_data.execute_safe_sql(sql, self.user_role, self.user_name)
        except Exception as exc:  # pylint: disable=broad-except
            return {
                "content": f"SQL validation failed: {exc}",
                "reasoning_details": None,
            }

        system_message = assistant_data.build_result_system_message(sql, rows)
        self.history.append(
            {"role": "assistant", "content": first_reply.get("content", "")}
        )
        self.history.append({"role": "system", "content": system_message})

        follow_up_reply = self.service.ask(
            self.history,
            runtime_context,
            reasoning_enabled=False,
        )
        self.history.append(
            {"role": "assistant", "content": follow_up_reply.get("content", "")}
        )
        return follow_up_reply


class AIAssistantWindow(QDialog):
    """Frameless dialog that surfaces the CIIMS AI helper"""

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        user_name: str = "",
        user_role: str = "user",
        context_provider: Optional[Callable[[], str]] = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("CIIMS AI Assistant")
        self.setModal(False)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setFixedSize(520, 640)

        self._context_provider = context_provider
        self._service = AssistantService()
        self._messages: List[Dict[str, Any]] = []
        self._worker: Optional[AssistantWorker] = None
        self._user_name = user_name
        self._user_role = user_role

        self._build_ui()
        welcome_text = (
            "Hi! I'm the CIIMS copilot. Ask me about inventory, borrowing, users, or troubleshooting and "
            "I'll answer right away."
        )
        self._append_message("Assistant", welcome_text)
        self._messages.append(
            {
                "role": "assistant",
                "content": welcome_text,
            }
        )

    def _build_ui(self) -> None:
        self.setStyleSheet(
            f"""
            QDialog {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border-radius: {AppleStyle.RADIUS_LARGE}px;
            }}
            QTextEdit {{
                background-color: {AppleStyle.BACKGROUND};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                color: {AppleStyle.TEXT_PRIMARY};
                padding: {AppleStyle.SPACING_MEDIUM}px;
            }}
            QTextEdit:focus {{
                border: 2px solid {AppleStyle.PRIMARY};
                background-color: {AppleStyle.CARD_BACKGROUND};
            }}
            QLabel#StatusLabel {{
                color: {AppleStyle.TEXT_SECONDARY};
                font-size: {AppleStyle.FONT_SIZE_SMALL}px;
            }}
            QLabel#LoadingLabel {{
                color: {AppleStyle.PRIMARY};
                font-size: {AppleStyle.FONT_SIZE_SMALL}px;
            }}
        """
        )

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            AppleStyle.SPACING_LARGE,
            AppleStyle.SPACING_LARGE,
            AppleStyle.SPACING_LARGE,
            AppleStyle.SPACING_LARGE,
        )
        main_layout.setSpacing(AppleStyle.SPACING_MEDIUM)

        header = QLabel("CIIMS Assistant")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(
            f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_MEDIUM}px;
                font-weight: 600;
            }}
        """
        )
        main_layout.addWidget(header)

        self.status_label = QLabel("Online", objectName="StatusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        self.history_view = QTextEdit()
        self.history_view.setReadOnly(True)
        self.history_view.setMinimumHeight(360)
        main_layout.addWidget(self.history_view)

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText(
            "Ask anything about CIIMS (inventory, borrowing, users, etc.)..."
        )
        self.input_box.setFixedHeight(110)
        main_layout.addWidget(self.input_box)

        self.loading_label = QLabel(" ", objectName="LoadingLabel")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.hide()
        main_layout.addWidget(self.loading_label)

        self.loading_timer = QTimer(self)
        self.loading_timer.setInterval(300)
        self.loading_timer.timeout.connect(self._update_loading_indicator)
        self._loading_phase = 0

        button_row = QHBoxLayout()
        button_row.addStretch()

        self.clear_button = QPushButton("Reset Chat")
        self.clear_button.clicked.connect(self.reset_conversation)
        self.clear_button.setStyleSheet(self._secondary_button_style())
        button_row.addWidget(self.clear_button)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_send)
        self.send_button.setStyleSheet(self._primary_button_style())
        button_row.addWidget(self.send_button)

        main_layout.addLayout(button_row)

    def _primary_button_style(self) -> str:
        return f"""
            QPushButton {{
                background-color: {AppleStyle.PRIMARY};
                color: #FFFFFF;
                border: none;
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 600;
                padding: {AppleStyle.SPACING_MEDIUM}px {AppleStyle.SPACING_LARGE}px;
                min-width: 120px;
                min-height: 46px;
            }}
            QPushButton:disabled {{
                background-color: {AppleStyle.BORDER};
                color: {AppleStyle.TEXT_SECONDARY};
            }}
            QPushButton:hover:!disabled {{
                background-color: {AppleStyle.PRIMARY_HOVER};
            }}
        """

    def _secondary_button_style(self) -> str:
        return f"""
            QPushButton {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                color: {AppleStyle.PRIMARY};
                border: 1px solid {AppleStyle.PRIMARY};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 600;
                padding: {AppleStyle.SPACING_MEDIUM}px {AppleStyle.SPACING_LARGE}px;
                min-width: 120px;
                min-height: 46px;
            }}
            QPushButton:hover {{
                background-color: {AppleStyle.BACKGROUND};
            }}
        """

    def _append_message(self, author: str, content: str) -> None:
        escaped = html.escape(content).replace("\n", "<br>")
        self.history_view.append(f"<b>{author}:</b> {escaped}")
        self.history_view.verticalScrollBar().setValue(
            self.history_view.verticalScrollBar().maximum()
        )

    def handle_send(self) -> None:
        if self._worker is not None:
            return

        prompt = self.input_box.toPlainText().strip()
        if not prompt:
            self.status_label.setText("Please enter a question before sending.")
            return

        self._append_message("You", prompt)
        self._messages.append({"role": "user", "content": prompt})
        self.input_box.clear()
        self._toggle_inputs(False, "Assistant is responding...")

        runtime_context = self._context_provider() if self._context_provider else ""
        self._worker = AssistantWorker(
            self._service,
            self._messages,
            runtime_context,
            self._user_name,
            self._user_role,
            self,
        )
        self._worker.finished.connect(self._handle_success)
        self._worker.failed.connect(self._handle_failure)
        self._worker.finished.connect(self._cleanup_worker)
        self._worker.failed.connect(self._cleanup_worker)
        self._worker.start()

    def _handle_success(self, reply: Dict[str, Any]) -> None:
        content = reply.get("content", "")
        reasoning_details = reply.get("reasoning_details")
        entry: Dict[str, Any] = {"role": "assistant", "content": content}
        if reasoning_details:
            entry["reasoning_details"] = reasoning_details
        self._messages.append(entry)
        self._append_message("Assistant", content)
        self._toggle_inputs(True, "Ready for the next question.")

    def _handle_failure(self, error_message: str) -> None:
        self._append_message(
            "Assistant", f"Sorry, I could not respond: {error_message}"
        )
        self._toggle_inputs(True, "Connection issue. Try again.")

    def _cleanup_worker(self) -> None:
        if self._worker:
            self._worker.deleteLater()
        self._worker = None

    def _toggle_inputs(self, enabled: bool, status_text: str) -> None:
        self.send_button.setEnabled(enabled)
        self.clear_button.setEnabled(enabled)
        self.input_box.setReadOnly(not enabled)
        self.status_label.setText(status_text)
        if not enabled:
            self.loading_label.show()
            self._loading_phase = 0
            self._update_loading_indicator()
            self.loading_timer.start()
        else:
            self.loading_timer.stop()
            self.loading_label.hide()

    def reset_conversation(self) -> None:
        if self._worker is not None:
            return
        self._messages.clear()
        self.history_view.clear()
        self._append_message(
            "Assistant",
            "Conversation reset. How can I help you with CIIMS now?",
        )
        self._messages.append(
            {
                "role": "assistant",
                "content": "Conversation reset and ready.",
            }
        )
        self.status_label.setText("Chat cleared.")

    def closeEvent(self, event: QCloseEvent) -> None:  # type: ignore[override]
        if self._worker is not None:
            event.ignore()
            self.status_label.setText("Please wait for the current response...")
            return
        super().closeEvent(event)

    def _update_loading_indicator(self):
        phases = [
            "Assistant is responding",
            "Assistant is responding.",
            "Assistant is responding..",
            "Assistant is responding...",
        ]
        self.loading_label.setText(phases[self._loading_phase % len(phases)])
        self._loading_phase += 1
