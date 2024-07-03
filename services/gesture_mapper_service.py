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
        Map a DynamicGesture to a StaticGesture.
        
        :param gesture: The DynamicGesture to map.
        :return: The mapped StaticGesture.
        """
        
        left_hand = self.__static_hand_to_dynamic_hand([gesture.left_hand for gesture in gestures])
        right_hand = self.__static_hand_to_dynamic_hand([gesture.right_hand for gesture in gestures])
                     
        return self.__factory.create_dynamic_gesture(left_hand, right_hand)
    
    def __static_hand_to_dynamic_hand(self, hand: List[StaticGesture.Hand]) -> DynamicGesture.Hand:
        """
        Map a Hand to a HandDto.
        
        :param hand: The Hand to map.
        :return: The mapped HandDto.
        """
        static_attributes = [(h.roll, h.pitch, h.yaw, h.finger_flex, h.gyro, h.accel) for h in hand]
        rolls, pitches, yaws, finger_flexes, gyros, accels = [np.array(attr) for attr in zip(*static_attributes)]
        
        mean_gyro = np.mean(gyros, axis=0)
        mean_accel = np.mean(accels, axis=0)
        
        gyro_axis = DynamicGesture.MovementAxis(np.argmax(mean_gyro))
        accel_axis = DynamicGesture.MovementAxis(np.argmax(mean_accel))
        
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
            gyro_axis=gyro_axis,
            accel_axis=accel_axis
        )