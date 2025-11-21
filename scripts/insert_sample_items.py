"""
Insert sample inventory items into the items table (English seed data).
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_connection

def insert_sample_items():
    """Insert sample inventory data"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sample inventory (English)
    sample_items = [
        # Books
        ("Python Crash Course", "Books", 10, "Beginner friendly Python guide"),
        ("Effective Java", "Books", 8, "Core Java reference"),
        ("Algorithms Unlocked", "Books", 5, "CS fundamentals"),
        ("Database System Concepts", "Books", 6, "Database theory"),
        ("Computer Networking", "Books", 7, "Networking essentials"),
        
        # Electronics
        ("Laptop (Dell XPS 15)", "Electronics", 3, "High performance dev laptop"),
        ("Projector", "Electronics", 5, "Classroom projector"),
        ("Wireless Mouse", "Electronics", 15, "Logitech wireless mouse"),
        ("Mechanical Keyboard", "Electronics", 12, "Programmer keyboard"),
        ("27in 4K Monitor", "Electronics", 4, "4K display"),
        
        # Sports
        ("Basketball", "Sports", 20, "Standard size 7 ball"),
        ("Soccer Ball", "Sports", 15, "Standard size 5 ball"),
        ("Badminton Racket", "Sports", 10, "YONEX racket"),
        ("Table Tennis Paddle", "Sports", 25, "Dual rubber paddle"),
        ("Jump Rope", "Sports", 30, "Counting jump rope"),
        
        # Lab gear
        ("Microscope", "Lab Equipment", 8, "Biology lab microscope"),
        ("Digital Scale", "Lab Equipment", 6, "Precision balance"),
        ("Beaker Set", "Lab Equipment", 20, "Glassware kit"),
        ("Test Tube Rack", "Lab Equipment", 15, "Standard rack"),
        ("Safety Goggles", "Lab Equipment", 50, "Protective eyewear"),
        
        # Office supplies
        ("A4 Paper Pack", "Office Supplies", 100, "500 sheets per pack"),
        ("Stapler", "Office Supplies", 30, "Standard stapler"),
        ("Document Folder", "Office Supplies", 80, "A4 multi-color folders"),
        ("Scientific Calculator", "Office Supplies", 25, "Scientific functions"),
        ("Mobile Whiteboard", "Office Supplies", 10, "Rolling whiteboard"),
    ]
    
    try:
        sql = """
            INSERT INTO items (item_name, item_category, item_quantity, remark)
            VALUES (%s, %s, %s, %s)
        """
        
        cursor.executemany(sql, sample_items)
        conn.commit()
        
        print(f"Inserted {len(sample_items)} sample items.")
        
        cursor.execute("SELECT item_id, item_name, item_category, item_quantity FROM items ORDER BY item_id")
        items = cursor.fetchall()
        print("\nCurrent items table snapshot:")
        print("-" * 80)
        print(f"{'ID':<5} {'Name':<30} {'Category':<18} {'Qty':<10}")
        print("-" * 80)
        for item in items:
            print(f"{item[0]:<5} {item[1]:<30} {item[2]:<18} {item[3]:<10}")
        
    except Exception as e:
        print(f"Failed to insert sample data: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    insert_sample_items()

