import sqlite3

class ExecuteQuery:
    """Context manager for executing a parameterized SQL query."""
    
    def __init__(self, query, params):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Establish connection and execute the query."""
        self.connection = sqlite3.connect("example.db")  # Connect synchronously
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        """Handle cleanup: commit changes and close the connection."""
        self.connection.commit()  # Ensure any changes are saved
        self.cursor.close()
        self.connection.close()

query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as result:
    print("Users older than 25:", result)
