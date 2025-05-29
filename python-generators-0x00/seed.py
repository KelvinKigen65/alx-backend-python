import MySQLdb

def stream_users_in_batches(batch_size):
   
    conn = MySQLdb.connect(host="localhost", user="root", passwd="Kelvin@6580", db="your_db")
    cursor = conn.cursor(dictionary=True)

    offset = 0
    while True:
        cursor.execute("SELECT id, name, age FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        batch = cursor.fetchall()

        if not batch:
            break

        yield batch
        offset += batch_size

    cursor.close()
    conn.close()

def batch_processing(batch_size):

    for batch in stream_users_in_batches(batch_size):
        yield (user for user in batch if user['age'] > 25)

# Example usage
batch_size = 50
for processed_batch in batch_processing(batch_size):
    for user in processed_batch:
        print(user)
