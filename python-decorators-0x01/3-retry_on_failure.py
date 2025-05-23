import time
import sqlite3 
import functools

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

# Decorator to retry a function on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)  # Execute function
                except sqlite3.OperationalError as e:  # Catch transient DB errors
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)  # Wait before retrying
            raise Exception("Function failed after maximum retries")
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
