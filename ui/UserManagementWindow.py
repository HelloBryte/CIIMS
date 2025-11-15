from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QComboBox, QDialog
)
from PySide6.QtCore import Qt
from database.db import get_connection
from ui.base_window import AppleStyle, AppleMessageDialog, AppleConfirmDialog


class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add New User")
        self.setFixedSize(450, 450)
        self.apply_apple_style()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE
        )
        layout.setSpacing(AppleStyle.SPACING_LARGE)

        # Title
        title = QLabel("Add New User")
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
        layout.addWidget(title)

        # Username
        name_label = QLabel("Username:")
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(name_label)
        self.name_input = self.create_input_field("Enter username")
        layout.addWidget(self.name_input)

        # Password
        password_label = QLabel("Password:")
        password_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(password_label)
        self.password_input = self.create_input_field("Enter password", password=True)
        layout.addWidget(self.password_input)

        # Phone
        phone_label = QLabel("Phone Number:")
        phone_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(phone_label)
        self.phone_input = self.create_input_field("Enter phone number")
        layout.addWidget(self.phone_input)

        # Role
        role_label = QLabel("Role:")
        role_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(role_label)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["user", "admin"])
        self.role_combo.setMinimumHeight(50)
        self.role_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                padding: {AppleStyle.SPACING_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                color: {AppleStyle.TEXT_PRIMARY};
            }}
            QComboBox:focus {{
                border: 2px solid {AppleStyle.PRIMARY};
            }}
        """)
        layout.addWidget(self.role_combo)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(AppleStyle.SPACING_MEDIUM)
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(44)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                color: {AppleStyle.TEXT_PRIMARY};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 600;
                padding: 12px 32px;
            }}
            QPushButton:hover {{
                background-color: {AppleStyle.BACKGROUND};
                border: 1px solid {AppleStyle.PRIMARY};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        ok_btn = QPushButton("OK")
        ok_btn.setMinimumHeight(44)
        ok_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppleStyle.PRIMARY};
                color: #FFFFFF;
                border: none;
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 600;
                padding: 12px 32px;
            }}
            QPushButton:hover {{
                background-color: {AppleStyle.PRIMARY_HOVER};
            }}
        """)
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        
        layout.addLayout(btn_layout)

    def apply_apple_style(self):
        """Apply Apple-style theme"""
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {AppleStyle.BACKGROUND};
                font-family: {AppleStyle.FONT_FAMILY};
            }}
        """)

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

    def get_data(self):
        return {
            'user_name': self.name_input.text().strip(),
            'user_password': self.password_input.text().strip(),
            'user_phone': self.phone_input.text().strip(),
            'user_role': self.role_combo.currentText()
        }


class EditUserDialog(QDialog):
    def __init__(self, user_data, parent=None):
        super().__init__(parent)
        self.user_data = user_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Edit User")
        self.setFixedSize(450, 500)
        self.apply_apple_style()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE
        )
        layout.setSpacing(AppleStyle.SPACING_LARGE)

        # Title
        title = QLabel("Edit User")
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
        layout.addWidget(title)

        # Username (read-only)
        name_label = QLabel("Username:")
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setText(self.user_data['user_name'])
        self.name_input.setReadOnly(True)
        self.name_input.setMinimumHeight(50)
        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {AppleStyle.BACKGROUND};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                padding: {AppleStyle.SPACING_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                color: {AppleStyle.TEXT_SECONDARY};
            }}
        """)
        layout.addWidget(self.name_input)

        # Password
        password_label = QLabel("New Password (leave empty to keep current):")
        password_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(password_label)
        self.password_input = self.create_input_field("Enter new password", password=True)
        layout.addWidget(self.password_input)

        # Phone
        phone_label = QLabel("Phone Number:")
        phone_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(phone_label)
        self.phone_input = QLineEdit()
        self.phone_input.setText(self.user_data['user_phone'])
        self.phone_input.setMinimumHeight(50)
        self.phone_input.setStyleSheet(f"""
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
        """)
        layout.addWidget(self.phone_input)

        # Role
        role_label = QLabel("Role:")
        role_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(role_label)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["user", "admin"])
        self.role_combo.setCurrentText(self.user_data['user_role'])
        self.role_combo.setMinimumHeight(50)
        self.role_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                padding: {AppleStyle.SPACING_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                color: {AppleStyle.TEXT_PRIMARY};
            }}
            QComboBox:focus {{
                border: 2px solid {AppleStyle.PRIMARY};
            }}
        """)
        layout.addWidget(self.role_combo)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(AppleStyle.SPACING_MEDIUM)
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(44)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                color: {AppleStyle.TEXT_PRIMARY};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 600;
                padding: 12px 32px;
            }}
            QPushButton:hover {{
                background-color: {AppleStyle.BACKGROUND};
                border: 1px solid {AppleStyle.PRIMARY};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        ok_btn = QPushButton("OK")
        ok_btn.setMinimumHeight(44)
        ok_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppleStyle.PRIMARY};
                color: #FFFFFF;
                border: none;
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 600;
                padding: 12px 32px;
            }}
            QPushButton:hover {{
                background-color: {AppleStyle.PRIMARY_HOVER};
            }}
        """)
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        
        layout.addLayout(btn_layout)

    def apply_apple_style(self):
        """Apply Apple-style theme"""
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {AppleStyle.BACKGROUND};
                font-family: {AppleStyle.FONT_FAMILY};
            }}
        """)

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

    def get_data(self):
        return {
            'user_password': self.password_input.text().strip(),
            'user_phone': self.phone_input.text().strip(),
            'user_role': self.role_combo.currentText()
        }


class UserManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_users()

    def initUI(self):
        self.setWindowTitle("User Management")
        self.setFixedSize(1100, 700)
        self.apply_apple_style()

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

        # Title
        title = QLabel("User Management")
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
        layout.addWidget(title)

        # Add user button
        btn_add = self.create_button("Add New User", self.add_user, primary=True)
        layout.addWidget(btn_add)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Username",
            "Role",
            "Phone",
            "Face Registered",
            "Actions"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Username
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Role
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Phone
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Face Registered
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Actions
        
        layout.addWidget(self.table)

        # Button area
        btn_layout = QHBoxLayout()
        
        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.clicked.connect(self.load_users)
        btn_layout.addWidget(self.btn_refresh)
        
        self.btn_close = QPushButton("Close")
        self.btn_close.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_close)
        
        layout.addLayout(btn_layout)

        self.setCentralWidget(container)

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
            QTableWidget {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                gridline-color: {AppleStyle.BORDER};
            }}
            QTableWidget::item {{
                padding: {AppleStyle.SPACING_SMALL}px;
            }}
            QHeaderView::section {{
                background-color: {AppleStyle.BACKGROUND};
                color: {AppleStyle.TEXT_PRIMARY};
                font-weight: 600;
                padding: {AppleStyle.SPACING_MEDIUM}px;
                border: none;
                border-bottom: 2px solid {AppleStyle.BORDER};
            }}
        """)

    def create_button(self, text, callback=None, primary=True):
        """Create a button with Apple-style design"""
        button = QPushButton(text)
        button.setMinimumHeight(44)
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
                padding: 10px 24px;
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

    def load_users(self):
        """Load all users from database"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT user_id, user_name, user_role, user_phone, face_registered
                FROM users
                ORDER BY user_id
            """)
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            
            self.table.setRowCount(0)
            
            for row, user in enumerate(users):
                self.table.insertRow(row)
                
                # ID
                self.table.setItem(row, 0, QTableWidgetItem(str(user['user_id'])))
                
                # Username
                self.table.setItem(row, 1, QTableWidgetItem(user['user_name']))
                
                # Role
                role_item = QTableWidgetItem(user['user_role'].capitalize())
                if user['user_role'] == 'admin':
                    role_item.setForeground(Qt.blue)
                self.table.setItem(row, 2, role_item)
                
                # Phone
                self.table.setItem(row, 3, QTableWidgetItem(user['user_phone']))
                
                # Face Registered
                face_status = "Yes" if user['face_registered'] else "No"
                face_item = QTableWidgetItem(face_status)
                if user['face_registered']:
                    face_item.setForeground(Qt.green)
                else:
                    face_item.setForeground(Qt.gray)
                self.table.setItem(row, 4, face_item)
                
                # Actions
                action_widget = QWidget()
                action_layout = QHBoxLayout()
                action_layout.setContentsMargins(2, 2, 2, 2)
                
                btn_edit = QPushButton("Edit")
                btn_edit.clicked.connect(lambda checked, user_id=user['user_id']: self.edit_user(user_id))
                action_layout.addWidget(btn_edit)
                
                btn_delete = QPushButton("Delete")
                btn_delete.clicked.connect(lambda checked, user_id=user['user_id'], username=user['user_name']: 
                                         self.delete_user(user_id, username))
                action_layout.addWidget(btn_delete)
                
                action_widget.setLayout(action_layout)
                self.table.setCellWidget(row, 5, action_widget)
                
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Failed to load users: {str(e)}", "error")
            dialog.exec()

    def add_user(self):
        """Add a new user"""
        dialog = AddUserDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            
            if not data['user_name'] or not data['user_password'] or not data['user_phone']:
                dialog = AppleMessageDialog(self, "Error", "Please fill in all required fields", "warning")
                dialog.exec()
                return
            
            if len(data['user_password']) < 6:
                dialog = AppleMessageDialog(self, "Error", "Password must be at least 6 characters long", "warning")
                dialog.exec()
                return
            
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (user_name, user_password, user_role, user_phone, face_registered)
                    VALUES (%s, %s, %s, %s, 0)
                """, (data['user_name'], data['user_password'], data['user_role'], data['user_phone']))
                conn.commit()
                cursor.close()
                conn.close()
                
                dialog = AppleMessageDialog(self, "Success", f"User '{data['user_name']}' added successfully!", "info")
                dialog.exec()
                self.load_users()
                
            except Exception as e:
                if "Duplicate entry" in str(e):
                    dialog = AppleMessageDialog(self, "Error", f"Username '{data['user_name']}' already exists", "warning")
                    dialog.exec()
                else:
                    dialog = AppleMessageDialog(self, "Error", f"Failed to add user: {str(e)}", "error")
                    dialog.exec()

    def edit_user(self, user_id):
        """Edit a user"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT user_id, user_name, user_role, user_phone, face_registered
                FROM users
                WHERE user_id = %s
            """, (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if not user_data:
                dialog = AppleMessageDialog(self, "Error", "User not found", "warning")
                dialog.exec()
                return
            
            dialog = EditUserDialog(user_data, self)
            if dialog.exec() == QDialog.Accepted:
                new_data = dialog.get_data()
                
                if not new_data['user_phone']:
                    dialog = AppleMessageDialog(self, "Error", "Phone number cannot be empty", "warning")
                    dialog.exec()
                    return
                
                conn = get_connection()
                cursor = conn.cursor()
                
                # Update password only if provided
                if new_data['user_password']:
                    if len(new_data['user_password']) < 6:
                        dialog = AppleMessageDialog(self, "Error", "Password must be at least 6 characters long", "warning")
                        dialog.exec()
                        cursor.close()
                        conn.close()
                        return
                    cursor.execute("""
                        UPDATE users
                        SET user_password = %s, user_phone = %s, user_role = %s
                        WHERE user_id = %s
                    """, (new_data['user_password'], new_data['user_phone'], 
                          new_data['user_role'], user_id))
                else:
                    cursor.execute("""
                        UPDATE users
                        SET user_phone = %s, user_role = %s
                        WHERE user_id = %s
                    """, (new_data['user_phone'], new_data['user_role'], user_id))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                dialog = AppleMessageDialog(self, "Success", "User updated successfully!", "info")
                dialog.exec()
                self.load_users()
                
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Failed to edit user: {str(e)}", "error")
            dialog.exec()

    def delete_user(self, user_id, username):
        """Delete a user"""
        dialog = AppleConfirmDialog(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete user '{username}'?\n\nThis action cannot be undone."
        )
        
        if dialog.exec() != QDialog.Accepted:
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Check if user has active borrows
            cursor.execute("""
                SELECT COUNT(*) as count FROM borrows
                WHERE user_id = %s AND return_status = 'not_returned'
            """, (user_id,))
            result = cursor.fetchone()
            
            if result[0] > 0:
                dialog = AppleMessageDialog(
                    self,
                    "Cannot Delete",
                    f"Cannot delete user '{username}' because they have {result[0]} active borrow(s).",
                    "warning"
                )
                dialog.exec()
                cursor.close()
                conn.close()
                return
            
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            dialog = AppleMessageDialog(self, "Success", f"User '{username}' deleted successfully!", "info")
            dialog.exec()
            self.load_users()
            
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Failed to delete user: {str(e)}", "error")
            dialog.exec()

