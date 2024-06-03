class Gesture:
    def __init__(self, id, name, roll, pitch, yaw, finger_flex_1, finger_flex_2, finger_flex_3, finger_flex_4, finger_flex_5):
        self.id = id
        self.name = name
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.finger_flex_1 = finger_flex_1
        self.finger_flex_2 = finger_flex_2
        self.finger_flex_3 = finger_flex_3
        self.finger_flex_4 = finger_flex_4
        self.finger_flex_5 = finger_flex_5

    def _check_value(self, value, threshold=None, min_val=None, max_val=None):
        """Helper function to check if a value meets the given threshold or falls within a range."""
        return (threshold is None or value > threshold) and \
               (min_val is None or max_val is None or min_val <= value <= max_val)
               
    def _classify_flex(self, flx):
        """
        Classifies the finger flexion values based on the finger flexion thresholds.

        Args:
            flx (list): A list of finger flexion values.

        Returns:
            list: A list of boolean values indicating whether each finger's flexion value matches the corresponding threshold.
        """
        return [self.finger_flex_thresholds[i][0] <= flex <= self.finger_flex_thresholds[i][1] for i, flex in enumerate(flx)]

    def check_gesture(self, eul, flx):
        """Check if the Euler angles and finger flexions meet the criteria for this gesture."""
        roll_match = self._check_value(eul[0], self.roll_threshold, self.roll_min, self.roll_max)
        pitch_match = self._check_value(eul[1], self.pitch_threshold, self.pitch_min, self.pitch_max)
        yaw_match = self._check_value(eul[2], self.yaw_threshold, self.yaw_min, self.yaw_max)

        flex_matches = self._classify_flex(flx)

        return roll_match and pitch_match and yaw_match and all(flex_matches)

gesture_a = Gesture(
    roll_threshold=None,  # No explicit roll threshold
    roll_range=(-10, 10),  # Roll angle range
    pitch_threshold=None,  # No explicit pitch threshold
    pitch_range=(-10, 10),  # Pitch angle range
    yaw_threshold=20,  # Yaw threshold (example)
    yaw_range=(None, None),  # No explicit yaw range
    finger_flex_thresholds=([(-10, 10), (-10, 10), (-10, 10), (-10, 10), (-10, 10)])  # Example thresholds
)

# Dictionary mapping gestures to lambda functions for checking them
dactylology_checks = {
    'A': lambda eul_izq, flx_izq, eul_der, flx_der: gesture_a.check_gesture(eul_izq, flx_izq) or gesture_a.check_gesture(eul_der, flx_der),
}

def recognize_letter(eul_izq, flx_izq, eul_der, flx_der):
    return next((letter for letter, check in dactylology_checks.items() if check(eul_izq, flx_izq, eul_der, flx_der)), None)

