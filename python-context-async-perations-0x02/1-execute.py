#!/usr/bin/env python3
"""
Class-based context manager to execute a database query with automatic connection handling
"""

import sqlite3


class ExecuteQuery:
    """
    Custom context manager that executes a query with optional parameters
    """

    def __init__(self, db_name, query, params=None):
        """
        Initialize with database name, query, and optional parameters
        """
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """
        Open the connection, execute the query, and return the results
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close cursor and connection, handle exceptions if any
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        for row in results:
            print(row)
