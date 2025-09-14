#!/usr/bin/env python3
"""
Class-based context manager for handling database connections automatically
"""

import sqlite3


class DatabaseConnection:
    """
    A custom context manager for SQLite database connections
    """

    def __init__(self, db_name):
        """
        Initialize with the database name
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Open the database connection and return the cursor
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the database connection
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is None:
                # Commit only if no exception occurred
                self.conn.commit()
            else:
                # Rollback if an exception occurred
                self.conn.rollback()
            self.conn.close()


if __name__ == "__main__":
    # Example usage
    with DatabaseConnection("users.db") as cursor:
        cursor.execute("SELECT * FROM users;")
        results = cursor.fetchall()
        for row in results:
            print(row)
