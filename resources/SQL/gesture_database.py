import sqlite3
import os

# Specify the directory where you want to store the database file
database_dir = 'resources/SQL/int_dataBase'
database_file = 'gestures.db'
database_path = os.path.join(database_dir, database_file)

# Ensure the directory exists
os.makedirs(database_dir, exist_ok=True)

# Connect to the SQLite database (this will create the database file if it doesn't exist)
conn = sqlite3.connect(database_path)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create tables for static and dynamic gestures
cursor.execute('''
CREATE TABLE IF NOT EXISTS static_gestures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll REAL,
    pitch REAL,
    yaw REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dynamic_gestures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gesture_data BLOB
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Database and tables created successfully at {database_path}.")
