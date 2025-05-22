import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)

cursor = conn.cursor()

# Fetch data from your table
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()

conn.close()

print(results)
