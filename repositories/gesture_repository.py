import sqlite3
import numpy as np

class GestureRepository:
    """
    A class that represents a repository for storing and retrieving gesture data.

    Attributes:
        db_static_path (str): The path to the static gestures database file.
        db_dynamic_path (str): The path to the dynamic gestures database file.
    """

    def __init__(self, db_static_path='resources/SQL/int_dataBase/staticGestures.db', db_dynamic_path='resources/SQL/int_dataBase/dynamicGestures.db'):
        """
        Initializes a new instance of the GestureRepository class.

        Args:
            db_static_path (str, optional): The path to the static gestures database file. Defaults to 'resources/SQL/int_dataBase/staticGestures.db'.
            db_dynamic_path (str, optional): The path to the dynamic gestures database file. Defaults to 'resources/SQL/int_dataBase/dynamicGestures.db'.
        """
        self._static_db_path = db_static_path
        self._dynamic_db_path = db_dynamic_path
        self._num_key_frames = 10
    
    def _extract_key_frames(self, gesture_data):
        """
        Extracts key frames from the given gesture data to reflect the main points of the movement.

        Args:
            gesture_data (list): A list of gesture data points.
            num_key_frames (int): The number of key frames to extract. Default is 5.

        Returns:
            list: A list of key frames extracted from the gesture data.

        Raises:
            None

        """
        if len(gesture_data) <= self._num_key_frames:
            return gesture_data
        
        gesture_data = [item[:2] for item in gesture_data]
        diffs = np.diff(gesture_data, axis=0)
        squared_diffs = np.sum(diffs ** 2, axis=2)
        total_diffs = np.sum(squared_diffs, axis=1)
        
        key_frame_indices = np.argsort(total_diffs)[-self._num_key_frames + 1:]
        key_frame_indices = np.sort(np.append([0], key_frame_indices))
        key_frames = [gesture_data[i] for i in key_frame_indices]
        
        return key_frames

    def get_all_static_gestures(self):
        """
        Retrieves all static gestures from the database.

        Returns:
            list: A list of tuples representing the static gestures data.
        """
        conn = sqlite3.connect(self._static_db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM static_gestures")
        gestures_data = cursor.fetchall()

        conn.close()
        return gestures_data
    
    def get_all_dynamic_gestures(self):
        """
        Retrieves all dynamic gestures from the database.

        Returns:
            list: A list of tuples representing the dynamic gestures data.
        """
        conn = sqlite3.connect(self._dynamic_db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM dynamic_gestures")
        gestures_data = cursor.fetchall()

        conn.close()
        return gestures_data

    def get_static_gesture_by_values(self, euler_izq, euler_der, flexor_izq, flexor_der, tolerance = 10):
        """
        Retrieves the closest static gesture name based on the given Euler angles and flexor values.

        Args:
            euler (list): A list of Euler angles [roll, pitch, yaw].
            flexors (list): A list of flexor values for each finger [finger1, finger2, finger3, finger4, finger5].
            threshold (int, optional): The maximum distance threshold for a gesture to be considered a match. Defaults to 2.

        Returns:
            str or None: The name of the closest static gesture if it is within the threshold, None otherwise.
        """
        conn = sqlite3.connect(self._static_db_path)
        cursor = conn.cursor()

        query = '''
        SELECT name
        FROM gestures
        WHERE
        (izq_yaw BETWEEN ? AND ?) AND (izq_pitch BETWEEN ? AND ?) AND (izq_roll BETWEEN ? AND ?) AND
        (flexor_izq_1 BETWEEN ? AND ?) AND
        (flexor_izq_2 BETWEEN ? AND ?) AND
        (flexor_izq_3 BETWEEN ? AND ?) AND
        (flexor_izq_4 BETWEEN ? AND ?) AND
        (flexor_izq_5 BETWEEN ? AND ?) AND
        (der_yaw BETWEEN ? AND ?) AND (der_pitch BETWEEN ? AND ?) AND (der_roll BETWEEN ? AND ?) AND
        (flexor_der_1 BETWEEN ? AND ?) AND
        (flexor_der_2 BETWEEN ? AND ?) AND
        (flexor_der_3 BETWEEN ? AND ?) AND
        (flexor_der_4 BETWEEN ? AND ?) AND
        (flexor_der_5 BETWEEN ? AND ?)
        LIMIT 1
        '''
        values = (
            euler_izq[0] - tolerance, euler_izq[0] + tolerance,
            euler_izq[1] - tolerance, euler_izq[1] + tolerance,
            euler_izq[2] - tolerance, euler_izq[2] + tolerance,
            flexor_izq[0] - tolerance, flexor_izq[0] + tolerance,
            flexor_izq[1] - tolerance, flexor_izq[1] + tolerance,
            flexor_izq[2] - tolerance, flexor_izq[2] + tolerance,
            flexor_izq[3] - tolerance, flexor_izq[3] + tolerance,
            flexor_izq[4] - tolerance, flexor_izq[4] + tolerance,
            
            euler_der[0] - tolerance, euler_der[0] + tolerance,
            euler_der[1] - tolerance, euler_der[1] + tolerance,
            euler_der[2] - tolerance, euler_der[2] + tolerance,
            flexor_der[0] - tolerance, flexor_der[0] + tolerance,
            flexor_der[1] - tolerance, flexor_der[1] + tolerance,
            flexor_der[2] - tolerance, flexor_der[2] + tolerance,
            flexor_der[3] - tolerance, flexor_der[3] + tolerance,
            flexor_der[4] - tolerance, flexor_der[4] + tolerance
        )

        cursor.execute(query, values)
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result
        return None
    
    def get_dynamic_gesture_by_values(self, gesture_data, threshold=2):
        
        conn = sqlite3.connect(self._static_db_path)
        cursor = conn.cursor()

        key_data = self._extract_key_frames(gesture_data)
        values = []
        for frame in key_data:
            euler_angles, flexors = frame
            values.extend(euler_angles)
            values.extend(flexors)
        
        # Construct the SQL query for distance calculation
        query = '''
        SELECT name, rolls, pitchs, yaws, flexor1s, flexor2s, flexor3s, flexor4s, flexor5s,
        FROM dynamic_gestures
        ORDER BY total_distance ASC
        LIMIT 1
        '''
        
        cursor.execute(query, values * 2)
        
        result = cursor.fetchone()
        
        conn.close()
        
        if result and result[1] <= threshold:
            return result[0]
        return None

