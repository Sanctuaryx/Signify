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
script_dir = os.path.dirname("classes/gesture_dto.py")
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
import classes.gesture as Gesture
import classes.gesture_dto as GestureDto
import services.gesture_mapper_service

from scipy.spatial.transform import Rotation as R
import time
import threading
from queue import Queue

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
        self._gesture_mapper = services.gesture_mapper_service.GestureMapperService()
        
        self._bno_controller = controllers.bno055_controller.SerialPortRearight('COM3', 'COM4', self._serial_data_queue, self._stop_event)
        self._serial_data_thread = threading.Thread(target=self._bno_controller.start, daemon=True)

        
    def _read_serial_ports(self):
        """Function to read data from the serial ports."""
        try:
            self._serial_data_thread.start() 
        except AttributeError as e:
            print(f"Error starting the bno controller: {e}")
            self._stop_event.set()
            
    def _is_calibration_needed(self, calibration_left, calibration_right):
        """Check if calibration is needed based on the calibration data."""
        return any(value < 2 for value in calibration_left) or any(value < 2 for value in calibration_right)

    def _process_gesture(self, gesture):
        """Process a recognized gesture and ensure it follows the cooldown rules."""
        
        self._tts.convert_text_to_audio_with_engine(gesture)
        self._last_gesture = gesture
        self._last_gesture_time = time.time()
        self._file_controller.play_speech_file()

    def _parse_sensor_data(self, data_right, data_left) -> GestureDto.GestureDto:
        """Parses the sensor data received from the serial port."""
      
        euler_right, gyro_right, accel_right, flexors_right, calibration_right = [list(map(float, item.split(','))) for item in data_right]
        euler_left, gyro_left, accel_left, flexors_left, calibration_left = [list(map(float, item.split(','))) for item in data_left]
        
        return GestureDto(
            id=None,
            name=None,
            left_hand=GestureDto.Hand(
                roll=euler_left[0],
                pitch=euler_left[1],
                yaw=euler_left[2],
                finger_flex = flexors_left,
                gyro = gyro_left,
                accel = accel_left,
                calibration = calibration_left
            ),
            right_hand=GestureDto.Hand(
                roll=euler_right[0],
                pitch=euler_right[1],
                yaw=euler_right[2],
                finger_flex = flexors_right,
                gyro = gyro_right,
                accel = accel_right,
                calibration = calibration_right
            ))

    def _process_static_gesture(self, gesture_dto):
        """Process a static gesture if recognized."""

        static_gesture = self._gesture_service.recognise_gesture(gesture_dto)
        if static_gesture:
            self._process_gesture(static_gesture)
        

    def _process_dynamic_gesture(self, gesture_dto):
        """Process a dynamic gesture if recognized."""
        if len(self._potential_dynamic_gestures) == 5:
            dynamic_gesture = self._gesture_service.recognise_gesture(self._gesture_mapper.gesture_dto_to_gesture(self._potential_dynamic_gestures))
            if dynamic_gesture:
                self._process_gesture(dynamic_gesture)
            self._potential_dynamic_gestures.clear()
        else:
            self._potential_dynamic_gestures.append(gesture_dto)

    def run(self):
        """Main loop to read and process serial data."""
        try:  
            self._read_serial_ports()
            while not self._stop_event.is_set():
                try:
                    if not self._serial_data_queue.empty():
                        data_left, data_right = self._serial_data_queue.get()
                        self._serial_data_queue.task_done()
                        gesture_dto = self._parse_sensor_data(data_right, data_left)

                        print(f"Left: {gesture_dto.left_hand.roll}, {gesture_dto.left_hand.pitch}, {gesture_dto.left_hand.yaw}, {gesture_dto.left_hand.finger_flex}")        
                        if self._is_calibration_needed(gesture_dto.left_hand.calibration, gesture_dto.right_hand.calibration):
                            print("Calibrating needed...")
                            self._calibration.calibrate()
                            self._serial_data_queue.queue.clear()
                            
                        else:
                            self._process_static_gesture(gesture_dto)
                            self._process_dynamic_gesture(gesture_dto)
                            
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
