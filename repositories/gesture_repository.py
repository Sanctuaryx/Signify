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
            print('Failed to fetch gestures from the database.')
            return None, None
            
        points = np.array([
            [
                hand.roll, hand.pitch, hand.yaw,
                *hand.finger_flex, 
                *(value for value in [hand.mean_acceleration, hand.std_acceleration, hand.mean_angular_velocity, hand.std_angular_velocity] if value is not None)
            ]
            for gesture in gestures
            for hand in (gesture.left_hand, gesture.right_hand) if hand is not None
        ])
        
        tree = KDTree(points)
        names = np.array([
            gesture.name
            for gesture in gestures])
        
        return tree, names
        
    def _fetch_gesture(self) -> list[DynamicGesture.DynamicGesture]:
        try:
            
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM gestures g LEFT JOIN hands lh ON g.left_hand_id = lh.id LEFT JOIN hands rh ON g.right_hand_id = rh.id")
            gestures_data = cursor.fetchall()
            conn.close()
                        
            return [self.__factory.create_dynamic_stored_gesture(
                row[0],
                row[1],
                DynamicGesture.Hand(
                    roll=row[5],
                    pitch=row[6],
                    yaw=row[7],
                    finger_flex=list(map(int, row[8:13])),
                    mean_acceleration=row[13],
                    std_acceleration=row[14],
                    mean_angular_velocity=row[15],
                    std_angular_velocity=row[16],
                    gyro_axis = int(row[17]),
                    accel_axis = int(row[18])
                    ) if row[2] is not None else None,
                DynamicGesture.Hand(
                    roll=row[20],
                    pitch=row[21],
                    yaw=row[22],
                    finger_flex=list(map(int, row[23:28])),
                    mean_acceleration=row[28],
                    std_acceleration=row[29],
                    mean_angular_velocity=row[30],
                    std_angular_velocity=row[31],
                    gyro_axis = int(row[32]),
                    accel_axis = int(row[33])
                    ) if row[3] is not None else None
            ) for row in gestures_data]
            
        except Exception as e:
            print(f'Failed to fetch gestures from the database: {e}')
            return None   
            
    def get_gestures(self):
        """
        Retrieves all static gestures from the database.

        Returns:
            list: A list of tuples representing the static gestures data.
        """
        return self.__gesture_tree, self.__gesture_names