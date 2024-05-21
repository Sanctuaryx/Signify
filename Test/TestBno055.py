import unittest
from unittest.mock import MagicMock
from queue import Queue
import threading
import sys, os

# Get the directory where the script lives
script_dir = os.path.dirname("main/ApiController.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("main/TextToSpeechConverter.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("main/GestureClass.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("main/FileController.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

from main.ApiController import ApiController
from main.GestureClass import recognize_letter
from main.TextToSpeechConverter import TTSConverter
from main.FileController import SpeechFileManager
class TestGestureRecognition(unittest.TestCase):
    def setUp(self):
        print("Test")

    def test_gesture_recognition(self):
        api_controller = ApiController()
        tts = TTSConverter("tts_models/es/css10/vits")
        speech = SpeechFileManager()
        
        # Example data to test gesture 'B'
        data_izq = '*5.0,5.0,5.0,5.0*30,30,30,30,30*3,3,3,3*'
        data_der = '*5.0,5.0,5.0,5.0*30,30,30,30,30*3,3,3,3*'
        
        euler_izq, flexors_izq, calibration_izq = api_controller.parse_sensor_data(data_izq)
        euler_der, flexors_der, calibration_der = api_controller.parse_sensor_data(data_der)
        
        print("+--------------------------------------------------+")
        print("| Parsing sensor data                              |")
        print("+--------------+-----------------------------------+----------------------------------+-------------------------+")
        print("|     Hand     |           Euler angles            |            Flexor data           |     Calibration data    |")
        print("+--------------+-----------------------------------+----------------------------------+-------------------------+")
        print("|   Left Hand  | ", euler_izq, " | ", flexors_izq, " | ", calibration_izq,"  |")
        print("|  Right Hand  | ", euler_der, " | ", flexors_der, " | ", calibration_der,"  |")
        print("+--------------+-----------------------------------+----------------------------------+-------------------------+")

        euler_der = [5.0, 5.0, 25.0]
        gesture = recognize_letter(euler_izq, flexors_izq, euler_der, flexors_der)
        
        print("+--------------------------+")
        print("|    Checking Gestures     |")
        print("+--------------------------+")
        print("|     Hand     |  Gesture  |")
        print("+--------------+-----------+")
        print("|    Letter    |    ", gesture, " |")
        print("+--------------+-----------+") 
        
        tts.convert_text_to_audio(gesture)
        speech.play_speech_file()

if __name__ == '__main__':
    unittest.main()
