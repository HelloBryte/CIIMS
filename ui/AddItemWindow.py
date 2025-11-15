from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QSpinBox, QTextEdit
)
from PySide6.QtCore import Qt
from database.db import get_connection
from ui.base_window import AppleStyle, AppleMessageDialog


class AddItemWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Item")
        self.setFixedSize(500, 500)
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
        title = QLabel("Add New Item")
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
        card_layout.addWidget(name_label)
        self.name_input = self.create_input_field("Enter item name")
        card_layout.addWidget(self.name_input)

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
        card_layout.addWidget(category_label)
        self.category_input = self.create_input_field("Enter category (e.g., Books, Electronics)")
        card_layout.addWidget(self.category_input)

        # Quantity
        quantity_label = QLabel("Initial Quantity:")
        quantity_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        card_layout.addWidget(quantity_label)
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(0)
        self.quantity_input.setMaximum(9999)
        self.quantity_input.setValue(0)
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
        card_layout.addWidget(self.quantity_input)

        # Remark
        remark_label = QLabel("Remark (Optional):")
        remark_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        card_layout.addWidget(remark_label)
        self.remark_input = QTextEdit()
        self.remark_input.setPlaceholderText("Enter remarks or description")
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
            QTextEdit::placeholder {{
                color: {AppleStyle.TEXT_SECONDARY};
            }}
        """)
        card_layout.addWidget(self.remark_input)

        # Button area
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(AppleStyle.SPACING_MEDIUM)
        
        self.btn_submit = self.create_button("Add Item", self.add_item, primary=True)
        btn_layout.addWidget(self.btn_submit)
        
        self.btn_cancel = self.create_button("Cancel", self.close, primary=False)
        btn_layout.addWidget(self.btn_cancel)
        
        card_layout.addLayout(btn_layout)

        layout.addWidget(card)
        self.setCentralWidget(container)

    def create_input_field(self, placeholder=""):
        """Create an input field with Apple-style design"""
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
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

    def add_item(self):
        """Add new item to database"""
        name = self.name_input.text().strip()
        category = self.category_input.text().strip()
        quantity = self.quantity_input.value()
        remark = self.remark_input.toPlainText().strip()

        if not name:
            dialog = AppleMessageDialog(self, "Error", "Item name cannot be empty", "warning")
            dialog.exec()
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO items (item_name, item_category, item_quantity, remark)
                VALUES (%s, %s, %s, %s)
            """, (name, category if category else None, quantity, remark if remark else None))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            dialog = AppleMessageDialog(self, "Success", f"Item '{name}' added successfully!", "info")
            dialog.exec()
            
            # Clear inputs
            self.name_input.clear()
            self.category_input.clear()
            self.quantity_input.setValue(0)
            self.remark_input.clear()
            
        except Exception as e:
            dialog = AppleMessageDialog(self, "Error", f"Failed to add item: {str(e)}", "error")
            dialog.exec()

