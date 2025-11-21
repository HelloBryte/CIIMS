from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QTabWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from datetime import datetime
from database.db import get_connection
from ui.base import AppleStyle, AppleMessageDialog


class AllBorrowsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_all_records()

    def initUI(self):
        self.setWindowTitle("All Borrowing Records")
        self.setFixedSize(1200, 700)

        # Main container
        container = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("All Borrowing Records")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Tab widget for different views
        self.tabs = QTabWidget()

        # Tab 1: All Records
        self.tab_all = QWidget()
        self.table_all = self.create_table()
        tab_all_layout = QVBoxLayout()
        tab_all_layout.addWidget(self.table_all)
        self.tab_all.setLayout(tab_all_layout)
        self.tabs.addTab(self.tab_all, "All Records")

        # Tab 2: Not Returned
        self.tab_not_returned = QWidget()
        self.table_not_returned = self.create_table()
        tab_not_returned_layout = QVBoxLayout()
        tab_not_returned_layout.addWidget(self.table_not_returned)
        self.tab_not_returned.setLayout(tab_not_returned_layout)
        self.tabs.addTab(self.tab_not_returned, "Not Returned")

        # Tab 3: Returned
        self.tab_returned = QWidget()
        self.table_returned = self.create_table()
        tab_returned_layout = QVBoxLayout()
        tab_returned_layout.addWidget(self.table_returned)
        self.tab_returned.setLayout(tab_returned_layout)
        self.tabs.addTab(self.tab_returned, "Returned")

        # Tab 4: Overdue
        self.tab_overdue = QWidget()
        self.table_overdue = self.create_table()
        tab_overdue_layout = QVBoxLayout()
        tab_overdue_layout.addWidget(self.table_overdue)
        self.tab_overdue.setLayout(tab_overdue_layout)
        self.tabs.addTab(self.tab_overdue, "Overdue")

        layout.addWidget(self.tabs)

        # Button area
        btn_layout = QHBoxLayout()

        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.clicked.connect(self.load_all_records)
        btn_layout.addWidget(self.btn_refresh)

        self.btn_close = QPushButton("Close")
        self.btn_close.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_close)

        layout.addLayout(btn_layout)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_table(self):
        """Create a table widget with standard columns"""
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(
            [
                "Borrow ID",
                "User",
                "Item Name",
                "Category",
                "Borrow Time",
                "Return Deadline",
                "Return Time",
                "Status",
            ]
        )

        # Set column widths
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Borrow ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # User
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Item Name
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Category
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Borrow Time
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Return Deadline
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Return Time
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Status

        return table

    def load_all_records(self):
        """Load all borrowing records from all users"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Query all borrowing records with user and item details
            cursor.execute(
                """
                SELECT 
                    b.borrow_id,
                    b.user_id,
                    b.borrow_time,
                    b.return_deadline,
                    b.return_time,
                    b.return_status,
                    u.user_name,
                    i.item_name,
                    i.item_category
                FROM borrows b
                JOIN users u ON b.user_id = u.user_id
                JOIN items i ON b.item_id = i.item_id
                ORDER BY b.borrow_time DESC
            """
            )

            all_records = cursor.fetchall()
            cursor.close()
            conn.close()

            # Separate records by status
            not_returned_records = []
            returned_records = []
            overdue_records = []

            current_time = datetime.now()

            for record in all_records:
                deadline = record["return_deadline"]
                if isinstance(deadline, datetime):
                    deadline_dt = deadline
                else:
                    deadline_dt = datetime.strptime(str(deadline), "%Y-%m-%d %H:%M:%S")

                if record["return_status"] == "returned":
                    returned_records.append(record)
                elif record["return_status"] == "not_returned":
                    not_returned_records.append(record)
                    # Check if overdue
                    if deadline_dt < current_time:
                        overdue_records.append(record)

            # Populate tables
            self.populate_table(self.table_all, all_records)
            self.populate_table(self.table_not_returned, not_returned_records)
            self.populate_table(self.table_returned, returned_records)
            self.populate_table(self.table_overdue, overdue_records)

            # Update tab labels with counts
            self.tabs.setTabText(0, f"All Records ({len(all_records)})")
            self.tabs.setTabText(1, f"Not Returned ({len(not_returned_records)})")
            self.tabs.setTabText(2, f"Returned ({len(returned_records)})")
            self.tabs.setTabText(3, f"Overdue ({len(overdue_records)})")

        except Exception as e:
            dialog = AppleMessageDialog(
                self, "Error", f"Failed to load records: {str(e)}", "error"
            )
            dialog.exec()

    def populate_table(self, table, records):
        """Populate a table with records"""
        table.setRowCount(0)

        if not records:
            return

        current_time = datetime.now()

        for row, record in enumerate(records):
            table.insertRow(row)

            # Borrow ID
            table.setItem(row, 0, QTableWidgetItem(str(record["borrow_id"])))

            # User
            table.setItem(row, 1, QTableWidgetItem(record["user_name"]))

            # Item Name
            table.setItem(row, 2, QTableWidgetItem(record["item_name"]))

            # Category
            table.setItem(row, 3, QTableWidgetItem(record["item_category"] or "N/A"))

            # Borrow Time
            borrow_time = record["borrow_time"]
            if isinstance(borrow_time, datetime):
                borrow_time_str = borrow_time.strftime("%Y-%m-%d %H:%M")
            else:
                borrow_time_str = str(borrow_time)
            table.setItem(row, 4, QTableWidgetItem(borrow_time_str))

            # Return Deadline
            deadline = record["return_deadline"]
            if isinstance(deadline, datetime):
                deadline_dt = deadline
                deadline_str = deadline.strftime("%Y-%m-%d")
            else:
                deadline_str = str(deadline)
                deadline_dt = datetime.strptime(str(deadline), "%Y-%m-%d %H:%M:%S")
            deadline_item = QTableWidgetItem(deadline_str)
            table.setItem(row, 5, deadline_item)

            # Return Time
            return_time = record["return_time"]
            if return_time:
                if isinstance(return_time, datetime):
                    return_time_str = return_time.strftime("%Y-%m-%d %H:%M")
                else:
                    return_time_str = str(return_time)
                table.setItem(row, 6, QTableWidgetItem(return_time_str))
            else:
                table.setItem(row, 6, QTableWidgetItem("N/A"))

            # Status
            status = record["return_status"]
            if status == "returned":
                status_item = QTableWidgetItem("Returned")
                status_item.setForeground(QColor(0, 128, 0))  # Green
            else:
                # Check if overdue
                if deadline_dt < current_time:
                    status_item = QTableWidgetItem("Overdue")
                    status_item.setForeground(QColor(255, 0, 0))  # Red
                    # Also highlight the deadline
                    deadline_item.setForeground(QColor(255, 0, 0))
                else:
                    status_item = QTableWidgetItem("Not Returned")
                    status_item.setForeground(QColor(255, 165, 0))  # Orange
            table.setItem(row, 7, status_item)
