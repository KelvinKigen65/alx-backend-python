

import mysql.connector

def stream_users():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Kelvin@6580",
        database="your_database"
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    db.close()

