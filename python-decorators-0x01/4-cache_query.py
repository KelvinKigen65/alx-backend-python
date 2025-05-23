import time
import sqlite3 
import functools

query_cache = {}

# Decorator to manage database connections
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open connection
        try:
            return func(conn, *args, **kwargs)  # Pass connection to function
        finally:
            conn.close()  # Ensure connection is closed after execution
    return wrapper

# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]  # Return cached result
        
        result = func(conn, query, *args, **kwargs)  # Execute function
        query_cache[query] = result  # Store result in cache
        return result

    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print(users_again)
