"""
Base window class for common UI functionality with Apple-style design
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QDialog,
    QGraphicsDropShadowEffect,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor, QPalette


class AppleStyle:
    """Apple-style design system"""
    
    # Colors - Apple-inspired palette
    BACKGROUND = "#F5F5F7"  # Light gray background
    CARD_BACKGROUND = "#FFFFFF"  # White cards
    PRIMARY = "#007AFF"  # Apple blue
    PRIMARY_HOVER = "#0051D5"
    SECONDARY = "#5856D6"  # Purple
    TEXT_PRIMARY = "#1D1D1F"  # Dark text
    TEXT_SECONDARY = "#86868B"  # Gray text
    BORDER = "#E5E5EA"  # Light border
    SUCCESS = "#34C759"  # Green
    WARNING = "#FF9500"  # Orange
    ERROR = "#FF3B30"  # Red
    
    # Typography
    FONT_FAMILY = "Arial, Helvetica, sans-serif"
    FONT_SIZE_LARGE = 28
    FONT_SIZE_MEDIUM = 17
    FONT_SIZE_REGULAR = 15
    FONT_SIZE_SMALL = 13
    
    # Spacing
    SPACING_SMALL = 8
    SPACING_MEDIUM = 16
    SPACING_LARGE = 24
    SPACING_XLARGE = 32
    
    # Border radius
    RADIUS_SMALL = 8
    RADIUS_MEDIUM = 12
    RADIUS_LARGE = 16


class BaseWindow(QMainWindow):
    """Base window class with Apple-style design"""

    def __init__(self, title="Window", size=(800, 600)):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(size[0], size[1])
        self.apply_apple_style()
        self.setup_ui()

    def apply_apple_style(self):
        """Apply Apple-style theme to the window"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {AppleStyle.BACKGROUND};
            }}
            QWidget {{
                background-color: {AppleStyle.BACKGROUND};
                font-family: {AppleStyle.FONT_FAMILY};
            }}
        """)

    def setup_ui(self):
        """Override in subclasses to setup specific UI"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE,
            AppleStyle.SPACING_XLARGE
        )
        self.main_layout.setSpacing(AppleStyle.SPACING_MEDIUM)

    def create_label(self, text, font_size=AppleStyle.FONT_SIZE_REGULAR, bold=False, color=None):
        """Create a label with Apple-style styling"""
        label = QLabel(text)
        font = QFont(AppleStyle.FONT_FAMILY, font_size)
        font.setWeight(QFont.Weight.DemiBold if bold else QFont.Weight.Normal)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        
        if color is None:
            color = AppleStyle.TEXT_PRIMARY if bold else AppleStyle.TEXT_SECONDARY
        
        label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                background-color: transparent;
                padding: {AppleStyle.SPACING_SMALL}px;
            }}
        """)
        return label

    def create_button(self, text, callback=None, primary=True, style="default"):
        """Create a button with Apple-style design"""
        button = QPushButton(text)
        button.setMinimumHeight(50)
        button.setMinimumWidth(120)
        
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
                margin: 0px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {hover_color};
            }}
            QPushButton:disabled {{
                background-color: {AppleStyle.BORDER};
                color: {AppleStyle.TEXT_SECONDARY};
            }}
        """)
        
        if callback:
            button.clicked.connect(callback)
        return button

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
                background-color: {AppleStyle.CARD_BACKGROUND};
            }}
            QLineEdit::placeholder {{
                color: {AppleStyle.TEXT_SECONDARY};
            }}
        """)
        return input_field

    def create_card(self):
        """Create a card widget with Apple-style design"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border-radius: {AppleStyle.RADIUS_LARGE}px;
                padding: {AppleStyle.SPACING_LARGE}px;
            }}
        """)
        return card

    def create_form_row(self, label_text, widget):
        """Create a form row with label and widget"""
        layout = QHBoxLayout()
        layout.setSpacing(AppleStyle.SPACING_MEDIUM)
        
        label = QLabel(label_text)
        label.setMinimumWidth(120)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(label)
        layout.addWidget(widget)
        layout.addStretch()
        return layout

    def show_info_message(self, title, message):
        """Show information message with Apple-style dialog"""
        dialog = AppleMessageDialog(self, title, message, "info")
        dialog.exec()

    def show_warning_message(self, title, message):
        """Show warning message with Apple-style dialog"""
        dialog = AppleMessageDialog(self, title, message, "warning")
        dialog.exec()

    def show_error_message(self, title, message):
        """Show error message with Apple-style dialog"""
        dialog = AppleMessageDialog(self, title, message, "error")
        dialog.exec()


class AppleMessageDialog(QDialog):
    """Apple-style message dialog"""
    
    def __init__(self, parent=None, title="", message="", message_type="info"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Calculate dialog size based on message length and lines
        # Count lines in message (including \n)
        line_count = message.count('\n') + 1
        # Calculate width: minimum 300, maximum 500, based on longest line
        lines = message.split('\n')
        max_line_length = max(len(line) for line in lines) if lines else len(message)
        width = min(500, max(300, max_line_length * 7 + 100))
        # Calculate height: base 180 + 30 per line, minimum 200, maximum 400
        height = min(400, max(200, 180 + line_count * 30))
        self.setFixedSize(width, height)
        
        # Create main container
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border-radius: {AppleStyle.RADIUS_LARGE}px;
            }}
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        container.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 32, 32, 24)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_MEDIUM}px;
                font-weight: 600;
                padding: 0px;
            }}
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Message
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignCenter)
        # Ensure text is fully visible - allow label to expand
        message_label.setMinimumHeight(60)
        message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        
        # Set color based on message type
        if message_type == "error":
            text_color = AppleStyle.ERROR
        elif message_type == "warning":
            text_color = AppleStyle.WARNING
        elif message_type == "info":
            text_color = AppleStyle.PRIMARY
        else:
            text_color = AppleStyle.TEXT_PRIMARY
        
        message_label.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 400;
                padding: 0px;
                line-height: 1.5;
            }}
        """)
        layout.addWidget(message_label)
        
        # Button
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        
        ok_button = QPushButton("OK")
        ok_button.setMinimumHeight(44)
        ok_button.setMinimumWidth(100)
        ok_button.setStyleSheet(f"""
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
            QPushButton:pressed {{
                background-color: {AppleStyle.PRIMARY_HOVER};
            }}
        """)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(container)
        
        # Center dialog on parent
        if parent:
            parent_geometry = parent.geometry()
            dialog_x = parent_geometry.x() + (parent_geometry.width() - width) // 2
            dialog_y = parent_geometry.y() + (parent_geometry.height() - height) // 2
            self.move(dialog_x, dialog_y)


class AppleConfirmDialog(QDialog):
    """Apple-style confirmation dialog with Yes/No buttons"""
    
    def __init__(self, parent=None, title="", message=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.result = False
        
        # Calculate dialog size based on message length
        width = min(450, max(350, len(message) * 8 + 100))
        height = 220
        self.setFixedSize(width, height)
        
        # Create main container
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                border-radius: {AppleStyle.RADIUS_LARGE}px;
            }}
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        container.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 32, 32, 24)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_MEDIUM}px;
                font-weight: 600;
                padding: 0px;
            }}
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Message
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet(f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 400;
                padding: 0px;
                line-height: 1.5;
            }}
        """)
        layout.addWidget(message_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(AppleStyle.SPACING_MEDIUM)
        button_layout.addStretch()
        
        no_button = QPushButton("No")
        no_button.setMinimumHeight(44)
        no_button.setMinimumWidth(100)
        no_button.setStyleSheet(f"""
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
            QPushButton:pressed {{
                background-color: {AppleStyle.BACKGROUND};
            }}
        """)
        no_button.clicked.connect(self.reject)
        button_layout.addWidget(no_button)
        
        yes_button = QPushButton("Yes")
        yes_button.setMinimumHeight(44)
        yes_button.setMinimumWidth(100)
        yes_button.setStyleSheet(f"""
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
            QPushButton:pressed {{
                background-color: {AppleStyle.PRIMARY_HOVER};
            }}
        """)
        yes_button.clicked.connect(self.accept)
        button_layout.addWidget(yes_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(container)
        
        # Center dialog on parent
        if parent:
            parent_geometry = parent.geometry()
            dialog_x = parent_geometry.x() + (parent_geometry.width() - width) // 2
            dialog_y = parent_geometry.y() + (parent_geometry.height() - height) // 2
            self.move(dialog_x, dialog_y)


class BaseDialog(QWidget):
    """Base dialog class for modal windows with Apple-style design"""

    def __init__(self, title="Dialog", size=(400, 300)):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(size[0], size[1])
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {AppleStyle.BACKGROUND};
                font-family: {AppleStyle.FONT_FAMILY};
            }}
        """)
        self.setup_ui()

    def setup_ui(self):
        """Override in subclasses to setup specific UI"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            AppleStyle.SPACING_LARGE,
            AppleStyle.SPACING_LARGE,
            AppleStyle.SPACING_LARGE,
            AppleStyle.SPACING_LARGE
        )
        self.main_layout.setSpacing(AppleStyle.SPACING_MEDIUM)

    def create_label(self, text, font_size=AppleStyle.FONT_SIZE_REGULAR, bold=False, color=None):
        """Create a label with Apple-style styling"""
        label = QLabel(text)
        font = QFont(AppleStyle.FONT_FAMILY, font_size)
        font.setWeight(QFont.Weight.DemiBold if bold else QFont.Weight.Normal)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        
        if color is None:
            color = AppleStyle.TEXT_PRIMARY if bold else AppleStyle.TEXT_SECONDARY
        
        label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                background-color: transparent;
                padding: {AppleStyle.SPACING_SMALL}px;
            }}
        """)
        return label

    def create_button(self, text, callback=None, primary=True):
        """Create a button with Apple-style design"""
        button = QPushButton(text)
        button.setMinimumHeight(50)
        button.setMinimumWidth(120)
        
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
                padding: {AppleStyle.SPACING_MEDIUM}px {AppleStyle.SPACING_LARGE}px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {hover_color};
            }}
            QPushButton:disabled {{
                background-color: {AppleStyle.BORDER};
                color: {AppleStyle.TEXT_SECONDARY};
            }}
        """)
        
        if callback:
            button.clicked.connect(callback)
        return button
