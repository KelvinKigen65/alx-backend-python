#!/usr/bin/python3
seed = __import__('seed')

def paginate_users(page_size, offset):
    """Fetches a page of users with a given offset."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """Generator that lazily fetches paginated user data."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
