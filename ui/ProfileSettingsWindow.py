from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QDialog,
    QGroupBox,
)
from PySide6.QtCore import Qt
import os
from database.db import get_connection
from face_recognition.face_register_utils import capture_for_register, train_one_user
from ui.base_window import AppleStyle, AppleMessageDialog, AppleConfirmDialog


class ProfileSettingsWindow(QMainWindow):
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name
        self.user_id = None
        self.user_info = None
        self.initUI()
        self.get_user_info()
        self.load_user_info()

    def initUI(self):
        self.setWindowTitle("Profile Settings")
        self.setFixedSize(500, 700)

        # Main container
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Profile Settings")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)

        # Account Information Group
        info_group = QGroupBox("Account Information")
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)

        self.info_username = QLabel("Username: -")
        info_layout.addWidget(self.info_username)

        self.info_role = QLabel("Role: -")
        info_layout.addWidget(self.info_role)

        self.info_phone = QLabel("Phone: -")
        info_layout.addWidget(self.info_phone)

        self.info_face_status = QLabel("Face Recognition: -")
        info_layout.addWidget(self.info_face_status)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Change Phone Number Group
        phone_group = QGroupBox("Change Phone Number")
        phone_layout = QVBoxLayout()
        phone_layout.setSpacing(10)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter new phone number")
        self.phone_input.setMinimumHeight(40)
        phone_layout.addWidget(self.phone_input)

        self.btn_update_phone = QPushButton("Update Phone Number")
        self.btn_update_phone.setMinimumHeight(40)
        self.btn_update_phone.clicked.connect(self.update_phone)
        phone_layout.addWidget(self.btn_update_phone)

        phone_group.setLayout(phone_layout)
        layout.addWidget(phone_group)

        # Change Password Group
        password_group = QGroupBox("Change Password")
        password_layout = QVBoxLayout()
        password_layout.setSpacing(10)

        self.old_password_input = QLineEdit()
        self.old_password_input.setPlaceholderText("Enter current password")
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.old_password_input.setMinimumHeight(40)
        password_layout.addWidget(self.old_password_input)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setMinimumHeight(40)
        password_layout.addWidget(self.new_password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setMinimumHeight(40)
        password_layout.addWidget(self.confirm_password_input)

        self.btn_update_password = QPushButton("Update Password")
        self.btn_update_password.setMinimumHeight(40)
        self.btn_update_password.clicked.connect(self.update_password)
        password_layout.addWidget(self.btn_update_password)

        password_group.setLayout(password_layout)
        layout.addWidget(password_group)

        # Face Recognition Group
        face_group = QGroupBox("Face Recognition")
        face_layout = QVBoxLayout()
        face_layout.setSpacing(10)

        self.face_status_label = QLabel("")
        self.face_status_label.setWordWrap(True)
        face_layout.addWidget(self.face_status_label)

        self.btn_update_face = QPushButton("Update Face Recognition")
        self.btn_update_face.setMinimumHeight(40)
        self.btn_update_face.clicked.connect(self.update_face_recognition)
        face_layout.addWidget(self.btn_update_face)

        face_group.setLayout(face_layout)
        layout.addWidget(face_group)

        layout.addStretch()

        # Close button
        self.btn_close = QPushButton("Close")
        self.btn_close.setMinimumHeight(40)
        self.btn_close.clicked.connect(self.close)
        layout.addWidget(self.btn_close)

        self.setCentralWidget(container)

    def get_user_info(self):
        """Get user information from database"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT user_id, user_name, user_role, user_phone, face_registered 
                FROM users 
                WHERE user_name=%s
            """,
                (self.user_name,),
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                self.user_id = user["user_id"]
                self.user_info = user
            else:
                dialog = AppleMessageDialog(
                    self, "Error", "Failed to get user information", "error"
                )
                dialog.exec()
        except Exception as e:
            dialog = AppleMessageDialog(
                self, "Error", f"Database connection failed: {str(e)}", "error"
            )
            dialog.exec()

    def load_user_info(self):
        """Load and display user information"""
        if not self.user_info:
            return

        self.info_username.setText(f"Username: {self.user_info['user_name']}")
        self.info_role.setText(f"Role: {self.user_info['user_role'].capitalize()}")
        self.info_phone.setText(f"Phone: {self.user_info['user_phone']}")

        if self.user_info["face_registered"]:
            self.info_face_status.setText("Face Recognition: Registered")
            self.info_face_status.setStyleSheet("color: green;")
            self.face_status_label.setText(
                "Face recognition is registered. You can update it by clicking the button below."
            )
        else:
            self.info_face_status.setText("Face Recognition: Not Registered")
            self.info_face_status.setStyleSheet("color: orange;")
            self.face_status_label.setText(
                "Face recognition is not registered. Click the button below to register."
            )

    def update_phone(self):
        """Update phone number"""
        if not self.user_id:
            dialog = AppleMessageDialog(
                self, "Error", "User information not loaded", "warning"
            )
            dialog.exec()
            return

        new_phone = self.phone_input.text().strip()
        if not new_phone:
            dialog = AppleMessageDialog(
                self, "Error", "Please enter a new phone number", "warning"
            )
            dialog.exec()
            return

        # Basic phone number validation
        if not new_phone.replace("-", "").replace(" ", "").replace("(", "").replace(
            ")", ""
        ).isdigit():
            dialog = AppleMessageDialog(
                self, "Error", "Please enter a valid phone number", "warning"
            )
            dialog.exec()
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE users 
                SET user_phone = %s 
                WHERE user_id = %s
            """,
                (new_phone, self.user_id),
            )
            conn.commit()
            cursor.close()
            conn.close()

            dialog = AppleMessageDialog(
                self, "Success", "Phone number updated successfully!", "info"
            )
            dialog.exec()
            self.phone_input.clear()
            # Refresh user info
            self.get_user_info()
            self.load_user_info()

        except Exception as e:
            dialog = AppleMessageDialog(
                self, "Error", f"Failed to update phone number: {str(e)}", "error"
            )
            dialog.exec()

    def update_password(self):
        """Update password"""
        if not self.user_id:
            dialog = AppleMessageDialog(
                self, "Error", "User information not loaded", "warning"
            )
            dialog.exec()
            return

        old_password = self.old_password_input.text().strip()
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not old_password or not new_password or not confirm_password:
            dialog = AppleMessageDialog(
                self, "Error", "Please fill in all password fields", "warning"
            )
            dialog.exec()
            return

        if new_password != confirm_password:
            dialog = AppleMessageDialog(
                self,
                "Error",
                "New password and confirmation do not match",
                "warning",
            )
            dialog.exec()
            return

        if len(new_password) < 6:
            dialog = AppleMessageDialog(
                self,
                "Error",
                "Password must be at least 6 characters long",
                "warning",
            )
            dialog.exec()
            return

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Verify old password
            cursor.execute(
                """
                SELECT user_password FROM users WHERE user_id = %s
            """,
                (self.user_id,),
            )
            result = cursor.fetchone()

            if not result or result["user_password"] != old_password:
                dialog = AppleMessageDialog(
                    self, "Error", "Current password is incorrect", "warning"
                )
                dialog.exec()
                cursor.close()
                conn.close()
                return

            # Update password
            cursor.execute(
                """
                UPDATE users 
                SET user_password = %s 
                WHERE user_id = %s
            """,
                (new_password, self.user_id),
            )
            conn.commit()
            cursor.close()
            conn.close()

            dialog = AppleMessageDialog(
                self, "Success", "Password updated successfully!", "info"
            )
            dialog.exec()
            self.old_password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()

        except Exception as e:
            dialog = AppleMessageDialog(
                self, "Error", f"Failed to update password: {str(e)}", "error"
            )
            dialog.exec()

    def update_face_recognition(self):
        """Update face recognition data"""
        if not self.user_id:
            dialog = AppleMessageDialog(
                self, "Error", "User information not loaded", "warning"
            )
            dialog.exec()
            return

        dialog = AppleConfirmDialog(
            self,
            "Update Face Recognition",
            "This will update your face recognition data. Please make sure you are in a well-lit environment and look directly at the camera.\n\nContinue?",
        )

        if dialog.exec() != QDialog.Accepted:
            return

        try:
            dialog = AppleMessageDialog(
                self,
                "Start Capture",
                "Please look at the camera. The system will capture 5 face images for model training.",
                "info",
            )
            dialog.exec()

            # Capture face images
            capture_for_register(self.user_id, 5)

            # Train the model
            train_one_user(self.user_id)

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
                (self.user_id,),
            )
            conn.commit()
            cursor.close()
            conn.close()

            dialog = AppleMessageDialog(
                self,
                "Success",
                "Face recognition updated successfully! You can now use face recognition to login.",
                "info",
            )
            dialog.exec()

            # Refresh user info
            self.get_user_info()
            self.load_user_info()

        except Exception as e:
            dialog = AppleMessageDialog(
                self,
                "Error",
                f"Failed to update face recognition: {str(e)}",
                "error",
            )
            dialog.exec()
