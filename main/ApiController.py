import threading
import sys, os

# Get the directory where the script lives
script_dir = os.path.dirname("main/Bno055Controller.py")
# Add the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

# Get the directory where the script lives
script_dir = os.path.dirname("main/Calibration.py")
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

import main.Bno055Controller
import main.Calibration
import main.TextToSpeechConverter
import main.GestureClass
import main.FileController

import math
import time
import threading
from queue import Queue
import numpy as np

class ApiController:
    def __init__(self):
        self._last_gesture = None
        self._last_gesture_time = 0
        self._cooldown_time = 2
        self._serial_data_queue = Queue(maxsize=100)
        self._stop_event = threading.Event()
        
        self._tts = main.TextToSpeechConverter.TTSConverter("tts_models/es/css10/vits")
        self._calibration = main.Calibration.BNO055Calibrator(self._serial_data_queue, self._stop_event)
        self._file_controller = main.FileController.SpeechFileManager()
        
        self._bno_controller = main.Bno055Controller.SerialPortReader('COM3', 'COM4', self._serial_data_queue, self._stop_event)
        self._serial_data_thread = threading.Thread(target=self._bno_controller.start, daemon=True)
        
    def read_serial_ports(self):
        """Function to read data from the serial ports."""
        try:
            self._serial_data_thread.start() 
        except AttributeError as e:
            print(f"Error starting the bno controller: {e}")
            self._stop_event.set()
            
    def is_calibration_needed(self, calibration_izq, calibration_der):
        """Check if calibration is needed based on the calibration data."""
        return any(value < 2 for value in calibration_izq) or any(value < 2 for value in calibration_der)

    def process_gesture(self, gesture):
        """Process a recognized gesture and ensure it follows the cooldown rules."""
        current_time = time.time()
        if gesture and (gesture != self._last_gesture or current_time - self._last_gesture_time > self._cooldown_time):
            print(f"Recognized gesture: {gesture}")
            self._tts.convert_text_to_audio(gesture)
            self._last_gesture = gesture
            self._last_gesture_time = current_time
            self._file_controller.play_speech_file()

    def parse_sensor_data(self, data):
        """Parses the sensor data received from the serial port."""
        
        split_data = [part for part in data.strip('*').split('*') if part]
        
        if len(split_data) != 3:
            print("Error: Unexpected data format")
            return None
        
        quat = list(map(float, split_data[0].split(',')))
        flexors = list(map(float, split_data[1].split(',')))
        calibration = list(map(float, split_data[2].split(',')))
        
        roll=math.atan2(2*(quat[0]*quat[1]+quat[2]*quat[3]),1-2*(quat[1]*quat[1]+quat[2]*quat[2]))
        pitch=math.asin(2*(quat[0]*quat[2]-quat[3]*quat[1]))
        yaw=math.atan2(2*(quat[0]*quat[3]+quat[1]*quat[2]),1-2*(quat[2]*quat[2]+quat[3]*quat[3]))-np.pi/2

        return [roll, pitch, yaw], flexors, calibration

    def run(self):
        """Main loop to read and process serial data."""
        try:  
            self.read_serial_ports()
            while not self._stop_event.is_set():
                try:
                    if not self._serial_data_queue.empty():
                        data_izq, data_der = self._serial_data_queue.get()
                        self._serial_data_queue.task_done()
                        euler_izq, flexors_izq, calibration_izq = self.parse_sensor_data(data_izq)
                        euler_der, flexors_der, calibration_der = self.parse_sensor_data(data_der)
                        print(f"Data parsed: {euler_izq} - {euler_der}")
                        
                        if self.is_calibration_needed(calibration_izq, calibration_der):
                            print("Calibrating needed...")
                            self._calibration.calibrate()
                            with self._serial_data_queue.mutex: self._serial_data_queue.queue.clear()
                        else:
                            gesture = main.GestureClass.recognize_letter(euler_izq, euler_der, flexors_izq, flexors_der)
                            if gesture:
                                self.process_gesture(gesture)
                except Exception as e:
                    print(f"Error processing data: {e}")
                    
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
