import unittest
from unittest.mock import MagicMock
from queue import Queue
import threading
import sys, os

# Get the directory where the script lives
script_dir = os.path.dirname("main/ApiController.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Assuming your code is in a module named gesture_recognition
from main.ApiController import  check_gestures, parse_sensor_data
class TestGestureRecognition(unittest.TestCase):
    def setUp(self):
        print("Test")

    def test_gesture_recognition(self):
        # Example data to test gesture 'B'
        data_izq = '*1.0,0.0,0.0,0.0*30,25,20,15,10*3,3,3,3*'
        data_der = '*1.0,0.0,0.0,0.0*30,25,20,15,10*3,3,3,3*'
        
        euler_izq, flexors_izq, calibration_izq = parse_sensor_data(data_izq)
        euler_der, flexors_der, calibration_der = parse_sensor_data(data_der)
        
        print("+----------------------+")
        print("| Parsing sensor data |")
        print("+----------------------+")
        print("|     Hand     |           Euler angles            |            Flexor data            |     Calibration data     |")
        print("+--------------+-----------------------------------+-----------------------------------+--------------------------+")
        print("|   Left Hand  | ", euler_izq, " | ", flexors_izq, " | ", calibration_izq,"  |")
        print("|  Right Hand  | ", euler_der, " | ", flexors_der, " | ", calibration_der,"  |")
        print("+--------------+-----------------------------------+-----------------------------------+-------------------------+")

        print("+-------------------+")
        print("|   Checking Gestures   |")
        print("+-------------------+")
        print("|     Hand     |  Gesture  |")
        print("+--------------+-----------+")
        print("|   Left Hand  |", check_gestures(euler_izq, flexors_izq), "   |")
        print("|  Right Hand  |", check_gestures(euler_der, flexors_der), "   |")
        print("+--------------+-----------+") 

if __name__ == '__main__':
    unittest.main()
