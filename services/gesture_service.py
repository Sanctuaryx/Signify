import os, sys

# Get the directory where the script lives
script_dir = os.path.dirname("repositories/gesture_repository.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("classes/DynamicGesture.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("classes/StaticGesture.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("classes/GestureFactory.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("classes/AbstractGestureFactory.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

import repositories.gesture_repository
import classes.DynamicGesture as DynamicGesture
import classes.StaticGesture as StaticGesture

import numpy as np

class GestureService:
    """
    Service class for recognizing static and dynamic gestures.

    Attributes:
        gesture_repository (GestureRepository): The repository for accessing predefined gestures.
    """

    def __init__(self):
        self.gesture_repository = repositories.gesture_repository.GestureRepository()
        
    def _extract_static_hand_features(self, hand: StaticGesture.Hand):
        """
        Extracts the static hand features from a given hand.

        Args:
            hand (StaticGesture.Hand): The hand object containing the static hand features.

        Returns:
            np.array: The extracted static hand features.
        """
        if hand is None:
            return [np.nan] * 14
        return np.array([
            hand.roll, hand.pitch, hand.yaw,
            *hand.finger_flex, 
            0.0, 0.0, 0.0, 0.0, 0, 0
        ])
            
    def _extract_dynamic_hand_features(self, hand: DynamicGesture.Hand):
        if hand is None:
            return [np.nan] * 14
        return np.array([
            hand.roll, hand.pitch, hand.yaw,
            *hand.finger_flex,
            hand.mean_acceleration, hand.std_acceleration, hand.mean_angular_velocity, hand.std_angular_velocity,
            hand.accel_axis, hand.gyro_axis
        ])
    
    def recognise_static_gesture(self, gesture: StaticGesture.StaticGesture, error_range=30.0): 
        """
        Recognizes a gesture by comparing it with a set of predefined gestures.

        Args:
            gesture (StaticGesture.StaticGesture): The gesture to be recognized.
            error_range (float, optional): The allowed error range for matching the gesture. Defaults to 0.1.

        Returns:
            str or None: The name of the recognized gesture, or None if no matching gesture is found within the error range.
        """
        gesture_tree, gesture_names = self.gesture_repository.get_gestures()
        
        left_hand_features = self._extract_static_hand_features(gesture.left_hand)
        right_hand_features = self._extract_static_hand_features(gesture.right_hand)
        points = np.concatenate((left_hand_features, right_hand_features))
        
        _, index = gesture_tree.query(points, k=1)
                
        nearest_point = gesture_tree.data[index]
        nearest_name = gesture_names[index]
        
        lower_threshold = points * (1 - error_range)
        upper_threshold = points * (1 + error_range)
        valid_lower = np.nan_to_num(lower_threshold, nan=-np.inf)
        valid_upper = np.nan_to_num(upper_threshold, nan=np.inf)
        
        if np.all(nearest_point >= valid_lower) and np.all(nearest_point <= valid_upper):
            return nearest_name
        else:
            return None
                
    def recognise_dynamic_gesture(self, gesture: DynamicGesture.DynamicGesture, error_range=30.0): 
        """
        Recognizes a dynamic gesture by comparing it with the set of predefined gestures.

        Args:
            gesture (DynamicGesture.DynamicGesture): The dynamic gesture to be recognized.
            error_range (float, optional): The error range allowed for matching the gesture. Defaults to 30.0.

        Returns:
            str or None: The name of the nearest matching gesture if it falls within the error range and movement bounds, 
            otherwise returns None.
        """
        gesture_tree, gesture_names = self.gesture_repository.get_gestures()
        
        left_hand_features = self._extract_dynamic_hand_features(gesture.left_hand)
        right_hand_features = self._extract_dynamic_hand_features(gesture.right_hand)
        points = np.concatenate((left_hand_features, right_hand_features))
        
        _, index = gesture_tree.query(points, k=1)
        
        nearest_point = gesture_tree.data[index]
        nearest_name = gesture_names[index]
        
        #eliminate from the general threshold the angular velocity and acceleration values, as well as the axis values
        general_indices = np.setdiff1d(np.arange(len(points)), [8,9,10,11,12,13, 22,23,24,25,26,27])
        lower_threshold = points[general_indices] * (1 - error_range)
        upper_threshold = points[general_indices] * (1 + error_range)
        valid_lower = np.nan_to_num(lower_threshold, nan=-np.inf)
        valid_upper = np.nan_to_num(upper_threshold, nan=np.inf)
        
        within_bounds = np.all(nearest_point[general_indices] >= valid_lower) and np.all(nearest_point[general_indices] <= valid_upper)

        within_movement_bounds = (
            (((points[8] > nearest_point[8]) and (points[9] < nearest_point[9]) and (points[12] == nearest_point[12])) or
            (points[10] > nearest_point[10]) and (points[11] < nearest_point[11]) and (points[13] == nearest_point[13])) 
            or
            ((((points[22] > nearest_point[22]) and (points[23] < nearest_point[23]) and (points[26] == nearest_point[26])) or
            (points[24] > nearest_point[24]) and (points[25] < nearest_point[25]) and (points[27] == nearest_point[27]))
            if len(nearest_point) > 27 else False)
             
        )
        
        if within_bounds and within_movement_bounds:
            return nearest_name
        else:
            return None