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
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt
from datetime import datetime
from database.db import get_connection
from ui.base_window import AppleStyle, AppleMessageDialog


class BorrowingRecordsWindow(QMainWindow):
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name
        self.user_id = None
        self.initUI()
        self.get_user_id()
        self.load_all_records()

    def initUI(self):
        self.setWindowTitle("My Borrowing Records")
        self.setFixedSize(1000, 600)

        # Main container
        container = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("My Borrowing Records")
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
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(
            [
                "Item Name",
                "Category",
                "Borrow Time",
                "Return Deadline",
                "Return Time",
                "Status",
                "Days Overdue",
            ]
        )

        # Set column widths
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Item Name
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Category
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Borrow Time
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Return Deadline
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Return Time
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Days Overdue

        return table

    def get_user_id(self):
        """Get user ID from username"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT user_id FROM users WHERE user_name=%s", (self.user_name,)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                self.user_id = user["user_id"]
            else:
                dialog = AppleMessageDialog(
                    self, "Error", "Failed to get user information", "error"
                )
                dialog.exec()
        except Exception as e:
            dialog = AppleMessageDialog(
                self, "Error", f"Database connection failed: {str(e)}", "error"
            )
            dialog.exec()

    def load_all_records(self):
        """Load all borrowing records for the user"""
        if not self.user_id:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Query all borrowing records with item details
            cursor.execute(
                """
                SELECT 
                    b.borrow_id,
                    b.item_id,
                    b.borrow_time,
                    b.return_deadline,
                    b.return_time,
                    b.return_status,
                    i.item_name,
                    i.item_category
                FROM borrows b
                JOIN items i ON b.item_id = i.item_id
                WHERE b.user_id = %s
                ORDER BY b.borrow_time DESC
            """,
                (self.user_id,),
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

            # Item Name
            table.setItem(row, 0, QTableWidgetItem(record["item_name"]))

            # Category
            table.setItem(row, 1, QTableWidgetItem(record["item_category"] or "N/A"))

            # Borrow Time
            borrow_time = record["borrow_time"]
            if isinstance(borrow_time, datetime):
                borrow_time_str = borrow_time.strftime("%Y-%m-%d %H:%M")
            else:
                borrow_time_str = str(borrow_time)
            table.setItem(row, 2, QTableWidgetItem(borrow_time_str))

            # Return Deadline
            deadline = record["return_deadline"]
            if isinstance(deadline, datetime):
                deadline_dt = deadline
                deadline_str = deadline.strftime("%Y-%m-%d")
            else:
                deadline_str = str(deadline)
                deadline_dt = datetime.strptime(str(deadline), "%Y-%m-%d %H:%M:%S")
            deadline_item = QTableWidgetItem(deadline_str)
            table.setItem(row, 3, deadline_item)

            # Return Time
            return_time = record["return_time"]
            if return_time:
                if isinstance(return_time, datetime):
                    return_time_str = return_time.strftime("%Y-%m-%d %H:%M")
                else:
                    return_time_str = str(return_time)
                table.setItem(row, 4, QTableWidgetItem(return_time_str))
            else:
                table.setItem(row, 4, QTableWidgetItem("N/A"))

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
            table.setItem(row, 5, status_item)

            # Days Overdue (only for overdue items)
            if status == "not_returned" and deadline_dt < current_time:
                days_overdue = (current_time - deadline_dt).days
                overdue_item = QTableWidgetItem(f"{days_overdue} days")
                overdue_item.setForeground(QColor(255, 0, 0))
                table.setItem(row, 6, overdue_item)
            else:
                table.setItem(row, 6, QTableWidgetItem("-"))
