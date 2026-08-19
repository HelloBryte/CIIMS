from PySide6.QtWidgets import (
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
)
from PySide6.QtCore import Qt
from database.db import get_connection
from utils.security import verify_password
from utils.logging_config import get_logger

from ui.screens.register_window import RegisterWindow
from ui.screens.main_window import MainWindow
from ui.base import BaseWindow, AppleStyle, AppleMessageDialog

logger = get_logger(__name__)


class LoginWindow(BaseWindow):
    """Login window for CIIMS application"""

    def __init__(self):
        super().__init__()
        self.main_window = None  # Initialize attribute in __init__
        self.register_window = None  # Initialize attribute in __init__
        self.initUI()
        self.setup_connections()

    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle("CIIMS Login")
        self.setFixedSize(500, 600)

        # Main container
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Title
        title = QLabel("Welcome to CIIMS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_LARGE}px;
                font-weight: 700;
                padding: 20px 0;
            }}
        """
        )
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Campus Intelligent Inventory Management System")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(
            f"""
            QLabel {{
                color: {AppleStyle.TEXT_SECONDARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                padding-bottom: 20px;
            }}
        """
        )
        layout.addWidget(subtitle)

        # Login card
        card = QWidget()
        card.setStyleSheet(
            f"""
            QWidget {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border-radius: {AppleStyle.RADIUS_LARGE}px;
                padding: 30px;
            }}
        """
        )
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)

        # Username input
        username_label = QLabel("Username")
        username_label.setStyleSheet(
            f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """
        )
        card_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(50)
        self.username_input.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {AppleStyle.BACKGROUND};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                padding: 15px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                color: {AppleStyle.TEXT_PRIMARY};
            }}
            QLineEdit:focus {{
                border: 2px solid {AppleStyle.PRIMARY};
            }}
        """
        )
        card_layout.addWidget(self.username_input)

        # Password input
        password_label = QLabel("Password")
        password_label.setStyleSheet(
            f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """
        )
        card_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(50)
        self.password_input.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {AppleStyle.BACKGROUND};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                padding: 15px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                color: {AppleStyle.TEXT_PRIMARY};
            }}
            QLineEdit:focus {{
                border: 2px solid {AppleStyle.PRIMARY};
            }}
        """
        )
        card_layout.addWidget(self.password_input)

        # Login button
        self.btn_login = QPushButton("Login")
        self.btn_login.setMinimumHeight(50)
        self.btn_login.clicked.connect(self.login)
        self.btn_login.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {AppleStyle.PRIMARY};
                color: #FFFFFF;
                border: none;
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 600;
                padding: 15px;
            }}
            QPushButton:hover {{
                background-color: {AppleStyle.PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {AppleStyle.PRIMARY_HOVER};
            }}
        """
        )
        card_layout.addWidget(self.btn_login)

        # Register button
        self.btn_register = QPushButton("Create Account")
        self.btn_register.setMinimumHeight(50)
        self.btn_register.clicked.connect(self.open_register)
        self.btn_register.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {AppleStyle.BACKGROUND};
                color: {AppleStyle.TEXT_SECONDARY};
                border: none;
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_SMALL}px;
                font-weight: 500;
                padding: 10px;
            }}
            QPushButton:hover {{
                color: {AppleStyle.PRIMARY};
            }}
        """
        )
        card_layout.addWidget(self.btn_register)

        layout.addWidget(card)
        self.setCentralWidget(container)

    def setup_connections(self):
        """Setup signal connections"""
        # Enter key login
        self.password_input.returnPressed.connect(self.login)
        self.username_input.returnPressed.connect(self.login)

    def login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            dialog = AppleMessageDialog(
                self, "Error", "Please enter username and password", "error"
            )
            dialog.exec()
            return

        try:
            # Get user from database
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT user_id, user_name, user_role, user_password FROM users WHERE user_name = %s",
                (username,),
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if not user:
                dialog = AppleMessageDialog(
                    self, "Error", "Invalid username or password", "error"
                )
                dialog.exec()
                return

            # Verify password
            if not verify_password(password, user["user_password"]):
                dialog = AppleMessageDialog(
                    self, "Error", "Invalid username or password", "error"
                )
                dialog.exec()
                return

            # Login successful - open main window
            self.main_window = MainWindow(user["user_name"], user["user_role"])
            self.main_window.show()
            self.close()

        except Exception as e:
            logger.error("Login error: %s", e, exc_info=True)
            dialog = AppleMessageDialog(
                self, "Error", "Login failed. Please try again.", "error"
            )
            dialog.exec()

    def open_register(self):
        """Open registration window"""
        # RegisterWindow is a QMainWindow, not a QDialog, so it must be
        # shown (not exec()'d) and kept alive via an attribute reference
        # to avoid being garbage-collected immediately.
        self.register_window = RegisterWindow()
        self.register_window.show()
