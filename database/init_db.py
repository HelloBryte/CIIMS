import mysql.connector
from mysql.connector import Error
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.security import hash_password
from config import Config

# Get database configuration
db_config = Config.get_db_config()
database_name = db_config["database"]

# Remove database-specific config for initial connection (to create database if needed)
init_config = {k: v for k, v in db_config.items() if k != "database"}

print(f"Connecting to MySQL server at {init_config['host']}...")
try:
    conn = mysql.connector.connect(**init_config)
    cursor = conn.cursor()
    print("✓ Connected to MySQL server successfully")
except Error as e:
    print(f"✗ Failed to connect to MySQL server: {e}")
    print("\nPlease check:")
    print("1. MySQL server is running")
    print("2. Database credentials in .env file are correct")
    print("3. MySQL user has proper permissions")
    sys.exit(1)

# Create database if it doesn't exist
print(f"\nCreating database '{database_name}' if it doesn't exist...")
try:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print(f"✓ Database '{database_name}' is ready")
except Error as e:
    print(f"✗ Failed to create database: {e}")
    cursor.close()
    conn.close()
    sys.exit(1)

# Use the database
cursor.execute(f"USE {database_name}")

# ========== set up table Users ==========
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(50) NOT NULL UNIQUE,
    user_password VARCHAR(255) NOT NULL,
    user_role ENUM('admin', 'user') NOT NULL,
    user_phone VARCHAR(20) NOT NULL,
    face_registered TINYINT(1)
);
"""
)

# Hash the admin password
admin_password_hash = hash_password("admin123")

cursor.execute(
    """
INSERT INTO users (user_name, user_password, user_role, user_phone)
VALUES ('admin', %s, 'admin', '13800138000')
ON DUPLICATE KEY UPDATE user_password = %s;
""",
    (admin_password_hash, admin_password_hash),
)

# ========== set up table items ==========
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    item_name VARCHAR(100) NOT NULL,
    item_category VARCHAR(50),
    item_quantity INT DEFAULT 0,
    remark TEXT
);
"""
)

# ========== set up table borrows ==========
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS borrows (
    borrow_id INT PRIMARY KEY AUTO_INCREMENT,
    item_id INT NOT NULL,
    user_id INT NOT NULL,
    borrow_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    return_deadline DATETIME NOT NULL,
    return_time DATETIME,
    return_status ENUM('not_returned', 'returned') NOT NULL DEFAULT 'not_returned',
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
"""
)

conn.commit()
cursor.close()
conn.close()
print("\n✓ Database initialization completed successfully!")
print(f"\nDefault admin account:")
print(f"  Username: admin")
print(f"  Password: admin123")
print(f"\n⚠️  IMPORTANT: Please change the admin password after first login!")
