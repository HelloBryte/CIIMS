"""
Logging configuration for the CIIMS application
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logging(log_level=logging.INFO, log_dir="logs"):
    """Setup logging configuration for the application"""

    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create log filename with timestamp
    log_filename = os.path.join(
        log_dir, f"ciims_{datetime.now().strftime('%Y%m%d')}.log"
    )

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                log_filename, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
            ),
            logging.StreamHandler(),  # Also output to console
        ],
    )

    # Set specific logger levels
    logging.getLogger("mysql.connector").setLevel(logging.WARNING)
    logging.getLogger("cv2").setLevel(logging.WARNING)

    return logging.getLogger(__name__)


def get_logger(name):
    """Get a logger instance with the specified name"""
    return logging.getLogger(name)
