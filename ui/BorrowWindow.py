from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QDateEdit
)
from PySide6.QtCore import Qt, QDate, QLocale
from datetime import datetime, timedelta
from database.db import get_connection
from ui.base_window import AppleStyle, AppleMessageDialog


class BorrowWindow(QMainWindow):
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name
        self.user_id = None
        self.initUI()
        self.load_items()
        self.get_user_id()

    def initUI(self):
        self.setWindowTitle("Borrow Item")
        self.setFixedSize(550, 450)
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
        title = QLabel("Borrow Item")
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

        # Item selection
        item_label = QLabel("Select Item:")
        item_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        card_layout.addWidget(item_label)
        
        self.item_combo = QComboBox()
        self.item_combo.setMinimumHeight(50)
        self.item_combo.setStyleSheet(f"""
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
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        card_layout.addWidget(self.item_combo)

        # Return deadline
        deadline_label = QLabel("Return Deadline:")
        deadline_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        card_layout.addWidget(deadline_label)
        
        # Default to 30 days later
        default_date = QDate.currentDate().addDays(30)
        self.deadline_edit = QDateEdit()
        self.deadline_edit.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
        self.deadline_edit.setDate(default_date)
        self.deadline_edit.setCalendarPopup(True)
        self.deadline_edit.setMinimumDate(QDate.currentDate())
        max_date = QDate.currentDate().addMonths(6)
        self.deadline_edit.setMaximumDate(max_date)
        self.deadline_edit.setMinimumHeight(50)
        self.deadline_edit.setStyleSheet(f"""
            QDateEdit {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                padding: {AppleStyle.SPACING_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                color: {AppleStyle.TEXT_PRIMARY};
            }}
            QDateEdit:focus {{
                border: 2px solid {AppleStyle.PRIMARY};
            }}
        """)
        card_layout.addWidget(self.deadline_edit)
        
        # Hint label
        hint_label = QLabel("(Maximum: 6 months from today)")
        hint_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_SECONDARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_SMALL}px;
            }}
        """)
        card_layout.addWidget(hint_label)

        # Button area
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(AppleStyle.SPACING_MEDIUM)
        
        self.btn_submit = self.create_button("Confirm Borrow", self.submit_borrow, primary=True)
        btn_layout.addWidget(self.btn_submit)
        
        self.btn_cancel = self.create_button("Cancel", self.close, primary=False)
        btn_layout.addWidget(self.btn_cancel)
        
        card_layout.addLayout(btn_layout)

        layout.addWidget(card)
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
        """)

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

    def get_user_id(self):
        """Get user ID from username"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT user_id FROM users WHERE user_name=%s", (self.user_name,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                self.user_id = user['user_id']
            else:
                dialog = AppleMessageDialog(self, "Error", "Failed to get user information", "error")
                dialog.exec()
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Database connection failed: {str(e)}", "error")
            dialog.exec()

    def load_items(self):
        """Load available items list (items with stock > 0)"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT item_id, item_name, item_category, item_quantity 
                FROM items 
                WHERE item_quantity > 0
                ORDER BY item_name
            """)
            items = cursor.fetchall()
            cursor.close()
            conn.close()
            
            self.item_combo.clear()
            self.items_data = {}  # Store item_id -> item_info mapping
            
            if not items:
                dialog = AppleMessageDialog(self, "Notice", "No items available for borrowing", "info")
                dialog.exec()
                self.item_combo.addItem("No items available")
                self.btn_submit.setEnabled(False)
            else:
                for item in items:
                    display_text = f"{item['item_name']} ({item['item_category']}) - Stock: {item['item_quantity']}"
                    self.item_combo.addItem(display_text)
                    self.items_data[display_text] = item
                    
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Failed to load items list: {str(e)}", "error")
            dialog.exec()
            self.item_combo.addItem("Load failed")
            self.btn_submit.setEnabled(False)

    def submit_borrow(self):
        """Submit borrow request"""
        if not self.user_id:
            dialog = AppleMessageDialog(self, "Error", "Failed to get user information", "warning")
            dialog.exec()
            return
        
        # Get selected item
        selected_text = self.item_combo.currentText()
        if not selected_text or selected_text == "No items available" or selected_text == "Load failed":
            dialog = AppleMessageDialog(self, "Notice", "Please select an item to borrow", "warning")
            dialog.exec()
            return
        
        item_info = self.items_data.get(selected_text)
        if not item_info:
            dialog = AppleMessageDialog(self, "Error", "Failed to get item information", "warning")
            dialog.exec()
            return
        
        item_id = item_info['item_id']
        
        # Get return deadline
        deadline_date = self.deadline_edit.date().toPython()
        deadline_datetime = datetime.combine(deadline_date, datetime.min.time())
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        max_deadline = today + timedelta(days=180)  # Approximately 6 months
        
        # Validate deadline cannot be earlier than today
        if deadline_datetime < today:
            dialog = AppleMessageDialog(self, "Error", "Return deadline cannot be earlier than today", "warning")
            dialog.exec()
            return
        
        # Validate deadline cannot be more than 6 months from today
        if deadline_datetime > max_deadline:
            dialog = AppleMessageDialog(self, "Error", "Return deadline cannot be more than 6 months from today", "warning")
            dialog.exec()
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Check stock again
            cursor.execute("SELECT item_quantity FROM items WHERE item_id=%s", (item_id,))
            result = cursor.fetchone()
            if not result or result[0] <= 0:
                dialog = AppleMessageDialog(self, "Notice", "Insufficient stock for this item", "warning")
                dialog.exec()
                cursor.close()
                conn.close()
                return
            
            # Insert borrow record (don't specify return_status, use database default)
            cursor.execute("""
                INSERT INTO borrows (item_id, user_id, return_deadline)
                VALUES (%s, %s, %s)
            """, (item_id, self.user_id, deadline_datetime))
            
            # Update item stock (decrease by 1)
            cursor.execute("""
                UPDATE items 
                SET item_quantity = item_quantity - 1 
                WHERE item_id = %s
            """, (item_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            success_message = (
                f"Item borrowed successfully!\n\n"
                f"Item: {item_info['item_name']}\n"
                f"Return Deadline: {deadline_datetime.strftime('%Y-%m-%d')}"
            )
            dialog = AppleMessageDialog(self, "Success", success_message, "info")
            dialog.exec()
            
            # Refresh items list
            self.load_items()
            
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Borrow failed: {str(e)}", "error")
            dialog.exec()

