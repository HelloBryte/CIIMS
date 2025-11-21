import os

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox
)
from ui.base import AppleMessageDialog, AppleStyle
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from database.db import get_connection
from face_recognition.face_register_utils import capture_for_register, train_one_user


class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Account")
        self.setFixedSize(480, 600)
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
        title = QLabel("Create Account")
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
        self.name_input = self.create_input_field("Username")
        card_layout.addWidget(self.name_input)

        # Password input
        self.pwd_input = self.create_input_field("Password (at least 6 characters)", password=True)
        card_layout.addWidget(self.pwd_input)

        # Phone input
        self.phone_input = self.create_input_field("Phone Number")
        card_layout.addWidget(self.phone_input)

        # Face registration checkbox
        self.face_checkbox = QCheckBox("Register face recognition (optional)")
        self.face_checkbox.setChecked(False)
        self.face_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                padding: {AppleStyle.SPACING_SMALL}px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid {AppleStyle.BORDER};
            }}
            QCheckBox::indicator:checked {{
                background-color: {AppleStyle.PRIMARY};
                border: 2px solid {AppleStyle.PRIMARY};
            }}
        """)
        card_layout.addWidget(self.face_checkbox)

        # Submit button
        self.btn_submit = self.create_button("Create Account", self.submit_register, primary=True)
        card_layout.addWidget(self.btn_submit)

        # Cancel button
        self.btn_cancel = self.create_button("Cancel", self.close, primary=False)
        card_layout.addWidget(self.btn_cancel)

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
        else:
            bg_color = AppleStyle.CARD_BACKGROUND
            hover_color = "#F0F0F0"
            text_color = AppleStyle.PRIMARY
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 600;
                padding: {AppleStyle.SPACING_MEDIUM}px;
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
        """Submit registration"""
        name = self.name_input.text().strip()
        pwd = self.pwd_input.text().strip()
        phone = self.phone_input.text().strip()
        register_face = self.face_checkbox.isChecked()

        # Validation
        if not name or not pwd or not phone:
            dialog = AppleMessageDialog(self, "Input Error", "Please fill in all required fields", "warning")
            dialog.exec()
            return

        if len(pwd) < 6:
            dialog = AppleMessageDialog(self, "Input Error", "Password must be at least 6 characters long", "warning")
            dialog.exec()
            return

        try:
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

            # If face registration is selected
            if register_face:
                dialog = AppleMessageDialog(
                    self, 
                    "Start Capture", 
                    "Please look at the camera. The system will capture 5 face images for model training.",
                    "info"
                )
                dialog.exec()

                # Call model training method
                capture_for_register(user_id, 5)
                train_one_user(user_id)

                # Clear temporary files
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
                    "UPDATE users SET face_registered = 1 WHERE user_id = %s", 
                    (user_id,)
                )
                conn.commit()
                cursor.close()
                conn.close()

                dialog = AppleMessageDialog(
                    self, 
                    "Success", 
                    "Registration successful! You can now use both password and face recognition to login.",
                    "info"
                )
                dialog.exec()
            else:
                dialog = AppleMessageDialog(
                    self, 
                    "Success", 
                    "Registration successful! You can now login with your username and password.",
                    "info"
                )
                dialog.exec()

            self.close()

        except Exception as e:
            if "Duplicate entry" in str(e) or "UNIQUE constraint" in str(e):
                dialog = AppleMessageDialog(self, "Error", f"Username '{name}' already exists. Please choose another username.", "warning")
                dialog.exec()
            else:
                dialog = AppleMessageDialog(self, "Error", f"Registration failed: {str(e)}", "error")
                dialog.exec()

