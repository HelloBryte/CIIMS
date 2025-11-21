#!/usr/bin/env python3
"""
Generate diverse sample items for CIIMS database to improve AI assistant testing
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database_helper import execute_query


def generate_sample_items():
    """Generate diverse English items across multiple categories"""

    sample_items = [
        # Books & Reading Materials
        (
            "Introduction to Algorithms",
            "books",
            5,
            "Computer science textbook by Cormen",
        ),
        ("Data Structures and Algorithms", "textbooks", 3, "Essential CS textbook"),
        ("Clean Code", "books", 8, "Software engineering best practices"),
        (
            "The Pragmatic Programmer",
            "books",
            6,
            "Programming practices and methodologies",
        ),
        ("Python Crash Course", "books", 10, "Python programming for beginners"),
        ("Machine Learning Yearning", "reference", 4, "Andrew Ng's ML guide"),
        ("Deep Learning", "textbooks", 2, "Comprehensive deep learning textbook"),
        ("Algorithm Design Manual", "reference", 3, "Algorithm design and analysis"),
        # Electronics & Computers
        ("MacBook Pro 14-inch", "computers", 3, "Apple laptop for development"),
        ("Dell XPS 15", "computers", 4, "Windows laptop for students"),
        ("iPad Air", "electronics", 6, "Apple tablet for note-taking"),
        ("Surface Pro", "electronics", 5, "Microsoft tablet/laptop hybrid"),
        ("Logitech MX Master 3", "electronics", 8, "Wireless mouse for productivity"),
        ("Mechanical Keyboard", "electronics", 7, "RGB mechanical keyboard"),
        ("USB-C Hub", "electronics", 12, "Multi-port USB hub"),
        ('External Monitor 27"', "electronics", 4, "4K external display"),
        # Photography & Media
        ("Canon EOS R5", "photography", 2, "Professional mirrorless camera"),
        ("Sony A7 IV", "photography", 3, "Full-frame mirrorless camera"),
        ("Nikon D850", "photography", 2, "Professional DSLR camera"),
        ("GoPro Hero 11", "photography", 5, "Action camera for outdoor use"),
        ("DJI Mini 3 Pro", "photography", 3, "Compact drone for aerial photography"),
        ("Tripod Carbon Fiber", "photography", 6, "Lightweight camera tripod"),
        ("Ring Light", "photography", 8, "LED ring light for video calls"),
        # Lab Equipment & Tools
        (
            "Oscilloscope Digital",
            "equipment",
            2,
            "Digital oscilloscope for electronics",
        ),
        ("Multimeter", "tools", 10, "Digital multimeter for electrical testing"),
        ("Soldering Station", "tools", 4, "Temperature-controlled soldering iron"),
        ("Arduino Uno Kit", "equipment", 8, "Microcontroller development kit"),
        ("Raspberry Pi 4", "equipment", 12, "Single board computer"),
        ("3D Printer", "equipment", 3, "FDM 3D printer for prototyping"),
        ("Power Supply", "equipment", 5, "Variable DC power supply"),
        ("Logic Analyzer", "tools", 3, "Digital logic analyzer"),
        # Audio & Music
        ("Bose QuietComfort 45", "audio", 6, "Noise-cancelling headphones"),
        ("Sony WH-1000XM4", "audio", 5, "Wireless noise-cancelling headphones"),
        ("Audio-Technica M50x", "audio", 7, "Studio monitor headphones"),
        ("USB Microphone", "audio", 9, "Professional USB microphone"),
        ("MIDI Keyboard", "audio", 4, "25-key MIDI controller"),
        ("Portable Speaker", "audio", 8, "Bluetooth portable speaker"),
        # Sports & Recreation
        ("Yoga Mat Professional", "sports", 10, "Non-slip yoga mat"),
        ("Dumbbell Set 20lb", "sports", 6, "Adjustable dumbbell set"),
        ("Tennis Racket", "sports", 4, "Professional tennis racket"),
        ("Basketball", "sports", 8, "Official size basketball"),
        ("Camping Tent 4-person", "recreation", 3, "Four-person camping tent"),
        ("Sleeping Bag", "recreation", 5, "Cold weather sleeping bag"),
        # Office Supplies
        ("Standing Desk", "office", 3, "Electric height-adjustable desk"),
        ("Ergonomic Chair", "office", 5, "Office chair with lumbar support"),
        ("Whiteboard", "office", 7, "Mobile whiteboard with markers"),
        ("Projector 4K", "office", 2, "4K office projector"),
        ("Document Scanner", "office", 4, "High-speed document scanner"),
        # Gaming & Entertainment
        ("PlayStation 5", "gaming", 3, "Sony gaming console"),
        ("Xbox Series X", "gaming", 3, "Microsoft gaming console"),
        ("Nintendo Switch", "gaming", 5, "Hybrid gaming console"),
        ("VR Headset", "gaming", 4, "Virtual reality headset"),
        ("Gaming Chair", "gaming", 6, "Ergonomic gaming chair"),
    ]

    print(f"Generating {len(sample_items)} diverse sample items...")

    try:
        # Option 1: Clear existing items and their borrow records
        print("Clearing existing borrow records and items...")
        execute_query("DELETE FROM borrows", ())
        execute_query("DELETE FROM items", ())

        # Option 2: Alternatively, just insert new items without clearing (uncomment below)
        # print("Adding new sample items to existing inventory...")

        # Insert new sample items
        for item_name, category, quantity, remark in sample_items:
            execute_query(
                "INSERT INTO items (item_name, item_category, item_quantity, remark) VALUES (%s, %s, %s, %s)",
                (item_name, category, quantity, remark),
            )
            print(f"Added: {item_name} ({category}) - {quantity} units")

        print(f"\nSuccessfully generated {len(sample_items)} sample items!")

        # Verify insertion
        result = execute_query("SELECT COUNT(*) as count FROM items", dictionary=True)
        print(f"Total items in database: {result[0]['count']}")

    except Exception as e:
        print(f"Error generating sample items: {e}")
        return False

    return True


if __name__ == "__main__":
    print("CIIMS Sample Items Generator")
    print("=" * 40)

    success = generate_sample_items()

    if success:
        print("\n✅ Sample items generation completed!")
        print("\nNow you can test the AI assistant with queries like:")
        print("- 'I want to borrow books'")
        print("- 'Need a laptop for class'")
        print("- 'Looking for camera equipment'")
        print("- 'Show me lab tools'")
        print("- 'Available gaming equipment'")
    else:
        print("\n❌ Failed to generate sample items")
        sys.exit(1)
