from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QDialog
)
from PySide6.QtCore import Qt
from datetime import datetime
from database.db import get_connection
from ui.base_window import AppleStyle, AppleMessageDialog, AppleConfirmDialog


class ReturnWindow(QMainWindow):
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name
        self.user_id = None
        self.initUI()
        self.get_user_id()
        self.load_borrowed_items()

    def initUI(self):
        self.setWindowTitle("Return Item")
        self.setFixedSize(900, 600)
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
        title = QLabel("Return Item")
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

        # Notice label - Simulated return process
        notice_label = QLabel("⚠️ Note: This is a simulated return process. In real scenarios, items are automatically recorded when returned on-site.")
        notice_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.WARNING};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_SMALL}px;
                padding: {AppleStyle.SPACING_MEDIUM}px;
                background-color: #FFF3CD;
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
            }}
        """)
        notice_label.setWordWrap(True)
        layout.addWidget(notice_label)

        # Table to display borrowed items
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Item Name", 
            "Category", 
            "Borrow Time", 
            "Return Deadline", 
            "Status", 
            "Action"
        ])
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Item Name
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Category
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Borrow Time
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Return Deadline
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Action
        
        layout.addWidget(self.table)

        # Button area
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(AppleStyle.SPACING_MEDIUM)
        
        self.btn_refresh = self.create_button("Refresh", self.load_borrowed_items, primary=False)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addStretch()
        
        self.btn_cancel = self.create_button("Close", self.close, primary=True)
        btn_layout.addWidget(self.btn_cancel)
        
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

    def load_borrowed_items(self):
        """Load user's borrowed items that are not returned"""
        if not self.user_id:
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query borrowed items with item details
            cursor.execute("""
                SELECT 
                    b.borrow_id,
                    b.item_id,
                    b.borrow_time,
                    b.return_deadline,
                    b.return_status,
                    i.item_name,
                    i.item_category
                FROM borrows b
                JOIN items i ON b.item_id = i.item_id
                WHERE b.user_id = %s AND b.return_status = 'not_returned'
                ORDER BY b.borrow_time DESC
            """, (self.user_id,))
            
            items = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Clear table
            self.table.setRowCount(0)
            
            if not items:
                dialog = AppleMessageDialog(self, "Notice", "No items to return", "info")
                dialog.exec()
                return
            
            # Populate table
            for row, item in enumerate(items):
                self.table.insertRow(row)
                
                # Item Name
                self.table.setItem(row, 0, QTableWidgetItem(item['item_name']))
                
                # Category
                self.table.setItem(row, 1, QTableWidgetItem(item['item_category'] or 'N/A'))
                
                # Borrow Time
                borrow_time = item['borrow_time']
                if isinstance(borrow_time, datetime):
                    borrow_time_str = borrow_time.strftime('%Y-%m-%d %H:%M')
                else:
                    borrow_time_str = str(borrow_time)
                self.table.setItem(row, 2, QTableWidgetItem(borrow_time_str))
                
                # Return Deadline
                deadline = item['return_deadline']
                if isinstance(deadline, datetime):
                    deadline_str = deadline.strftime('%Y-%m-%d')
                else:
                    deadline_str = str(deadline)
                self.table.setItem(row, 3, QTableWidgetItem(deadline_str))
                
                # Status (check if overdue)
                deadline_dt = deadline if isinstance(deadline, datetime) else datetime.strptime(str(deadline), '%Y-%m-%d %H:%M:%S')
                if deadline_dt < datetime.now():
                    status_item = QTableWidgetItem("Overdue")
                    status_item.setForeground(Qt.red)
                else:
                    status_item = QTableWidgetItem("Not Returned")
                self.table.setItem(row, 4, status_item)
                
                # Return Button
                return_btn = QPushButton("Return")
                return_btn.clicked.connect(lambda checked, borrow_id=item['borrow_id'], item_id=item['item_id'], item_name=item['item_name']: 
                                         self.return_item(borrow_id, item_id, item_name))
                self.table.setCellWidget(row, 5, return_btn)
                
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Failed to load borrowed items: {str(e)}", "error")
            dialog.exec()

    def return_item(self, borrow_id, item_id, item_name):
        """Return an item"""
        try:
            dialog = AppleConfirmDialog(
                self, 
                "Confirm Return", 
                f"Are you sure you want to return '{item_name}'?"
            )
            
            if dialog.exec() != QDialog.Accepted:
                return
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Update borrow record
            current_time = datetime.now()
            cursor.execute("""
                UPDATE borrows 
                SET return_time = %s, return_status = 'returned'
                WHERE borrow_id = %s
            """, (current_time, borrow_id))
            
            # Increase item stock
            cursor.execute("""
                UPDATE items 
                SET item_quantity = item_quantity + 1 
                WHERE item_id = %s
            """, (item_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            dialog = AppleMessageDialog(self, "Success", f"Item '{item_name}' returned successfully!", "info")
            dialog.exec()
            
            # Refresh the list
            self.load_borrowed_items()
            
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Return failed: {str(e)}", "error")
            dialog.exec()

