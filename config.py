"""
Application configuration management
"""

import os
from dotenv import load_dotenv
from utils.logging_config import get_logger

# Load environment variables
load_dotenv()

logger = get_logger(__name__)


class Config:
    """Application configuration class"""

    # Database configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_DATABASE = os.getenv("DB_DATABASE", "campus_system")
    DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

    # Database pool configuration
    DB_POOL_NAME = "ciims_pool"
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))

    # Face recognition configuration
    FACE_RECOGNITION_MODEL_PATH = os.getenv(
        "FACE_RECOGNITION_MODEL_PATH", "model/trainer.yml"
    )
    FACE_RECOGNITION_HAAR_CASCADE_PATH = os.getenv(
        "FACE_RECOGNITION_HAAR_CASCADE_PATH", "haarcascade_frontalface_default.xml"
    )
    FACE_RECOGNITION_CONFIDENCE_THRESHOLD = float(
        os.getenv("FACE_RECOGNITION_CONFIDENCE_THRESHOLD", "50")
    )

    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", "10485760"))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

    # Application configuration
    APP_NAME = os.getenv("APP_NAME", "Campus Intelligent Inventory Management System")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

    # Security configuration
    PASSWORD_HASH_ROUNDS = int(os.getenv("PASSWORD_HASH_ROUNDS", "12"))

    @classmethod
    def get_db_config(cls):
        """Get database configuration as dictionary"""
        return {
            "host": cls.DB_HOST,
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD,
            "database": cls.DB_DATABASE,
            "charset": cls.DB_CHARSET,
        }

    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        errors = []

        # Validate database configuration
        if not cls.DB_HOST:
            errors.append("DB_HOST is required")
        if not cls.DB_USER:
            errors.append("DB_USER is required")
        if not cls.DB_DATABASE:
            errors.append("DB_DATABASE is required")

        # Validate face recognition model file
        if not os.path.exists(cls.FACE_RECOGNITION_MODEL_PATH):
            logger.warning(
                "Face recognition model file not found: %s",
                cls.FACE_RECOGNITION_MODEL_PATH,
            )

        # Skip Haar cascade validation for now (will be handled by face_recognition_utils)
        logger.info("Haar cascade file validation skipped (will be handled at runtime)")

        if errors:
            for error in errors:
                logger.error("Configuration validation error: %s", error)
            return False

        logger.info("Configuration validation passed")
        return True
