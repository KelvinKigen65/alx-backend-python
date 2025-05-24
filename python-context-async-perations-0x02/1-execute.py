
import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)  # Open connection
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)  # Execute query
        return self.cursor.fetchall()  # Return query results

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()  # Ensure connection is closed
        if exc_type:
            print(f"An error occurred: {exc_value}")  # Handle errors

# Query users older than 25
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("users.db", query, params) as results:
    for row in results:
        print(row)
