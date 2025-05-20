import MySQLdb

def stream_users_in_batches(batch_size):
    """Generator to fetch user records in batches."""
    conn = MySQLdb.connect(host="localhost", user="your_user", passwd="your_password", db="your_db")
    cursor = conn.cursor(dictionary=True)

    offset = 0
    while True:
        cursor.execute("SELECT id, name, age FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        batch = cursor.fetchall()

        if not batch:
            break  # Stop when no more rows are available

        yield batch
        offset += batch_size

    cursor.close()
    conn.close()

def batch_processing(batch_size):
    """Processes batches to filter users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        yield [user for user in batch if user['age'] > 25]  # Loop 2 (comprehension)

# Example usage:
batch_size = 50
for processed_batch in batch_processing(batch_size):  # Loop 3
    for user in processed_batch:
        print(user)
