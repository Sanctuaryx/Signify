import sqlite3
import numpy as np
from scipy.spatial import KDTree
import classes.DynamicGesture as DynamicGesture
import classes.StaticGesture as StaticGesture
import classes.GestureFactory as GestureFactory
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
        self.__factory = GestureFactory.GestureFactory()
        self._db_path = db_path
        self.__gesture_tree, self.__gesture_names = self._get_all_gestures()
        print('DynamicGesture repository initialized successfully.')

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

            cursor.execute("SELECT * FROM gestures g LEFT JOIN hands lh ON g.left_hand_id = lh.id LEFT JOIN hands rh ON g.right_hand_id = rh.id")
            gestures_data = cursor.fetchall()
            conn.close()
                        
            return [self.__factory.create_dynamic_gesture(
                id=row[0],
                name=row[1],
                left_hand=DynamicGesture.Hand(
                    roll=row[3],
                    pitch=row[4],
                    yaw=row[5],
                    finger_flex=list(map(int, row[6:11])),
                    mean_acceleration=row[11],
                    std_acceleration=row[12],
                    mean_angular_velocity=row[13],
                    std_angular_velocity=row[14],
                    gyro_axis = int(row[15]),
                    accel_axis = int(row[16])
                    ),
                right_hand=DynamicGesture.Hand(
                    roll=row[17],
                    pitch=row[18],
                    yaw=row[19],
                    finger_flex=list(map(int, row[20:25])),
                    mean_acceleration=row[25],
                    std_acceleration=row[26],
                    mean_angular_velocity=row[27],
                    std_angular_velocity=row[28],
                    gyro_axis = int(row[29]),
                    accel_axis = int(row[30])
                    )
            ) for row in gestures_data]
            
        except Exception as e:
            return None   
        
    def _parse_hand_data(self, hand_data_str):
        hand_data = list(map(float, hand_data_str.split(',')))
        return DynamicGesture.Hand(
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
        return self.__gesture_tree, self.__gesture_names