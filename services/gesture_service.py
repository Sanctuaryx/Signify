import os, sys

# Get the directory where the script lives
script_dir = os.path.dirname("repositories/gesture_repository.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("classes/gesture.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

import repositories.gesture_repository

class GestureService:
    def __init__(self):
        self.gesture_repository = repositories.gesture_repository.GestureRepository()
        self.gestures = None

    def _load_gestures(self):
        gesture_data = self.gesture_repository.get_all_static_gestures()
        gestures = {}

        for gesture in gesture_data:
            (id, name, roll, pitch, yaw, finger1, finger2, finger3, finger4, finger5) = gesture

            flex_thresholds = [
                finger1, finger2, finger3, finger4, finger5
            ]

            #gestures[name] = classes.gesture(id, name, roll, pitch, yaw, flex_thresholds)

        self.gestures = gestures

    def recognize_gesture_from_loaded_db(self, eul_izq, flx_izq, eul_der, flx_der):
        """
        Recognize the letter based on the Euler angles and finger flexions of both hands.

        :param eul_izq: Euler angles of the left hand.
        :param flx_izq: Finger flexions of the left hand.
        :param eul_der: Euler angles of the right hand.
        :param flx_der: Finger flexions of the right hand.
        :return: The recognized letter or None if no match is found.
        """
        self._load_gestures()
        return next((name for name, gesture in self.gestures.items() if gesture.check_gesture(eul_izq, flx_izq) or gesture.check_gesture(eul_der, flx_der)), None)

    def recognise_gesture_by_values(self, euler_izq, flexors_izq, euler_der, flexors_der):
        """
        Retrieve a gesture based on provided values.

        :param roll: Roll value.
        :param pitch: Pitch value.
        :param yaw: Yaw value.
        :param finger_flex: List of finger flex values.
        :return: The gesture or None if no match is found.
        """
        result = self.gesture_repository.get_static_gesture_by_values(euler_izq, euler_der, flexors_izq, flexors_der)
        if result:
            return result
        return None
    
    def recognise_dynamic_gesture(self, gesture_izq, gesture_der):
        """
        Retrieve a gesture based on provided values.

        :param roll: Roll value.
        :param pitch: Pitch value.
        :param yaw: Yaw value.
        :param finger_flex: List of finger flex values.
        :return: The gesture or None if no match is found.
        """
        result_der = self.gesture_repository.get_dynamic_gesture_by_values(gesture_der)
        if result_der:
            return result_der
        
        result_izq = self.gesture_repository.get_dynamic_gesture_by_values(gesture_izq)
        if result_izq:
            return result_izq
        
        return None
        
