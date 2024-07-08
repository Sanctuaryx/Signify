from enum import Enum
import classes.BaseGesture as BaseGesture

class MovementAxis(Enum):
    X = 1
    Y = 2
    Z = 3
    
class Hand:
    """
    Represents a dynamic gesture of a hand.

    Attributes:
        roll (float): The roll angle of the hand.
        pitch (float): The pitch angle of the hand.
        yaw (float): The yaw angle of the hand.
        finger_flex (float): The flexion of the fingers.
        gyro_axis (MovementAxis): The axis of gyroscope movement.
        accel_axis (MovementAxis): The axis of accelerometer movement.
        mean_acceleration (float): The mean acceleration of the hand.
        std_acceleration (float): The standard deviation of acceleration of the hand.
        mean_angular_velocity (float): The mean angular velocity of the hand.
        std_angular_velocity (float): The standard deviation of angular velocity of the hand.
    """

    def __init__(self, roll, pitch, yaw, finger_flex, gyro_axis: MovementAxis = None, accel_axis: MovementAxis = None, mean_acceleration = None, std_acceleration = None, mean_angular_velocity = None, std_angular_velocity = None):
        self._roll = roll
        self._pitch = pitch
        self._yaw = yaw
        self._finger_flex = finger_flex
        self._mean_acceleration = mean_acceleration
        self._std_acceleration = std_acceleration
        self._mean_angular_velocity = mean_angular_velocity
        self._std_angular_velocity = std_angular_velocity
        self.gyro_axis = gyro_axis
        self.accel_axis = accel_axis

    @property
    def roll(self):
        return self._roll
    
    @roll.setter
    def set_roll(self, roll):
        self._roll = roll
    
    @property
    def pitch(self):
        return self._pitch
    
    @pitch.setter
    def set_pitch(self, pitch):
        self._pitch = pitch
    
    @property
    def yaw(self):
        return self._yaw
    
    @yaw.setter
    def set_yaw(self, yaw):
        self._yaw = yaw
    
    @property
    def finger_flex(self):
        return self._finger_flex
    
    @finger_flex.setter
    def set_finger_flex(self, finger_flex):
        self._finger_flex = finger_flex
    
    @property
    def mean_acceleration(self):
        return self._mean_acceleration
    
    @mean_acceleration.setter
    def set_mean_acceleration(self, mean_acceleration):
        self._mean_acceleration = mean_acceleration
    
    @property
    def std_acceleration(self):
        return self._std_acceleration
    
    @std_acceleration.setter
    def set_std_acceleration(self, std_acceleration):
        self._std_acceleration = std_acceleration
    
    @property
    def mean_angular_velocity(self):
        return self._mean_angular_velocity
    
    @mean_angular_velocity.setter
    def set_mean_angular_velocity(self, mean_angular_velocity):
        self._mean_angular_velocity = mean_angular_velocity
    
    @property
    def std_angular_velocity(self):
        return self._std_angular_velocity
    
    @std_angular_velocity.setter
    def set_std_angular_velocity(self, std_angular_velocity):
        self._std_angular_velocity = std_angular_velocity
    
class DynamicGesture(BaseGesture.BaseGesture):
    """
    Represents a dynamic gesture that involves both the left and right hand.

    Args:
        left_hand (Hand): The left hand involved in the gesture.
        right_hand (Hand): The right hand involved in the gesture.
        id (optional): The ID of the gesture. Defaults to None.
        name (optional): The name of the gesture. Defaults to None.
    """

    def __init__(self, left_hand: Hand, right_hand: Hand, id=None, name=None):
        super().__init__(id, name)
        self._left_hand = left_hand
        self._right_hand = right_hand

    @property
    def left_hand(self):
        """
        Get the left hand involved in the gesture.

        Returns:
            Hand: The left hand.
        """
        return self._left_hand

    @left_hand.setter
    def set_left_hand(self, left_hand):
        """
        Set the left hand involved in the gesture.

        Args:
            left_hand (Hand): The left hand.
        """
        self._left_hand = left_hand

    @property
    def right_hand(self):
        """
        Get the right hand involved in the gesture.

        Returns:
            Hand: The right hand.
        """
        return self._right_hand

    @right_hand.setter
    def set_right_hand(self, right_hand):
        """
        Set the right hand involved in the gesture.

        Args:
            right_hand (Hand): The right hand.
        """
        self._right_hand = right_hand
    