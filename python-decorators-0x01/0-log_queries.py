import sqlite3
import functools
from datetime import datetime



def log_queries(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Executing SQL Query: {query}") 
        return func(query, *args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


users = fetch_all_users(query="SELECT * FROM users")
