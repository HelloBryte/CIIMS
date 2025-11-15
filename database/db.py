import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import Error
from config import Config
from utils.logging_config import get_logger

logger = get_logger(__name__)

# Database configuration from Config class
DB_CONFIG = Config.get_db_config()

# Connection pool configuration
POOL_NAME = Config.DB_POOL_NAME
POOL_SIZE = Config.DB_POOL_SIZE

# Create connection pool
try:
    connection_pool = MySQLConnectionPool(
        pool_name=POOL_NAME, pool_size=POOL_SIZE, **DB_CONFIG
    )
    logger.info(
        "Database connection pool '%s' created successfully with %s connections",
        POOL_NAME,
        POOL_SIZE,
    )
except Error as e:
    logger.error("Failed to create connection pool: %s", e)
    connection_pool = None


def get_connection():
    """Get database connection from connection pool"""
    try:
        if connection_pool:
            return connection_pool.get_connection()
        else:
            # Fallback to direct connection
            return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        logger.error("Failed to get database connection: %s", e)
        raise
