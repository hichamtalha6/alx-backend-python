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
            yield row[0]   # yield each age
        cursor.close()
        connection.close()


def average_age():
    """
    Calculate the average age using the generator
    without loading all rows into memory.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += float(age)
        count += 1
    return (total / count) if count > 0 else 0


if __name__ == "__main__":
    print("Streaming ages:")
    for i, age in enumerate(stream_user_ages(), 1):
        print(age)
        if i == 5:  # just show first 5 ages
            break

    print(f"\nAverage age: {average_age():.2f}")
