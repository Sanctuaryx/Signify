import unittest
from unittest.mock import MagicMock
from queue import Queue
import threading
import sys, os
import pyttsx3

# Get the directory where the script lives
script_dir = os.path.dirname("signify.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("controllers/bno055_controller.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("services/calibration_service.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("services/text_to_speech_service.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("classes/gesture.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("services/file_management_service.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

from signify import ApiController
from classes.gesture import recognize_letter
from services.text_to_speech_service import TTSConverter
from services.file_management_service import SpeechFileManager
class TestGestureRecognition:

    def test_gesture_recognition(self):
        api_controller = ApiController()
        #tts = TTSConverter("tts_models/multilingual/multi-dataset/xtts_v2")
        #tts = TTSConverter("tts_models/es/css10/vits")
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
        
        #tts.convert_text_to_audio("la palabra es: A", speaker_wav="resources/audioResources/samples_es_sample.wav", language="es")
        #tts.convert_text_to_audio(text="la letra es Be")
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)
        
        # Check and set the available voices
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'spanish' in voice.languages:
                self.engine.setProperty('voice', voice.id)
                
            
        self.engine.save_to_file("A", "resources/audioResources/audioTracks/audio.wav")
        self.engine.runAndWait()
        
        speech.play_speech_file()

if __name__ == '__main__':
    test = TestGestureRecognition()
    test.test_gesture_recognition()
