from PySide6.QtWidgets import (
    QLineEdit,
    QHBoxLayout,
    QApplication,
    QLabel,
    QDialog,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import QThread, Signal, QObject, Qt
from PySide6.QtGui import QImage, QPixmap
from database.db import get_connection
from utils.security import verify_password
from utils.database_helper import execute_query
from utils.logging_config import get_logger

# recognize_face is no longer used directly, we do recognition in thread
from ui.RegisterWindow import RegisterWindow
from ui.MainWindow import MainWindow
from ui.base_window import BaseWindow, AppleStyle
import cv2
import numpy as np

logger = get_logger(__name__)


class FaceRecognitionThread(QThread):
    """Thread for face recognition to prevent blocking UI and crashes"""

    finished = Signal(str, str)  # name, message
    frame_ready = Signal(np.ndarray)  # frame for preview

    def run(self):
        """Run face recognition in separate thread"""
        name = ""
        msg = ""
        cap = None
        recognized = False
        try:
            # Open camera
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                cap = cv2.VideoCapture(1)
            if not cap.isOpened():
                self.finished.emit("", "Unable to open camera")
                return

            # Import here to avoid circular import
            from face_recognition.face_recognition_utils import (
                get_cached_recognizer,
                get_cached_user_map,
            )

            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )

            recognizer = get_cached_recognizer()
            if recognizer is None:
                self.finished.emit("", "Failed to load face recognition model")
                return

            user_map = get_cached_user_map()
            if not user_map:
                self.finished.emit("", "No registered face data found")
                return

            import time

            start_time = time.time()

            while True:
                ret, frame = cap.read()
                if not ret or frame is None:
                    continue

                # Emit frame for preview (main thread will display it)
                self.frame_ready.emit(frame.copy())

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                recognized = False
                for x, y, w, h in faces:
                    if x < 0 or y < 0 or x + w > gray.shape[1] or y + h > gray.shape[0]:
                        continue

                    try:
                        face_roi = gray[y : y + h, x : x + w]
                        if face_roi.size == 0:
                            continue

                        id, confidence = recognizer.predict(face_roi)
                        if confidence < 70:
                            name = user_map.get(id, "Unknown")
                            if name != "Unknown":
                                recognized = True
                                break
                    except Exception as e:
                        logger.warning(f"Recognition error: {e}")
                        continue

                if recognized:
                    self.finished.emit(name, "Face recognition successful")
                    break

                # 30 second timeout
                if time.time() - start_time > 30:
                    self.finished.emit("", "Recognition timeout, please try again")
                    break

        except SystemExit:
            raise
        except Exception as e:
            logger.error(f"Face recognition thread error: {e}", exc_info=True)
            self.finished.emit("", f"Face recognition error: {str(e)}")
        finally:
            if cap:
                try:
                    cap.release()
                except:
                    pass
            # Emit signal if not already emitted (for errors or timeout)
            if not recognized and name == "" and msg == "":
                self.finished.emit("", "Recognition failed, please try again")


class LoginWindow(BaseWindow):
    def __init__(self):
        super().__init__("CIIMS - Login", (480, 720))
        self.setup_login_ui()

    def setup_login_ui(self):
        """Setup login-specific UI components with Apple-style design"""
        # Clear main layout
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(0)

        # Add top spacer
        self.main_layout.addStretch()

        # Create card container
        card = self.create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(0)  # We'll add spacing manually

        # Title section
        title = QLabel("CIIMS")
        title.setStyleSheet(
            f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                background-color: transparent;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_LARGE}px;
                font-weight: 700;
                padding: 20px 0px;
            }}
        """
        )
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(False)
        title.setMinimumHeight(50)
        title.setMaximumHeight(80)
        card_layout.addWidget(title)

        # Add spacing after title
        card_layout.addSpacing(12)

        # Subtitle section
        subtitle = QLabel("Campus Intelligent Inventory\nManagement System")
        subtitle.setStyleSheet(
            f"""
            QLabel {{
                color: {AppleStyle.TEXT_SECONDARY};
                background-color: transparent;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_SMALL}px;
                font-weight: 400;
                padding: 0px 20px;
            }}
        """
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setMinimumHeight(50)
        subtitle.setMaximumHeight(80)
        card_layout.addWidget(subtitle)

        # Add large spacing after subtitle
        card_layout.addSpacing(32)

        # Username input
        self.input_username = self.create_input_field("Username")
        card_layout.addWidget(self.input_username)
        card_layout.addSpacing(20)

        # Password input
        self.input_password = self.create_input_field("Password", password=True)
        card_layout.addWidget(self.input_password)
        card_layout.addSpacing(32)

        # Sign In button
        self.btn_login = self.create_button("Sign In", self.do_login, primary=True)
        card_layout.addWidget(self.btn_login)
        card_layout.addSpacing(32)

        # Divider
        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background-color: {AppleStyle.BORDER};")
        card_layout.addWidget(divider)
        card_layout.addSpacing(32)

        # Create Account button
        self.btn_register = QPushButton("Create Account")
        self.btn_register.setMinimumHeight(50)
        self.btn_register.clicked.connect(self.open_register)
        self.btn_register.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                color: {AppleStyle.PRIMARY};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 600;
                padding: 14px 24px;
            }}
            QPushButton:hover {{
                background-color: {AppleStyle.BACKGROUND};
                border: 1px solid {AppleStyle.PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: {AppleStyle.BACKGROUND};
            }}
        """
        )
        card_layout.addWidget(self.btn_register)
        card_layout.addSpacing(20)

        # Face ID button
        self.btn_face_login = QPushButton("Face ID")
        self.btn_face_login.setMinimumHeight(50)
        self.btn_face_login.clicked.connect(self.face_login)
        self.btn_face_login.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {AppleStyle.CARD_BACKGROUND};
                color: {AppleStyle.PRIMARY};
                border: 1px solid {AppleStyle.BORDER};
                border-radius: {AppleStyle.RADIUS_MEDIUM}px;
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                font-weight: 600;
                padding: 14px 24px;
            }}
            QPushButton:hover {{
                background-color: {AppleStyle.BACKGROUND};
                border: 1px solid {AppleStyle.PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: {AppleStyle.BACKGROUND};
            }}
        """
        )
        card_layout.addWidget(self.btn_face_login)

        # Add card to main layout
        self.main_layout.addWidget(card)

        # Add bottom spacer
        self.main_layout.addStretch()

    def do_login(self):
        """Execute login with username and password"""
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            self.show_warning_message("Notice", "Username and password cannot be empty")
            return

        try:
            # Query database using helper
            sql = "SELECT * FROM users WHERE user_name=%s"
            users = execute_query(sql, (username,), dictionary=True)

            if users and len(users) > 0:
                user = users[0]
                if verify_password(password, user["user_password"]):
                    self.show_info_message("Success", f"Welcome {user['user_name']}!")
                    # Open main window
                    self.main_window = MainWindow(user["user_name"], user["user_role"])
                    self.main_window.show()
                    self.close()  # Close login window after successful login
                else:
                    self.show_error_message("Failed", "Incorrect username or password")
            else:
                self.show_error_message("Failed", "Incorrect username or password")

        except Exception as e:
            self.show_error_message("Error", f"Database error occurred: {str(e)}")

    def open_register(self):
        """Open registration window"""
        self.register_window = RegisterWindow()
        self.register_window.show()

    def face_login(self):
        """Face recognition login"""
        # Show permission warning first on macOS
        import platform

        if platform.system() == "Darwin":
            from ui.base_window import AppleConfirmDialog
            dialog = AppleConfirmDialog(
                self,
                "Camera Permission",
                "Face recognition requires camera permission.\n\n"
                "If this is the first time using this feature, the system may request permission.\n"
                "Please ensure camera permission is granted in system settings.\n\n"
                "Path: System Settings > Privacy & Security > Camera\n\n"
                "Continue?"
            )
            if dialog.exec() != QDialog.Accepted:
                return

        # Disable button to prevent multiple clicks
        self.btn_face_login.setEnabled(False)
        self.btn_face_login.setText("Recognizing...")

        # Create preview window with Apple-style design
        self.preview_window = QDialog(self)
        self.preview_window.setWindowTitle("Face Recognition")
        self.preview_window.setMinimumSize(640, 480)
        self.preview_window.setStyleSheet(
            f"""
            QDialog {{
                background-color: {AppleStyle.BACKGROUND};
            }}
        """
        )
        layout = QVBoxLayout()
        layout.setContentsMargins(
            AppleStyle.SPACING_LARGE,
            AppleStyle.SPACING_LARGE,
            AppleStyle.SPACING_LARGE,
            AppleStyle.SPACING_LARGE,
        )

        # Title
        title_label = QLabel("Please face the camera")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(
            f"""
            QLabel {{
                color: {AppleStyle.TEXT_PRIMARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_MEDIUM}px;
                font-weight: 600;
                padding: {AppleStyle.SPACING_MEDIUM}px;
            }}
        """
        )
        layout.addWidget(title_label)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setText("Starting camera...")
        self.preview_label.setStyleSheet(
            f"""
            QLabel {{
                color: {AppleStyle.TEXT_SECONDARY};
                font-family: {AppleStyle.FONT_FAMILY};
                font-size: {AppleStyle.FONT_SIZE_REGULAR}px;
                background-color: {AppleStyle.CARD_BACKGROUND};
                border-radius: {AppleStyle.RADIUS_LARGE}px;
                padding: {AppleStyle.SPACING_LARGE}px;
            }}
        """
        )
        layout.addWidget(self.preview_label)
        self.preview_window.setLayout(layout)
        self.preview_window.show()

        # Create and start thread
        self.face_thread = FaceRecognitionThread()
        self.face_thread.finished.connect(self.on_face_recognition_finished)
        self.face_thread.frame_ready.connect(self.update_preview)
        self.face_thread.start()

    def update_preview(self, frame):
        """Update preview window with camera frame"""
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(
                rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qt_image)
            # Scale to fit label while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.preview_label.setPixmap(scaled_pixmap)
        except Exception as e:
            logger.error(f"Error updating preview: {e}")

    def on_face_recognition_finished(self, name, msg):
        """Handle face recognition result"""
        # Close preview window
        if hasattr(self, "preview_window"):
            try:
                self.preview_window.close()
            except:
                pass

        # Re-enable button
        self.btn_face_login.setEnabled(True)
        self.btn_face_login.setText("Face Login")

        if name:
            from ui.base_window import AppleMessageDialog
            dialog = AppleMessageDialog(self, "Success", f"Welcome {name}!", "info")
            dialog.exec()
            try:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT user_role FROM users WHERE user_name=%s", (name,)
                )
                row = cursor.fetchone()
                cursor.close()
                conn.close()

                if row:
                    user_role = row["user_role"]
                else:
                    user_role = "user"  # Default to regular user

                # Open main window
                self.main_window = MainWindow(name, user_role)
                self.main_window.show()

                self.close()  # Close login window
            except Exception as e:
                self.show_error_message(
                    "Database Error", f"Failed to get user information: {str(e)}"
                )
        else:
            from ui.base_window import AppleMessageDialog
            dialog = AppleMessageDialog(self, "Recognition Failed", msg, "warning")
            dialog.exec()
