from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt
from database.db import get_connection
from ui.base_window import AppleStyle, AppleMessageDialog


class PasswordLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Login")
        self.setFixedSize(400, 400)
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
        # Main container
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE
        )
        layout.setSpacing(AppleStyle.SPACING_LARGE)
        layout.addStretch()

        # Create card
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border-radius: {AppleStyle.RADIUS_LARGE}px;
                padding: {AppleStyle.SPACING_LARGE}px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE
        )
        card_layout.setSpacing(AppleStyle.SPACING_LARGE)

        # Title
        title = QLabel("Password Login")
        title.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_LARGE}px;
                font-weight: 700;
                padding: {AppleStyle.SPACING_MEDIUM}px;
            }}
        """)
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # Username input
        self.input_username = self.create_input_field("Enter username")
        card_layout.addWidget(self.input_username)

        # Password input
        self.input_password = self.create_input_field("Enter password", password=True)
        card_layout.addWidget(self.input_password)

        # Login button
        self.btn_login = self.create_button("Login", self.do_login, primary=True)
        card_layout.addWidget(self.btn_login)

        layout.addWidget(card)
        layout.addStretch()
        self.setCentralWidget(container)

    def create_input_field(self, placeholder="", password=False):
        """Create an input field with Apple-style design"""
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        if password:
            input_field.setEchoMode(QLineEdit.Password)
        input_field.setMinimumHeight(50)
        input_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                padding: {AppleStyle.SPACING_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                color: {AppleStyle.TEXT_PRIMARY};
            }}
            QLineEdit:focus {{
                border: 2px solid {AppleStyle.PRIMARY};
            }}
            QLineEdit::placeholder {{
                color: {AppleStyle.TEXT_SECONDARY};
            }}
        """)
        return input_field

    def create_button(self, text, callback=None, primary=True):
        """Create a button with Apple-style design"""
        button = QPushButton(text)
        button.setMinimumHeight(50)
        if primary:
            bg_color = AppleStyle.PRIMARY
            hover_color = AppleStyle.PRIMARY_HOVER
            text_color = "#FFFFFF"
            border_style = "none"
        else:
            bg_color = AppleStyle.CARD_BACKGROUND
            hover_color = "#F0F0F0"
            text_color = AppleStyle.PRIMARY
            border_style = f"1px solid {AppleStyle.BORDER}"
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: {border_style};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 600;
                padding: {AppleStyle.SPACING_MEDIUM}px {AppleStyle.SPACING_LARGE}px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {hover_color};
            }}
        """)
        if callback:
            button.clicked.connect(callback)
        return button

    # Execute login logic (database verification)
    def do_login(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            dialog = AppleMessageDialog(self, "Notice", "Username and password cannot be empty", "warning")
            dialog.exec()
            return

        # Query database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM users WHERE user_name=%s AND user_password=%s"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            from ui.MainWindow import MainWindow
            dialog = AppleMessageDialog(self, "Success", f"Welcome {user['user_name']}!", "info")
            dialog.exec()
            # Open main window
            self.main_window = MainWindow(user['user_name'], user['user_role'])
            self.main_window.show()
            self.close()  # Close login window after successful login
        else:
            dialog = AppleMessageDialog(self, "Failed", "Incorrect username or password", "error")
            dialog.exec()
