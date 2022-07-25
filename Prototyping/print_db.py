import sqlite3
import time

DATABASE_PATH = "prices.sqlite"

def db_connection(path: str):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except sqlite3.Error as e:
        print("Error:", e)
    return connection

connection = db_connection(DATABASE_PATH)
cur = connection.cursor()

for row in cur.execute("SELECT * FROM prices"):
    print(row)

time.sleep(20)

connection.close()