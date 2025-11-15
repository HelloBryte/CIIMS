"""
Database helper utilities for consistent error handling and resource management
"""

from contextlib import contextmanager
from database.db import get_connection
from mysql.connector import Error
from utils.logging_config import get_logger

logger = get_logger(__name__)


@contextmanager
def database_cursor(dictionary=False):
    """
    Context manager for database operations with automatic resource cleanup

    Args:
        dictionary: Return results as dictionary if True, tuple if False

    Yields:
        Database cursor for operations

    Example:
        with database_cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=dictionary)
        yield cursor
        conn.commit()
    except Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def execute_query(query, params=None, dictionary=False):
    """
    Execute a database query and return results

    Args:
        query: SQL query string
        params: Query parameters tuple
        dictionary: Return results as dictionary if True

    Returns:
        Query results
    """
    try:
        with database_cursor(dictionary=dictionary) as cursor:
            cursor.execute(query, params or ())
            if query.strip().upper().startswith(("SELECT", "SHOW", "DESCRIBE")):
                return cursor.fetchall()
            else:
                return cursor.lastrowid
    except Error as e:
        logger.error(f"Query execution failed: {query}, params: {params}, error: {e}")
        raise


def execute_many(query, params_list):
    """
    Execute multiple queries with different parameters

    Args:
        query: SQL query string
        params_list: List of parameter tuples

    Returns:
        Number of affected rows
    """
    try:
        with database_cursor() as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount
    except Error as e:
        logger.error(f"Batch execution failed: {query}, error: {e}")
        raise
