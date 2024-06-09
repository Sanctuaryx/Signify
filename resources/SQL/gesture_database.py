import sqlite3
import os

# Function to insert data into dynamic_gestures table
def insert_gesture(cursor, name, left_hand, right_hand):
    cursor.execute('''
    INSERT INTO gestures (name, left_hand, right_hand)
    VALUES (?, ?, ?)
    ''', (name, left_hand, right_hand))

def create_tables(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS gestures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        left_hand TEXT,
        right_hand TEXT
    )
    ''')
    
def setup_database():
               
    # Specify the directory where you want to store the database file
    database_dir = 'resources/SQL/int_dataBase'
    database_file = 'gestures.db'
    database_path = os.path.join(database_dir, database_file)
    
    os.makedirs(database_dir, exist_ok=True)
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    create_tables(cursor)
    
    conn.commit()
    conn.close()

    print(f"Database and tables created successfully at {database_path}.")
    
if __name__ == '__main__':
    setup_database()
 
