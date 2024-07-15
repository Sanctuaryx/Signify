import sqlite3
import os

# Function to insert data into hands table
def insert_hand(cursor, roll, pitch, yaw, finger1, finger2, finger3, finger4, finger5, mean_acceleration, std_acceleration, mean_angular_velocity, std_angular_velocity, gyro_axis, accel_axis):
    cursor.execute('''
    INSERT INTO hands (roll, pitch, yaw, finger1, finger2, finger3, finger4, finger5, mean_acceleration, std_acceleration, mean_angular_velocity, std_angular_velocity, gyro_axis, accel_axis)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (roll, pitch, yaw, finger1, finger2, finger3, finger4, finger5, mean_acceleration, std_acceleration, mean_angular_velocity, std_angular_velocity, gyro_axis, accel_axis))
    return cursor.lastrowid

# Function to insert data into gestures table
def insert_gesture(cursor, name, left_hand_id, right_hand_id):
    cursor.execute('''
    INSERT INTO gestures (name, left_hand_id, right_hand_id)
    VALUES (?, ?, ?)
    ''', (name, left_hand_id, right_hand_id))

def create_tables(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll REAL,
        pitch REAL,
        yaw REAL,
        finger1 INTEGER,
        finger2 INTEGER,
        finger3 INTEGER,
        finger4 INTEGER,
        finger5 INTEGER,
        mean_acceleration REAL,
        std_acceleration REAL,
        mean_angular_velocity REAL,
        std_angular_velocity REAL,
        gyro_axis INTEGER,
        accel_axis INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS gestures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        left_hand_id INTEGER,
        right_hand_id INTEGER,
        FOREIGN KEY (left_hand_id) REFERENCES hands(id),
        FOREIGN KEY (right_hand_id) REFERENCES hands(id)
    )
    ''')
    
def setup_data():
    return [
        {
            "name": "A",
            "left_hand": None,
            "right_hand": (82.0, -78.5, 97.5, 54, 16, 28, 106, 160, 0.0, 0.0, 0.0, 0.0, 0, 0)
        },
        
        {
            "name": "R",
            "left_hand": None,
            "right_hand": (96.0, -73.5, 120.0, 800, 700, 16, 52, 210, 0.0, 0.0, 0.0, 0.0, 0, 0)
        },
        
        {
            "name": "U",
            "left_hand": None,
            "right_hand": (154.0, -42, 104, 887, 890, 16, 95, 210, 0.0, 0.0, 0.0, 0.0, 0, 0)
        },
        
        {
            "name": "L",
            "left_hand": None,
            "right_hand": (98.12, -72.87, 131.94, 119, 18, 19, 40, 158, 0.0, 0.0, 0.0, 0.0, 0, 0)
        },
        
        {
            "name": "BUENOS",
            "left_hand": None,
            "right_hand": (344.44, -10.88, 70.25, 891, 893, 890, 893, 159, 0.0, 0.0, 0.0, 0.0, 0, 0)
        },
        
        
        {
            "name": "SOY",
            "left_hand": None,
            "right_hand": (333.69,-23.25,97.31, 469,13,13,64,214, 0.0, 0.0, 0.0, 0.0, 0, 0)
        },
        
        {
            "name": "DIAS",
            "left_hand": (179.56,-12.06,0.94, 40,887,26,52,196, 0.0, 0.0, 0.0, 0.0, 0, 0),
            "right_hand": (31.44,-7.06,18.62, 887,19,14,92,206, 0.0, 0.0, 0.0, 0.0, 0, 0)
        }
    ]

def setup_database():
    # Specify the directory where you want to store the database file
    database_dir = 'resources/SQL/int_dataBase'
    database_file = 'gestures.db'
    database_path = os.path.join(database_dir, database_file)
    
    os.makedirs(database_dir, exist_ok=True)
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    create_tables(cursor)
    data = setup_data()
    
    for row in data:
        name = row["name"]
        left_hand_data = row["left_hand"]
        right_hand_data = row["right_hand"]
        
        left_hand_id = insert_hand(cursor, *left_hand_data) if left_hand_data else None
        right_hand_id = insert_hand(cursor, *right_hand_data) if right_hand_data else None
        
        insert_gesture(cursor, name, left_hand_id, right_hand_id)
        print(f"Inserted data for gesture {name} successfully.")
        
    cursor.execute("SELECT * FROM gestures g LEFT JOIN hands lh ON g.left_hand_id = lh.id LEFT JOIN hands rh ON g.right_hand_id = rh.id")
    
    conn.commit()
    conn.close()

    print(f"Database and tables created successfully at {database_path}.")

if __name__ == '__main__':
    setup_database()
