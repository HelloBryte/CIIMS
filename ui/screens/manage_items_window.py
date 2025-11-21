from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QSpinBox, QTextEdit, QDialog
)
from PySide6.QtCore import Qt
from database.db import get_connection
from ui.base import AppleStyle, AppleMessageDialog, AppleConfirmDialog


class EditItemDialog(QDialog):
    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.item_data = item_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Edit Item")
        self.setFixedSize(500, 500)
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
        title = QLabel("Edit Item")
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

        # Item Name
        name_label = QLabel("Item Name:")
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
        self.name_input.setText(self.item_data['item_name'])
        self.name_input.setMinimumHeight(50)
        self.name_input.setStyleSheet(f"""
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
        layout.addWidget(self.name_input)

        # Category
        category_label = QLabel("Category:")
        category_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(category_label)
        self.category_input = QLineEdit()
        self.category_input.setText(self.item_data['item_category'] or '')
        self.category_input.setMinimumHeight(50)
        self.category_input.setStyleSheet(f"""
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
        layout.addWidget(self.category_input)

        # Quantity
        quantity_label = QLabel("Quantity:")
        quantity_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(quantity_label)
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(0)
        self.quantity_input.setMaximum(9999)
        self.quantity_input.setValue(self.item_data['item_quantity'])
        self.quantity_input.setMinimumHeight(50)
        self.quantity_input.setStyleSheet(f"""
            QSpinBox {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                padding: {AppleStyle.SPACING_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                color: {AppleStyle.TEXT_PRIMARY};
            }}
            QSpinBox:focus {{
                border: 2px solid {AppleStyle.PRIMARY};
            }}
        """)
        layout.addWidget(self.quantity_input)

        # Remark
        remark_label = QLabel("Remark:")
        remark_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(remark_label)
        self.remark_input = QTextEdit()
        self.remark_input.setText(self.item_data['remark'] or '')
        self.remark_input.setMaximumHeight(100)
        self.remark_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                padding: {AppleStyle.SPACING_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                color: {AppleStyle.TEXT_PRIMARY};
            }}
            QTextEdit:focus {{
                border: 2px solid {AppleStyle.PRIMARY};
            }}
        """)
        layout.addWidget(self.remark_input)

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

    def get_data(self):
        return {
            'item_name': self.name_input.text().strip(),
            'item_category': self.category_input.text().strip() or None,
            'item_quantity': self.quantity_input.value(),
            'remark': self.remark_input.toPlainText().strip() or None
        }


class ManageItemsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_items()

    def initUI(self):
        self.setWindowTitle("Manage Items")
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
        title = QLabel("Manage Items")
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

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Item Name",
            "Category",
            "Quantity",
            "Actions"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Item Name
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Category
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Quantity
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Actions
        
        layout.addWidget(self.table)

        # Button area
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(AppleStyle.SPACING_MEDIUM)
        
        self.btn_refresh = self.create_button("Refresh", self.load_items, primary=False)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addStretch()
        
        self.btn_close = self.create_button("Close", self.close, primary=True)
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

    def load_items(self):
        """Load all items from database"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT item_id, item_name, item_category, item_quantity, remark
                FROM items
                ORDER BY item_id
            """)
            items = cursor.fetchall()
            cursor.close()
            conn.close()
            
            self.table.setRowCount(0)
            
            for row, item in enumerate(items):
                self.table.insertRow(row)
                
                # ID
                self.table.setItem(row, 0, QTableWidgetItem(str(item['item_id'])))
                
                # Item Name
                self.table.setItem(row, 1, QTableWidgetItem(item['item_name']))
                
                # Category
                self.table.setItem(row, 2, QTableWidgetItem(item['item_category'] or 'N/A'))
                
                # Quantity
                quantity_item = QTableWidgetItem(str(item['item_quantity']))
                if item['item_quantity'] == 0:
                    quantity_item.setForeground(Qt.red)
                self.table.setItem(row, 3, quantity_item)
                
                # Actions
                action_widget = QWidget()
                action_layout = QHBoxLayout()
                action_layout.setContentsMargins(2, 2, 2, 2)
                
                btn_edit = QPushButton("Edit")
                btn_edit.clicked.connect(lambda checked, item_id=item['item_id']: self.edit_item(item_id))
                action_layout.addWidget(btn_edit)
                
                btn_delete = QPushButton("Delete")
                btn_delete.clicked.connect(lambda checked, item_id=item['item_id'], item_name=item['item_name']: 
                                         self.delete_item(item_id, item_name))
                action_layout.addWidget(btn_delete)
                
                action_widget.setLayout(action_layout)
                self.table.setCellWidget(row, 4, action_widget)
                
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Failed to load items: {str(e)}", "error")
            dialog.exec()

    def edit_item(self, item_id):
        """Edit an item"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT item_id, item_name, item_category, item_quantity, remark
                FROM items
                WHERE item_id = %s
            """, (item_id,))
            item_data = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if not item_data:
                dialog = AppleMessageDialog(self, "Error", "Item not found", "warning")
                dialog.exec()
                return
            
            dialog = EditItemDialog(item_data, self)
            if dialog.exec() == QDialog.Accepted:
                new_data = dialog.get_data()
                
                if not new_data['item_name']:
                    dialog = AppleMessageDialog(self, "Error", "Item name cannot be empty", "warning")
                    dialog.exec()
                    return
                
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE items
                    SET item_name = %s, item_category = %s, item_quantity = %s, remark = %s
                    WHERE item_id = %s
                """, (new_data['item_name'], new_data['item_category'], 
                      new_data['item_quantity'], new_data['remark'], item_id))
                conn.commit()
                cursor.close()
                conn.close()
                
                dialog = AppleMessageDialog(self, "Success", "Item updated successfully!", "info")
                dialog.exec()
                self.load_items()
                
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Failed to edit item: {str(e)}", "error")
            dialog.exec()

    def delete_item(self, item_id, item_name):
        """Delete an item"""
        dialog = AppleConfirmDialog(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{item_name}'?\n\nThis action cannot be undone."
        )
        
        if dialog.exec() != QDialog.Accepted:
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Check if item is currently borrowed
            cursor.execute("""
                SELECT COUNT(*) as count FROM borrows
                WHERE item_id = %s AND return_status = 'not_returned'
            """, (item_id,))
            result = cursor.fetchone()
            
            if result[0] > 0:
                dialog = AppleMessageDialog(
                    self,
                    "Cannot Delete",
                    f"Cannot delete '{item_name}' because it is currently borrowed by {result[0]} user(s).",
                    "warning"
                )
                dialog.exec()
                cursor.close()
                conn.close()
                return
            
            cursor.execute("DELETE FROM items WHERE item_id = %s", (item_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            dialog = AppleMessageDialog(self, "Success", f"Item '{item_name}' deleted successfully!", "info")
            dialog.exec()
            self.load_items()
            
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Failed to delete item: {str(e)}", "error")
            dialog.exec()

