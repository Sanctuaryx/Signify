import sqlite3
import os

def insert_static_gesture(cursor, name, left_roll, right_roll, left_pitch, right_pitch, left_yaw, right_yaw, 
                          left_flexor_1, left_flexor_2, left_flexor_3, left_flexor_4, left_flexor_5,
                          right_flexor_1, right_flexor_2, right_flexor_3, right_flexor_4, right_flexor_5):
    cursor.execute('''
    INSERT INTO static_gestures (name, left_roll, right_roll, left_pitch, right_pitch, left_yaw, right_yaw, 
                                 left_flexor_1, left_flexor_2, left_flexor_3, left_flexor_4, left_flexor_5,
                                 right_flexor_1, right_flexor_2, right_flexor_3, right_flexor_4, right_flexor_5)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, left_roll, right_roll, left_pitch, right_pitch, left_yaw, right_yaw, 
          left_flexor_1, left_flexor_2, left_flexor_3, left_flexor_4, left_flexor_5,
          right_flexor_1, right_flexor_2, right_flexor_3, right_flexor_4, right_flexor_5))

# Function to insert data into dynamic_gestures table
def insert_dynamic_gesture(cursor, name, rolls, pitches, yaws, flexor1s, flexor2s, flexor3s, flexor4s, flexor5s):
    cursor.execute('''
    INSERT INTO dynamic_gestures (name, rolls, pitches, yaws, flexor1s, flexor2s, flexor3s, flexor4s, flexor5s)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, rolls, pitches, yaws, flexor1s, flexor2s, flexor3s, flexor4s, flexor5s))

def create_tables(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS static_gestures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        left_roll REAL,
        right_roll REAL,
        left_pitch REAL,
        right_pitch REAL,
        left_yaw REAL,
        right_yaw REAL,
        left_flexor_1 INTEGER,
        left_flexor_2 INTEGER,
        left_flexor_3 INTEGER,
        left_flexor_4 INTEGER,
        left_flexor_5 INTEGER,
        right_flexor_1 INTEGER,
        right_flexor_2 INTEGER,
        right_flexor_3 INTEGER,
        right_flexor_4 INTEGER,
        right_flexor_5 INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dynamic_gestures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rolls TEXT,
        pitches TEXT,
        yaws TEXT,
        flexor1s TEXT,
        flexor2s TEXT,
        flexor3s TEXT,
        flexor4s TEXT,
        flexor5s TEXT
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
 
