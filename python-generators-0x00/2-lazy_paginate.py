#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database.
    Returns a list of rows starting at offset with length page_size.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches each page from the database.
    Only fetches the next page when needed.
    Uses a single loop.
    """
    offset = 0
    while True:  # loop 1
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
