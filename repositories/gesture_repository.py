from collections import defaultdict
import sqlite3
import numpy as np

class GestureRepository:
    """
    A class that represents a repository for storing and retrieving gesture data.

    Attributes:
        db_static_path (str): The path to the static gestures database file.
        db_dynamic_path (str): The path to the dynamic gestures database file.
    """

    def __init__(self, db_path='resources/SQL/int_dataBase/gestures.db'):
        """
        Initializes a new instance of the GestureRepository class.

        Args:
            db_static_path (str, optional): The path to the static gestures database file. Defaults to 'resources/SQL/int_dataBase/staticGestures.db'.
            db_dynamic_path (str, optional): The path to the dynamic gestures database file. Defaults to 'resources/SQL/int_dataBase/dynamicGestures.db'.
        """
        self._db_path = db_path
        self.dynamic_gestures = self._get_all_dynamic_gestures()
        self.static_gestures = self._get_all_static_gestures()
        self._num_key_frames = 5
    
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

    def _get_all_static_gestures(self):
        """
        Retrieves all static gestures from the database.

        Returns:
            list: A list of tuples representing the static gestures data.
        """
        try:
            attributes = [
            'id', 'name',
            'left_roll', 'right_roll',
            'left_pitch', 'right_pitch',
            'left_yaw', 'right_yaw',
            'left_flexor_1', 'right_flexor_1',
            'left_flexor_2', 'right_flexor_2',
            'left_flexor_3', 'right_flexor_3',
            'left_flexor_4', 'right_flexor_4',
            'left_flexor_5', 'right_flexor_5'
            ]
            
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM static_gestures")
            gestures_data = cursor.fetchall()
            conn.close()
            
            unpacked_values = map(dict(zip(attributes)), gestures_data)
            self.static_gestures = { attr: {unpacked[attr]: unpacked['name'] for unpacked in unpacked_values}for attr in attributes}
            print(f"Indexes: {self.static_gestures}")
        
        except Exception as e:
            print(f"Error retrieving static gestures: {e}")
            return None
    
    def _get_all_dynamic_gestures(self):
        """
        Retrieves all dynamic gestures from the database.

        Returns:
            list: A list of tuples representing the dynamic gestures data.
        """
        try:
            
            attributes = [
            'id', 'name',
            'left_roll', 'right_roll',
            'left_pitch', 'right_pitch',
            'left_yaw', 'right_yaw',
            'left_flexor_1', 'right_flexor_1',
            'left_flexor_2', 'right_flexor_2',
            'left_flexor_3', 'right_flexor_3',
            'left_flexor_4', 'right_flexor_4',
            'left_flexor_5', 'right_flexor_5'
            ]
            
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM dynamic_gestures")
            gestures_data = cursor.fetchall()
            conn.close()

            unpacked_values = map(dict(zip(attributes)), gestures_data)
            self.dynamic_gestures = { attr: {unpacked[attr]: unpacked['name'] for unpacked in unpacked_values} for attr in attributes}
            
        except Exception as e:
            print(f"Error retrieving dynamic gestures: {e}")
            return None

    def findClosestStaticSingleGestureByValue(self, left_euler, right_euler, left_flexor, right_flexor, tolerance = 10):
        """
        Retrieves the closest static gesture name based on the given Euler angles and flexor values.

        Args:
            euler (list): A list of Euler angles [roll, pitch, yaw].
            flexors (list): A list of flexor values for each finger [finger1, finger2, finger3, finger4, finger5].
            threshold (int, optional): The maximum distance threshold for a gesture to be considered a match. Defaults to 2.

        Returns:
            str or None: The name of the closest static gesture if it is within the threshold, None otherwise.
        """

        return [self.static_gestures.get(attribute, {}).get(value, None)]

        
        
    def findClosestStaticBothGestureByValue(self, left_euler, right_euler, left_flexor, right_flexor, tolerance = 10):
        """
        Retrieves the closest static gesture name based on the given Euler angles and flexor values.

        Args:
            euler (list): A list of Euler angles [roll, pitch, yaw].
            flexors (list): A list of flexor values for each finger [finger1, finger2, finger3, finger4, finger5].
            threshold (int, optional): The maximum distance threshold for a gesture to be considered a match. Defaults to 2.

        Returns:
            str or None: The name of the closest static gesture if it is within the threshold, None otherwise.
        """

        try:
                
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()

            query = '''
            SELECT name
            FROM static_gestures
            WHERE
            (left_roll BETWEEN ? AND ?) AND (left_pitch BETWEEN ? AND ?) AND (left_yaw BETWEEN ? AND ?) AND
            (left_flexor_1 BETWEEN ? AND ?) AND
            (left_flexor_2 BETWEEN ? AND ?) AND
            (left_flexor_3 BETWEEN ? AND ?) AND
            (left_flexor_4 BETWEEN ? AND ?) AND
            (left_flexor_5 BETWEEN ? AND ?) AND
            (right_roll BETWEEN ? AND ?) AND (right_pitch BETWEEN ? AND ?) AND (right_yaw BETWEEN ? AND ?) AND
            (right_flexor_1 BETWEEN ? AND ?) AND
            (right_flexor_2 BETWEEN ? AND ?) AND
            (right_flexor_3 BETWEEN ? AND ?) AND
            (right_flexor_4 BETWEEN ? AND ?) AND
            (right_flexor_5 BETWEEN ? AND ?)
            LIMIT 1
            '''
            values = (
                left_euler[0] - tolerance, left_euler[0] + tolerance,
                left_euler[1] - tolerance, left_euler[1] + tolerance,
                left_euler[2] - tolerance, left_euler[2] + tolerance,
                left_flexor[0] - tolerance, left_flexor[0] + tolerance,
                left_flexor[1] - tolerance, left_flexor[1] + tolerance,
                left_flexor[2] - tolerance, left_flexor[2] + tolerance,
                left_flexor[3] - tolerance, left_flexor[3] + tolerance,
                left_flexor[4] - tolerance, left_flexor[4] + tolerance,
                
                right_euler[0] - tolerance, right_euler[0] + tolerance,
                right_euler[1] - tolerance, right_euler[1] + tolerance,
                right_euler[2] - tolerance, right_euler[2] + tolerance,
                right_flexor[0] - tolerance, right_flexor[0] + tolerance,
                right_flexor[1] - tolerance, right_flexor[1] + tolerance,
                right_flexor[2] - tolerance, right_flexor[2] + tolerance,
                right_flexor[3] - tolerance, right_flexor[3] + tolerance,
                right_flexor[4] - tolerance, right_flexor[4] + tolerance
            )

            cursor.execute(query, values)
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result
            return None

        except Exception as e:
            return None
    
    def findClosestDynamicGesture(self, gesture_data, threshold=2):
        
        try:
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()

            key_data = self._extract_key_frames(gesture_data)
            values = []
            for frame in key_data:
                euler_angles, flexors = frame
                values.extend(euler_angles)
                values.extend(flexors)
            
            # Construct the SQL query for distance calculation
            query = '''
            SELECT name, rolls, pitches, yaws, flexor1s, flexor2s, flexor3s, flexor4s, flexor5s,
            FROM dynamic_gestures
            ORDER BY total_distance ASC
            LIMIT 1
            '''
            cursor.execute(query, values * 2)
            
            result = cursor.fetchone()
            
            conn.close()
            print(f'Result: {result} - result[1]: {result[1] if result else None} - result[1]: {result[0] if result else None}')
            if result and result[1] <= threshold:
                return result[0]
            return None
        
        except Exception as e:
            print(f"Error retrieving dynamic gesture: {e}")
            return None

