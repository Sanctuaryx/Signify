import classes.DynamicGesture as Gesture
import classes.StaticGesture as GestureDto
from typing import List
import numpy as np

class GestureMapperService:
    def __init__(self):
        """
        Initializes a new instance of the GestureMapperService class.
        """
        pass
        
    def gesture_dto_to_gesture(self, gestures: List[GestureDto.GestureDto]) -> Gesture.Gesture:
        """
        Map a Gesture to a GestureDto.
        
        :param gesture: The Gesture to map.
        :return: The mapped GestureDto.
        """
        
        left_hand = self._hand_dto_to_hand([gesture.left_hand for gesture in gestures])
        right_hand = self._hand_dto_to_hand([gesture.right_hand for gesture in gestures])
                     
        return GestureDto(None, None, left_hand, right_hand)
    
    def _hand_dto_to_hand(self, hand: List[GestureDto.Hand]):
        """
        Map a Hand to a HandDto.
        
        :param hand: The Hand to map.
        :return: The mapped HandDto.
        """
        rolls = np.array([h.roll for h in hand])
        pitches = np.array([h.pitch for h in hand])
        yaws = np.array([h.yaw for h in hand])
        finger_flexes = np.array([h.finger_flex for h in hand])
        gyros = np.array([h.gyro for h in hand])
        accels = np.array([h.accel for h in hand])
        
        mean_gyro = np.mean(gyros, axis=0)
        mean_accel = np.mean(accels, axis=0)
        
        gyro_axis = Gesture.MovementAxis(np.argmax(mean_gyro))
        accel_axis = Gesture.MovementAxis(np.argmax(mean_accel))
        
        resultant_acceleration = np.linalg.norm(accels, axis=1)
        mean_acceleration = np.mean(resultant_acceleration, dtype=np.float64)
        std_acceleration = np.std(resultant_acceleration, dtype=np.float64)

        resultant_angular_velocity = np.linalg.norm(gyros, axis=1)
        mean_angular_velocity = np.mean(resultant_angular_velocity, dtype=np.float64)
        std_angular_velocity = np.std(resultant_angular_velocity, dtype=np.float64)
        
        return Gesture.Hand(
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