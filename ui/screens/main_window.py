from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
)
from PySide6.QtCore import Qt

from ui.base import AppleStyle
from ui.dialogs import AIAssistantWindow
from ui.screens.add_item_window import AddItemWindow
from ui.screens.all_borrows_window import AllBorrowsWindow
from ui.screens.borrow_window import BorrowWindow
from ui.screens.borrowing_records_window import BorrowingRecordsWindow
from ui.screens.manage_items_window import ManageItemsWindow
from ui.screens.profile_settings_window import ProfileSettingsWindow
from ui.screens.return_window import ReturnWindow
from ui.screens.user_management_window import UserManagementWindow


class MainWindow(QMainWindow):
    def __init__(self, user_name, user_role):
        super().__init__()
        self.user_name = user_name
        self.user_role = user_role
        self.assistant_window = None
        self.setWindowTitle(f"CIIMS - {user_name}")
        self.setFixedSize(600, 700)
        self.apply_apple_style()
        self.initUI()

    def apply_apple_style(self):
        """Apply Apple-style theme"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {AppleStyle.BACKGROUND};
            }}
            QWidget {{
                background-color: {AppleStyle.BACKGROUND};
                font-family: {AppleStyle.FONT_FAMILY};
            }}
        """)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE
        )
        layout.setSpacing(AppleStyle.SPACING_LARGE)

        # Welcome header
        welcome_label = QLabel(f"Welcome, {self.user_name}")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_LARGE}px;
                font-weight: 700;
                padding: {AppleStyle.SPACING_MEDIUM}px;
            }}
        """)
        layout.addWidget(welcome_label)

        # Create card for buttons
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border-radius: {AppleStyle.RADIUS_LARGE}px;
                padding: {AppleStyle.SPACING_LARGE}px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(AppleStyle.SPACING_MEDIUM)
        card_layout.setContentsMargins(
            AppleStyle.SPACING_LARGE,
            AppleStyle.SPACING_LARGE,
            AppleStyle.SPACING_LARGE,
            AppleStyle.SPACING_LARGE
        )

        # Different UI for admin and regular users
        if self.user_role == "admin":
            section_title = QLabel("Administrator")
            section_title.setStyleSheet(f"""
                QLabel {{
                    color: {AppleStyle.TEXT_SECONDARY};
                    font-family: {AppleStyle.FONT_FAMILY};
                    font-size: {AppleStyle.FONT_SIZE_SMALL}px;
                    font-weight: 600;
                    padding-bottom: {AppleStyle.SPACING_SMALL}px;
                }}
            """)
            card_layout.addWidget(section_title)

            btn_add_item = self.create_menu_button("Add New Item", self.open_add_item_window)
            card_layout.addWidget(btn_add_item)

            btn_edit_item = self.create_menu_button("Manage Items", self.open_manage_items_window)
            card_layout.addWidget(btn_edit_item)

            btn_all_users = self.create_menu_button("User Management", self.open_user_management_window)
            card_layout.addWidget(btn_all_users)

            btn_all_borrows = self.create_menu_button("All Borrowing Records", self.open_all_borrows_window)
            card_layout.addWidget(btn_all_borrows)

        else:
            section_title = QLabel("Quick Actions")
            section_title.setStyleSheet(f"""
                QLabel {{
                    color: {AppleStyle.TEXT_SECONDARY};
                    font-family: {AppleStyle.FONT_FAMILY};
                    font-size: {AppleStyle.FONT_SIZE_SMALL}px;
                    font-weight: 600;
                    padding-bottom: {AppleStyle.SPACING_SMALL}px;
                }}
            """)
            card_layout.addWidget(section_title)

            btn_borrow = self.create_menu_button("Borrow Items", self.open_borrow_window)
            card_layout.addWidget(btn_borrow)
            
            btn_return = self.create_menu_button("Return Items", self.open_return_window)
            card_layout.addWidget(btn_return)
            
            btn_records = self.create_menu_button("My Borrowing Records", self.open_records_window)
            card_layout.addWidget(btn_records)
            
            btn_profile = self.create_menu_button("Profile Settings", self.open_profile_settings)
            card_layout.addWidget(btn_profile)

        layout.addWidget(card)
        layout.addStretch()

        assistant_row = QHBoxLayout()
        assistant_row.addStretch()
        assistant_button = QPushButton("AI Assistant")
        assistant_button.setFixedSize(140, 44)
        assistant_button.clicked.connect(self.open_ai_assistant)
        assistant_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppleStyle.PRIMARY};
                color: #FFFFFF;
                border: none;
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {AppleStyle.PRIMARY_HOVER};
            }}
        """)
        assistant_row.addWidget(assistant_button)
        layout.addLayout(assistant_row)

    def create_menu_button(self, text, callback):
        """Create a menu button with Apple-style design"""
        button = QPushButton(text)
        button.setMinimumHeight(60)
        button.clicked.connect(callback)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                color: {AppleStyle.TEXT_PRIMARY};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
                padding: {AppleStyle.SPACING_MEDIUM}px {AppleStyle.SPACING_LARGE}px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {AppleStyle.BACKGROUND};
                border: 1px solid {AppleStyle.PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: {AppleStyle.BACKGROUND};
            }}
        """)
        return button

    def open_borrow_window(self):
        """Open borrow window"""
        self.borrow_window = BorrowWindow(self.user_name)
        self.borrow_window.show()

    def open_return_window(self):
        """Open return window"""
        self.return_window = ReturnWindow(self.user_name)
        self.return_window.show()

    def open_records_window(self):
        """Open borrowing records window"""
        self.records_window = BorrowingRecordsWindow(self.user_name)
        self.records_window.show()

    def open_profile_settings(self):
        """Open profile settings window"""
        self.profile_window = ProfileSettingsWindow(self.user_name)
        self.profile_window.show()

    # Admin functions
    def open_add_item_window(self):
        """Open add new item window"""
        self.add_item_window = AddItemWindow()
        self.add_item_window.show()

    def open_manage_items_window(self):
        """Open manage items window"""
        self.manage_items_window = ManageItemsWindow()
        self.manage_items_window.show()

    def open_user_management_window(self):
        """Open user management window"""
        self.user_management_window = UserManagementWindow()
        self.user_management_window.show()

    def open_all_borrows_window(self):
        """Open all borrowing records window"""
        self.all_borrows_window = AllBorrowsWindow()
        self.all_borrows_window.show()

    def open_ai_assistant(self):
        """Open the CIIMS AI assistant dialog"""
        if not hasattr(self, "assistant_window") or self.assistant_window is None:
            self.assistant_window = AIAssistantWindow(
                self,
                user_name=self.user_name,
                user_role=self.user_role,
                context_provider=self._build_assistant_context,
            )
            self.assistant_window.destroyed.connect(self._reset_assistant_window)
        self.assistant_window.show()
        self.assistant_window.raise_()
        self.assistant_window.activateWindow()

    def _build_assistant_context(self) -> str:
        """Provide runtime context for the assistant"""
        return (
            f"Active user: {self.user_name} "
            f"(role: {self.user_role}). "
            "The user is currently on the main dashboard."
        )

    def _reset_assistant_window(self):
        """Clear assistant window reference once it is closed"""
        self.assistant_window = None
