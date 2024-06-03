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
import classes.gesture
import services.file_management_service
import services.gesture_service

import math
from scipy.spatial.transform import Rotation as R
import time
import threading
from queue import Queue
import numpy as np

class ApiController:
    def __init__(self):
        sys.stdout.write("Initializing ApiController...")
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
        sys.stdout.flush()

        
    def _read_serial_ports(self):
        """Function to read data from the serial ports."""
        try:
            self._serial_data_thread.start() 
        except AttributeError as e:
            print(f"Error starting the bno controller: {e}")
            self._stop_event.set()
            
    def _is_calibration_needed(self, calibration_izq, calibration_der):
        """Check if calibration is needed based on the calibration data."""
        return any(value < 3 for value in calibration_izq) or any(value < 3 for value in calibration_der)

    def _process_gesture(self, gesture):
        """Process a recognized gesture and ensure it follows the cooldown rules."""
        
        self._tts.convert_text_to_audio_with_engine(gesture)
        self._last_gesture = gesture
        self._last_gesture_time = time.time()
        self._file_controller.play_speech_file()

    def _parse_sensor_data(self, data):
        """Parses the sensor data received from the serial port."""
      
        quat = list(map(float, data[0].split(',')))
        flexors = list(map(float, data[1].split(',')))
        calibration = list(map(float, data[2].split(',')))
        
        r = R.from_quat([quat[1], quat[2], quat[3], quat[0]])
        euler = r.as_euler('xyz', degrees=True)

        return euler, flexors, calibration

    def run(self):
        """Main loop to read and process serial data."""
        try:  
            self._read_serial_ports()
            while not self._stop_event.is_set():
                try:
                    if not self._serial_data_queue.empty():
                        with self._serial_data_queue.mutex: data_izq, data_der = list(self._serial_data_queue.queue)
                        self._serial_data_queue.task_done()
                        
                        euler_izq, flexors_izq, calibration_izq = self._parse_sensor_data(data_izq)
                        euler_der, flexors_der, calibration_der = self._parse_sensor_data(data_der)
                        
                        sys.stdout.write(f"\rData parsed: {euler_izq} - {euler_der} - {flexors_izq} - {flexors_der} - {calibration_izq} - {calibration_der}")
                        sys.stdout.flush()
                            
                        if self._is_calibration_needed(calibration_izq, calibration_der):
                            print("Calibrating needed...")
                            self._calibration.calibrate()
                            with self._serial_data_queue.mutex: self._serial_data_queue.queue.clear()
                            
                        else:
                            static_gesture = self._gesture_service.recognise_gesture_by_values(euler_izq, flexors_izq, euler_der, flexors_der)
                            if static_gesture:
                                    self._process_gesture(static_gesture)
                            if len(self._potential_dynamic_gestures) == 20: 
                                dynamic_gesture = self._gesture_service.recognise_dynamic_gesture(self._potential_dynamic_gestures)
                                if dynamic_gesture:
                                    self._process_gesture(dynamic_gesture)
                                    with self._serial_data_queue.mutex: self._serial_data_queue.queue.clear()
                            else:
                                self._potential_dynamic_gestures.append([[euler_izq, flexors_izq], [euler_der, flexors_der]])                                
                               
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
