import classes.BaseGesture as BaseGesture

class Hand:
    """
    Represents a static gesture of a hand.

    Attributes:
        roll (float): The roll angle of the hand.
        pitch (float): The pitch angle of the hand.
        yaw (float): The yaw angle of the hand.
        finger_flex (float): The flexion of the fingers.
        gyro (float): The gyroscope data.
        accel (float): The accelerometer data.
        calibration (float): The calibration data.
    """

    def __init__(self, roll, pitch, yaw, gyro, accel, finger_flex, calibration):
        self._roll = roll
        self._pitch = pitch
        self._yaw = yaw
        self._finger_flex = finger_flex
        self._gyro = gyro
        self._accel = accel
        self._calibration = calibration
        
    @property
    def roll(self):
        return self._roll
    
    @roll.setter
    def roll(self, roll):
        self._roll = roll
        
    @property
    def pitch(self):
        return self._pitch
    
    @pitch.setter   
    def pitch(self, pitch):
        self._pitch = pitch
        
    @property
    def yaw(self):
        return self._yaw
    
    @yaw.setter
    def yaw(self, yaw):
        self._yaw = yaw
        
    @property
    def finger_flex(self):
        return self._finger_flex
    
    @finger_flex.setter
    def finger_flex(self, finger_flex):
        self._finger_flex = finger_flex
        
    @property
    def gyro(self):
        return self._gyro
    
    @gyro.setter
    def gyro(self, gyro):
        self._gyro = gyro
        
    @property
    def accel(self):
        return self._accel
    
    @accel.setter
    def accel(self, accel):
        self._accel = accel
        
    @property
    def calibration(self):
        return self._calibration
    
    @calibration.setter
    def calibration(self, calibration):
        self._calibration = calibration

class StaticGesture(BaseGesture.BaseGesture):
    """
    Represents a static gesture that can be performed with both hands.

    Args:
        left_hand (Hand): The left hand associated with the gesture.
        right_hand (Hand): The right hand associated with the gesture.
        id (optional): The ID of the gesture. Defaults to None.
        name (optional): The name of the gesture. Defaults to None.
    """

    def __init__(self, left_hand: Hand, right_hand: Hand, id=None, name=None):
        super().__init__(id, name)
        self._left_hand = left_hand
        self._right_hand = right_hand

    @property
    def left_hand(self):
        return self._left_hand

    @left_hand.setter
    def left_hand(self, left_hand):
       self._left_hand = left_hand

    @property
    def right_hand(self):
        return self._right_hand

    @right_hand.setter
    def right_hand(self, right_hand):
        self._right_hand = right_hand

    