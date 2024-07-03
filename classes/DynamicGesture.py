from enum import Enum
import classes.BaseGesture as BaseGesture

class MovementAxis(Enum):
    X = 1
    Y = 2
    Z = 3
    
class Hand:
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
    def __init__(self, left_hand : Hand, right_hand : Hand, id = None, name = None):
        super().__init__(id, name)
        self._left_hand = left_hand
        self._right_hand = right_hand
    
    @property
    def left_hand(self):
        return self._left_hand
    
    @left_hand.setter
    def set_left_hand(self, left_hand):
        self._left_hand = left_hand
    
    @property
    def right_hand(self):
        return self._right_hand
    
    @right_hand.setter
    def set_right_hand(self, right_hand):
        self._right_hand = right_hand
    