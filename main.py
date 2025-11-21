import sys
from PySide6.QtWidgets import QApplication
from ui.screens.login_window import LoginWindow
from utils.logging_config import setup_logging
from config import Config

# Setup logging
logger = setup_logging()
logger.info("Starting %s v%s", Config.APP_NAME, Config.APP_VERSION)

# Validate configuration
if not Config.validate_config():
    logger.error("Configuration validation failed. Exiting.")
    sys.exit(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
