#!/usr/bin/python3
import mysql.connector


def stream_users_in_batches(batch_size):
    """Return a generator that yields users in batches of batch_size."""
    def generator():
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

            batch = []
            for row in cursor:  # loop 1
                batch.append(row)
                if len(batch) == batch_size:
                    yield batch
                    batch = []
            if batch:  # yield leftover
                yield batch

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    return generator()  # <- use return here


def batch_processing(batch_size):
    """
    Generator that processes each batch:
    - fetches users in batches
    - filters users over age 25
    - yields them one by one
    """
    for batch in stream_users_in_batches(batch_size):  # loop 2
        for user in batch:  # loop 3
            if int(user["age"]) > 25:
                yield user
