#!/usr/bin/python3
import seed


def stream_user_ages(connection):
    """
    Generator that streams user ages one by one from the user_data table.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row[0]   # only return the age
    cursor.close()


if __name__ == "__main__":
    connection = seed.connect_to_prodev()
    if connection:
        for age in stream_user_ages(connection):
            print(age)
        connection.close()
