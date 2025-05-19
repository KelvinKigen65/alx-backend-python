import mysql.connector
import csv

def connect_db():
    """Connect to the MySQL server."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",
            passwd="your_password"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()
    print("Database ALX_prodev created successfully!")

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",
            passwd="your_password",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Create the user_data table if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX(user_id)
        );
    """)
    cursor.close()
    print("Table user_data created successfully!")

def insert_data(connection, file_path):
    """Insert data from CSV into the database if it doesn't exist."""
    cursor = connection.cursor()
    
    # Read CSV file
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        
        for row in reader:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
            """, row)

    connection.commit()
    cursor.close()
    print("Data inserted successfully!")
