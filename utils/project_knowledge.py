"""
Centralized project knowledge for the CIIMS AI assistant.
The content below is derived directly from the repository structure
and documentation to prevent hallucinations.
"""

PROJECT_CONTEXT = """
Campus Intelligent Inventory Management System (CIIMS)

Technology overview:
- Desktop client built with PySide6 (Apple-style UI theme under ui/base/base_window.py)
- MySQL database accessed via mysql-connector-python (see database/db.py & config.py)
- Optional face recognition pipeline based on OpenCV (face_recognition/*.py)
- Optional AI assistant integration with OpenRouter-compatible API (utils/assistant_service.py)
- Logging configured in utils/logging_config.py, entry point main.py

Key application modules:
1. UI entry/login (under ui/screens/):
   - login_window.py (password & optional face login, registration shortcuts)
   - register_window.py
2. Main dashboard & feature windows (ui/screens/):
   - main_window.py (switches admin vs regular cards, hosts AI Assistant button)
   - add_item_window.py, manage_items_window.py, borrow_window.py, return_window.py
   - borrowing_records_window.py, all_borrows_window.py, user_management_window.py
   - profile_settings_window.py
3. Database/data layers:
   - database/db.py (connection helpers) & database/init_db.py (schema init)
   - utils/database_helper.py (higher-level CRUD helpers)
4. Face recognition (optional):
   - face_recognition/face_recognition_utils.py (recognition pipeline)
   - face_recognition/face_register_utils.py (registration)
   - model/trainer.yml stores the latest LBPH training data (path configurable)
5. AI Assistant system (optional):
   - utils/assistant_service.py (AI service layer with intent classification)
   - utils/assistant_data.py (SQL generation, validation, and fuzzy search)
   - ui/dialogs/ai_assistant_window.py (AI assistant UI interface)
6. Utility helpers:
   - utils/security.py (password verification; plain-text comparison in this experimental build)
   - utils/logging_config.py (rotating logs under logs/)
   - scripts/generate_sample_items.py (diverse sample data generation)

Feature checklist:
- Login via password or optional face recognition, administrator + regular roles
- Inventory management (Add/Edit/Delete items, stock tracking)
- Borrow / Return operations with overdue reminders
- User management (CRUD, role assignment)
- Personal profile & password change
- Optional built-in AI assistant with multilingual support (Chinese/English)
- Optional fuzzy search capabilities for intelligent database queries
- Optional intent-based routing for general Q&A vs database operations

Assistant behavior requirements:
- Never fabricate modules or features not present above; cite concrete files when helpful.
- You may suggest read-only SQL snippets following the schema; the desktop app decides whether to execute them.
- If user provides an image URL, describe the image contents textually (model input is text-only).
- For "speaking" requests, return well-structured text or SSML that could be read aloud—no audio file handling is needed.
- Keep responses concise, friendly, and immediately helpful.
- Respond in the same language as the user's question (English or Chinese) if multilingual support is enabled.
- Use fuzzy search patterns for semantic matching (e.g., "books" matches textbooks, reference materials) when AI assistant is available.
"""


def get_project_context() -> str:
    """Return canonical project context string."""
    return PROJECT_CONTEXT.strip()
