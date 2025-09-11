#!/usr/bin/python3
import mysql.connector


def stream_users():
    """Generator that yields rows one by one from user_data table."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # adjust if needed
            password="root",   # adjust if needed
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
