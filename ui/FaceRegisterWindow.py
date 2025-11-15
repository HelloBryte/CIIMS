import os

from PySide6.QtWidgets import (
    QWidget, QLineEdit, QMainWindow,
    QVBoxLayout, QPushButton, QLabel
)
from PySide6.QtCore import Qt
from database.db import get_connection
from face_recognition.face_register_utils import capture_for_register, train_one_user
from ui.base_window import AppleStyle, AppleMessageDialog


class FaceRegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Registration")
        self.setFixedSize(450, 500)
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
        title = QLabel("Face Registration")
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

        self.name_input = self.create_input_field("Enter name")
        card_layout.addWidget(self.name_input)

        self.phone_input = self.create_input_field("Enter phone number")
        card_layout.addWidget(self.phone_input)

        self.pwd_input = self.create_input_field("Set password", password=True)
        card_layout.addWidget(self.pwd_input)

        self.btn_submit = self.create_button("Submit and Capture Face", self.submit_register, primary=True)
        card_layout.addWidget(self.btn_submit)

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

    def submit_register(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        pwd = self.pwd_input.text().strip()

        if not (name and phone and pwd):
            dialog = AppleMessageDialog(self, "Input Error", "Please fill in all fields", "warning")
            dialog.exec()
            return

        # Write to database, get user_id
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (user_name, user_password, user_role, user_phone, face_registered)"
            " VALUES (%s,%s,'user',%s, 0)",
            (name, pwd, phone)
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()

        try:
            dialog = AppleMessageDialog(self, "Start Capture", "Please look at the camera. The system will capture 5 face images for model training", "info")
            dialog.exec()

            # Call model training method
            capture_for_register(user_id, 5)
            train_one_user(user_id)

            # Clear temporary files (if temp directory exists)
            folder = "temp"
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

            # Update face registration status in database
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET face_registered = 1 WHERE user_id = %s", (user_id,)
            )
            conn.commit()
            cursor.close()
            conn.close()

            # Interface notification
            dialog = AppleMessageDialog(self, "Success", "Registration successful! You can now use face recognition to login", "info")
            dialog.exec()
            self.close()
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Face registration failed: {str(e)}", "error")
            dialog.exec()
