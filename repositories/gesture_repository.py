import sqlite3
import numpy as np
from scipy.spatial import KDTree
import classes.gesture as Gesture
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
        self.gesture_tree, self.gesture_names = self._get_all_gestures()
        print('Gesture repository initialized successfully.')

    def _get_all_gestures(self):
        """
        Retrieves all static gestures from the database.

        Returns:
            list: A list of tuples representing the static gestures data.
        """
        gestures = self._fetch_gesture()
        if gestures is None:
            return None, None
            
        points = np.array([
            [
                hand.roll, hand.pitch, hand.yaw,
                *hand.finger_flex,  # Unpacking the finger flex values
                *(value for value in [hand.mean_acceleration, hand.std_acceleration, hand.mean_angular_velocity, hand.std_angular_velocity] if value is not None)
            ]
            for gesture in gestures
            for hand in (gesture.left_hand, gesture.right_hand) if hand is not None
        ])
        
        names = np.array([
            gesture.name
            for gesture in gestures
            for hand in (gesture.left_hand, gesture.right_hand) if hand is not None])
        tree = KDTree(points)
        
        return tree, names
        
    def _fetch_gesture(self):
        try:
            
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM gestures")
            gestures_data = cursor.fetchall()
            conn.close()
                        
            return [Gesture(
                id=row[0],
                name=row[1],
                left_hand=self._parse_hand_data(row[2]) if row[2] != '' else None,
                right_hand=self._parse_hand_data(row[3]) if row[3] != '' else None
            ) for row in gestures_data]
            
        except Exception as e:
            return None   
        
    def _parse_hand_data(self, hand_data_str):
        hand_data = list(map(float, hand_data_str.split(',')))
        return Gesture.Hand(
            roll=hand_data[0],
            pitch=hand_data[1],
            yaw=hand_data[2],
            finger_flex=list(map(int, hand_data[3:8])),
            mean_acceleration=hand_data[8],
            std_acceleration=hand_data[9],
            mean_angular_velocity=hand_data[10],
            std_angular_velocity=hand_data[11],
            gyro_axis = int(hand_data[12]),
            accel_axis = int(hand_data[13])
            )
            
    def get_gestures(self):
        """
        Retrieves all static gestures from the database.

        Returns:
            list: A list of tuples representing the static gestures data.
        """
        return self.gesture_tree, self.gesture_names