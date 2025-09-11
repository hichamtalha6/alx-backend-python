#!/usr/bin/python3
import seed


def stream_user_ages():
    """
    Generator that yields ages of users one by one from user_data table.
    """
    connection = seed.connect_to_prodev()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield row[0]
        cursor.close()
        connection.close()
