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

# Decorator to manage transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # Execute function
            conn.commit()  # Commit if successful
            return result
        except Exception as e:
            conn.rollback()  # Rollback on error
            print(f"Transaction failed: {e}")
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
