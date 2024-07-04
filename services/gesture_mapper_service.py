import classes.DynamicGesture as DynamicGesture
import classes.StaticGesture as StaticGesture
import classes.BaseGesture as BaseGesture
import classes.GestureFactory as GestureFactory
from typing import List
import numpy as np

class GestureMapperService:
    def __init__(self):
        """
        Initializes a new instance of the GestureMapperService class.
        """
        self.__factory = GestureFactory.GestureFactory()
        
    def static_gesture_to_dynamic_gesture(self, gestures: List[StaticGesture.StaticGesture]) -> DynamicGesture.DynamicGesture:
        """
        Converts a list of static gestures to a dynamic gesture.

        Args:
            gestures (List[StaticGesture.StaticGesture]): A list of static gestures.

        Returns:
            DynamicGesture.DynamicGesture: The converted dynamic gesture.
        """
        left_hand = self.__static_hand_to_dynamic_hand([gesture.left_hand for gesture in gestures if gesture.left_hand is not None])
        right_hand = self.__static_hand_to_dynamic_hand([gesture.right_hand for gesture in gestures if gesture.right_hand is not None])

        return self.__factory.create_dynamic_gesture(left_hand, right_hand)
    
    def __get_movement_axis(self, mean):
        """
        Get the movement axis based on the mean values.

        Args:
            mean (numpy.ndarray): The mean values.

        Returns:
            DynamicGesture.MovementAxis: The movement axis.

        """
        axis_index = np.argmax(mean) + 1  # np.argmax returns 0-based index, add 1 to shift to 1-based
        if axis_index > 3:
            axis_index = 3
        elif axis_index < 1:
            axis_index = 1
        return DynamicGesture.MovementAxis(axis_index)

    def __static_hand_to_dynamic_hand(self, hand: List[StaticGesture.Hand]) -> DynamicGesture.Hand:
        """
        Converts a list of StaticGesture.Hand objects to a DynamicGesture.Hand object.

        Args:
            hand (List[StaticGesture.Hand]): A list of StaticGesture.Hand objects.

        Returns:
            DynamicGesture.Hand: The converted DynamicGesture.Hand object.
        """
        static_attributes = [(h.roll, h.pitch, h.yaw, h.finger_flex, h.gyro, h.accel) for h in hand]
        rolls, pitches, yaws, finger_flexes, gyros, accels = [np.array(attr) for attr in zip(*static_attributes)]

        mean_gyro = np.mean(gyros, axis=0)
        mean_accel = np.mean(accels, axis=0)

        gyro_axis = DynamicGesture.MovementAxis(self.__get_movement_axis(mean_gyro))
        accel_axis = DynamicGesture.MovementAxis(self.__get_movement_axis(mean_accel))

        resultant_acceleration = np.linalg.norm(accels, axis=1)
        mean_acceleration = np.mean(resultant_acceleration, dtype=np.float64)
        std_acceleration = np.std(resultant_acceleration, dtype=np.float64)

        resultant_angular_velocity = np.linalg.norm(gyros, axis=1)
        mean_angular_velocity = np.mean(resultant_angular_velocity, dtype=np.float64)
        std_angular_velocity = np.std(resultant_angular_velocity, dtype=np.float64)

        return DynamicGesture.Hand(
            roll=np.mean(rolls),
            pitch=np.mean(pitches),
            yaw=np.mean(yaws),
            finger_flex=[int(np.mean(group)) for group in zip(*finger_flexes)],
            mean_acceleration=mean_acceleration,
            std_acceleration=std_acceleration,
            mean_angular_velocity=mean_angular_velocity,
            std_angular_velocity=std_angular_velocity,
            gyro_axis=gyro_axis.value,
            accel_axis=accel_axis.value
        )