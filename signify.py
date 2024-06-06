import threading
import sys, os

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
script_dir = os.path.dirname("services/gesture_service.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("services/file_management_service.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

import controllers.bno055_controller
import services.calibration_service
import services.text_to_speech_service
import services.file_management_service
import services.gesture_service

import math
from scipy.spatial.transform import Rotation as R
import time
import threading
from queue import Queue
import numpy as np
import datetime

class ApiController:
    def __init__(self):
        print("Initializing ApiController...")
        self._last_gesture = None
        self._potential_dynamic_gestures = []
        self._last_gesture_time = 0
        self._cooldown_time = 2
        self._serial_data_queue = Queue(maxsize=50)
        self._stop_event = threading.Event()
        
        self._tts = services.text_to_speech_service.TTSConverter("tts_models/es/css10/vits")
        self._calibration = services.calibration_service.BNO055Calibrator(self._serial_data_queue, self._stop_event)
        self._file_controller = services.file_management_service.SpeechFileManager()
        self._gesture_service = services.gesture_service.GestureService()
        
        self._bno_controller = controllers.bno055_controller.SerialPortReader('COM3', 'COM4', self._serial_data_queue, self._stop_event)
        self._serial_data_thread = threading.Thread(target=self._bno_controller.start, daemon=True)

        
    def _read_serial_ports(self):
        """Function to read data from the serial ports."""
        try:
            self._serial_data_thread.start() 
        except AttributeError as e:
            print(f"Error starting the bno controller: {e}")
            self._stop_event.set()
            
    def _is_calibration_needed(self, calibration_izq, calibration_der):
        """Check if calibration is needed based on the calibration data."""
        return any(value < 2 for value in calibration_izq) or any(value < 2 for value in calibration_der)

    def _process_gesture(self, gesture):
        """Process a recognized gesture and ensure it follows the cooldown rules."""
        
        self._tts.convert_text_to_audio_with_engine(gesture)
        self._last_gesture = gesture
        self._last_gesture_time = time.time()
        self._file_controller.play_speech_file()
        
    def _cross(self, v1, v2):
        return np.cross(v1, v2)

    def _get_positional_vectors(self, euler):
        
        roll_rad = np.radians(euler[0])
        pitch_rad = np.radians(euler[1])
        yaw_rad = np.radians(euler[2])

        k = np.array([np.cos(yaw_rad) * np.cos(pitch_rad), np.sin(pitch_rad), np.sin(yaw_rad) * np.cos(pitch_rad)])
        
        y = np.array([0, 1, 0])
        s = self._cross(k, y)
        v = self._cross(s, k)
        vrot = v * np.cos(roll_rad) + np.cross(k, v) * np.sin(roll_rad)        
        print(f"K: {k} - V: {v} - Vrot: {vrot}")
        return k, np.cross(k, vrot), vrot

    def _parse_sensor_data(self, data):
        """Parses the sensor data received from the serial port."""
      
        quat = list(map(float, data[0].split(',')))
        flexors = list(map(float, data[1].split(',')))
        calibration = list(map(float, data[2].split(',')))
        
        r = R.from_quat([quat[1], quat[2], quat[3], quat[0]])
        euler = r.as_euler('xyz', degrees=True)

        return euler, flexors, calibration
    
    def _process_static_gesture(self, euler_izq, flexors_izq, euler_der, flexors_der):
        """Process a static gesture if recognized."""

        static_gesture = self._gesture_service.recognise_gesture_by_values(euler_izq, flexors_izq, euler_der, flexors_der)
        if static_gesture:
            self._process_gesture(static_gesture)
        

    def _process_dynamic_gesture(self, euler_izq, flexors_izq, euler_der, flexors_der):
        """Process a dynamic gesture if recognized."""
        print(f"Euler izq: {euler_izq} - Flexors izq: {flexors_izq} - Euler der: {euler_der} - Flexors der: {flexors_der}")

        if len(self._potential_dynamic_gestures) == 20: 
            dynamic_gesture = self._gesture_service.recognise_dynamic_gesture(self._potential_dynamic_gestures)
            if dynamic_gesture:
                self._process_gesture(dynamic_gesture)
        else:
            self._potential_dynamic_gestures.append([[euler_izq, flexors_izq], [euler_der, flexors_der]])

    def run(self):
        """Main loop to read and process serial data."""
        try:  
            self._read_serial_ports()
            while not self._stop_event.is_set():
                try:
                    if not self._serial_data_queue.empty():
                        data_izq, data_der = self._serial_data_queue.get()
                        #self._serial_data_queue.task_done()
                        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
                        euler_izq, flexors_izq, calibration_izq = self._parse_sensor_data(data_izq)
                        euler_der, flexors_der, calibration_der = self._parse_sensor_data(data_der)

                        
                        #if self._is_calibration_needed(calibration_izq, calibration_der):
                         #   print("Calibrating needed...")
                            #self._calibration.calibrate()
                          #  self._serial_data_queue.queue.clear()
                            
                        #else:
                        self._process_static_gesture(euler_izq, flexors_izq, euler_der, flexors_der)
                        print("s")
                        self._process_dynamic_gesture(euler_izq, flexors_izq, euler_der, flexors_der)
                            
                        with self._serial_data_queue.mutex: self._serial_data_queue.queue.clear()
            
                except Exception as e:
                    self._serial_data_queue.get()  # Remove the invalid data
                    
        except Exception as e:
            self._serial_data_queue.get()  # Remove the invalid data 
        except KeyboardInterrupt:
            print("Stopping...")
            self._stop_event.set()  # Signal the thread to stop
            with self._serial_data_queue.mutex: self._serial_data_queue.queue.clear()
            
        finally:
            self._bno_controller.stop()
            self._serial_data_thread.join()  # Wait for the thread to finish
            print("\n\nProgram terminated.")
            
if __name__ == "__main__":
    
    processor = ApiController()
    processor.run()
