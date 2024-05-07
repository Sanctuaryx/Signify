
class Gesture:
    def __init__(self, roll_threshold = None, roll_range = None, 
                 pitch_threshold = None, pitch_range = None, 
                 yaw_threshold = None, yaw_range = None, 
                 finger_flex_thresholds = (30, 50, 100)):
        
        self.roll_threshold = roll_threshold
        self.roll_min, self.roll_max = roll_range
        
        self.pitch_threshold = pitch_threshold
        self.pitch_min, self.pitch_max = pitch_range
        
        self.yaw_threshold = yaw_threshold
        self.yaw_min, self.yaw_max = yaw_range
        
        self.finger_flexed, self.finger_semi, self.finger_extended = finger_flex_thresholds

    def _check_value(self, value, threshold=None, min_val=None, max_val=None):
        """Helper function to check if a value meets the given threshold or falls within a range."""
        return (threshold is None or value > threshold) and \
               (min_val is None or max_val is None or min_val <= value <= max_val)
               
    def _classify_flex(self, value):
        """Classify a flex value as 'flexed', 'semi', or 'extended'."""
        if value < self.flexed_threshold:
            return "flexed"
        elif self.flexed_threshold <= value < self.semi_threshold:
            return "semi"
        else:
            return "extended"

    def check_gesture(self, eul, flx):
        """Check if the Euler angles and finger flexions meet the criteria for this gesture."""
        roll_match = self._check_value(eul[0], self.roll_threshold, self.roll_min, self.roll_max)
        pitch_match = self._check_value(eul[1], self.pitch_threshold, self.pitch_min, self.pitch_max)
        yaw_match = self._check_value(eul[2], self.yaw_threshold, self.yaw_min, self.yaw_max)

        flex_matches = [self._classify_flex(f) for f in flx]

        return roll_match and pitch_match and yaw_match and all(flex_matches)

# Initialize gestures with placeholder thresholds
gesture_a = Gesture(
    roll_threshold=45,  # Example roll threshold for "A" gesture
    pitch_range=(-10, 10),  # Pitch angle range (min, max)
    yaw_range=(-10, 10),  # Yaw angle range (min, max)
    finger_flex_thresholds=[
        50,  # Thumb flexion threshold (fully extended)
        30,  # Index flexion threshold (fully flexed)
        30,  # Middle flexion threshold (fully flexed)
        30,  # Ring flexion threshold (fully flexed)
        30   # Pinky flexion threshold (fully flexed)
    ]
)

# Dictionary mapping gestures to lambda functions for checking them
gesture_checks = {
    'A': lambda eul_izq, flx_izq, eul_der, flx_der: gesture_a.check_gesture(eul_izq, flx_izq) or gesture_a.check_gesture(eul_der, flx_der),
}

def recognize_letter(eul_izq, flx_izq, eul_der, flx_der):
      
    return next((letter for letter, check in gesture_checks.items() if check(eul_izq, flx_izq, eul_der, flx_der)), None)

