# Let's use PlantUML to render the diagram from the provided code.
from plantuml import PlantUML
import matplotlib.pyplot as plt
import io

# PlantUML code
plantuml_code = """
@startuml
' Define the main package
package "GestureRecognitionPackage" {
    package "GestureRecognition" {
        package "Controllers" {
            class ApiController {
                - _last_gesture : None
                - _potential_dynamic_gestures : []
                - _last_gesture_time : 0
                - _cooldown_time : 2
                - _serial_data_queue : Queue(maxsize=50)
                - _stop_event : threading.Event()
                - _tts : TTSConverter
                - _calibration : BNO055Calibrator
                - _file_controller : SpeechFileManager
                - _gesture_service : GestureService
                - _gesture_mapper : GestureMapperService
                - _bno_controller : SerialPortReader
                + create ApiController()
                + _read_serial_ports()
                + is_calibration_needed(calibration_left, calibration_right)
                + _process_gesture(gesture)
                + _process_static_gesture(gesture_dto)
                + _process_dynamic_gesture(gesture_dto)
                + run()
            }
        }

        package "Services" {
            class GestureService {
                - gesture_repository : GestureRepository
                - gesture_factory : HandFactory
                + create GestureService()
                + _extract_hand_features(hand : GestureDto.Hand)
                + _extract_hand_features(hand : Gesture.Hand)
                + recognise_gesture(gesture : GestureDto.Gesture, error_range : 0.1)
            }

            class GestureMapperService {
                - left_hand
                - right_hand
                + create GestureMapperService()
                + _hand_dto_to_hand(hand : List)
            }
        }

        package "Repositories" {
            class GestureRepository {
                - _db_path : db_path
                + create GestureRepository()
                + _get_all_gestures()
                + _fetch_gesture()
                + _parse_hand_data(hand_data_str)
                + get_gestures()
            }
        }

        package "Models" {
            class Gesture {
                - id : int
                - name : String
                - left_hand : Hand
                - right_hand : Hand
                + create Gesture(id: int, name: String, left_hand: Hand, right_hand: Hand)
                + getId(): int
                + getName(): String
                + getLeftHand(): Hand
                + getRightHand(): Hand
            }

            class GestureDto {
                - id : int
                - name : String
                - left_hand : Hand
                - right_hand : Hand
                + create GestureDto(id: int, name: String, left_hand: Hand, right_hand: Hand)
                + getId(): int
                + getName(): String
                + getLeftHand(): Hand
                + getRightHand(): Hand
            }

            class Hand {
                - _roll : float
                - _pitch : float
                - _yaw : float
                - _finger_flex : float
                - _mean_acceleration : float
                - _std_acceleration : float
                - _mean_angular_velocity : float
                - _std_angular_velocity : float
                - gyro_axis : MovementAxis
                - accel_axis : MovementAxis
                + create Hand(roll: float, pitch: float, yaw: float, finger_flex: float, mean_acceleration: float, std_acceleration: float, mean_angular_velocity: float, std_angular_velocity: float, gyro_axis: MovementAxis, accel_axis: MovementAxis)
                + getRoll(): float
                + getPitch(): float
                + getYaw(): float
                + getFingerFlex(): float
                + getMeanAcceleration(): float
                + getStdAcceleration(): float
                + getMeanAngularVelocity(): float
                + getStdAngularVelocity(): float
                + getGyroAxis(): MovementAxis
                + getAccelAxis(): MovementAxis
            }

            enum MovementAxis {
                X
                Y
                Z
            }
        }

        package "Factories" {
            interface HandFactory {
                + createHand(roll: float, pitch: float, yaw: float, finger_flex: float, mean_acceleration: float, std_acceleration: float, mean_angular_velocity: float, std_angular_velocity: float, gyro_axis: MovementAxis, accel_axis: MovementAxis): Hand
            }

            class ConcreteHandFactory implements HandFactory {
                + createHand(roll: float, pitch: float, yaw: float, finger_flex: float, mean_acceleration: float, std_acceleration: float, mean_angular_velocity: float, std_angular_velocity: float, gyro_axis: MovementAxis, accel_axis: MovementAxis): Hand
            }
        }
    }

    package "SpeechProcessing" {
        package "Controllers" {
            class SpeechApiController {
                - _tts : TTSConverter
                - _file_controller : SpeechFileManager
                + create SpeechApiController()
                + play_speech_file()
            }
        }

        package "Services" {
            class SpeechFileManager {
                - playback_thread : None
                - file_path : file_path
                + create SpeechFileManager()
                + delete_speech_file()
                + _play_audio()
                + play_speech_file()
            }
        }

        package "Models" {
            class TTSConverter {
                - tts : TTS(model_name)
                - output_file : resources/audioResources/audioTracks/audio.wav
                - speaker_wav : resources/audioResources/speaker.wav
                - language : es
                - engine : pyttsx3.init()
                + create TTSConverter()
                + convert_text_to_audio(text : PythonStr, speaker.wav : PythonStr = None, language : PythonStr = None)
                + convert_text_to_audio_with_engine(text : PythonStr)
            }
        }
    }

    package "SensorCalibration" {
        package "Controllers" {
            class BNO055Calibrator {
                - _serial_data_queue : serial_data_queue
                - _stop_event : stop_event
                - _last_saved_calibration : None
                + create BNO055Calibrator(data_source)
                + get_calibration_data(data_source)
                + _perform_calibration(routine(senser_name))
                + _wait_for_calibration(data_source, sensor_name)
                + calibrate()
            }
        }

        package "Models" {
            class SerialPortReader {
                - port_left : str
                - port_right : str
                - baud_rate : int
                - timeout : float
                - _data_queue : Queue
                - _stop_event : Event
                - ser_left : Serial
                - ser_right : Serial
                - __data_left : None
                - __data_right : None
                - __expected_lengths : list
                + SerialPortReader(port_left: str, port_right: str, data_queue: Queue, stop_event: Event, baud_rate: int = 115200, timeout: float = 0.3)
                + start()
                + stop()
                - __reset_arduino()
                - __is_port_in_use(port: str)
                - __low_pass_filter(string_left: str, string_right: str)
                - __close_ports()
            }
        }
    }

    package "Main" {
        class Main {
            + script_dir
            + processor
        }
    }

    ' Relationships
    GestureRecognition.Controllers.ApiController --> GestureRecognition.Services.GestureService
    GestureRecognition.Controllers.ApiController --> GestureRecognition.Services.GestureMapperService
    GestureRecognition.Controllers.ApiController --> GestureRecognition.Repositories.GestureRepository
    GestureRecognition.Controllers.ApiController --> GestureRecognition.Models.Hand
    GestureRecognition.Controllers.ApiController --> SpeechProcessing.Models.TTSConverter
    GestureRecognition.Controllers.ApiController --> SpeechProcessing.Services.SpeechFileManager
    GestureRecognition.Controllers.ApiController --> SensorCalibration.Models.SerialPortReader
    GestureRecognition.Controllers.ApiController --> SensorCalibration.Controllers.BNO055Calibrator

    SpeechProcessing.Controllers.SpeechApiController --> SpeechProcessing.Models.TTSConverter
    SpeechProcessing.Controllers.SpeechApiController --> SpeechProcessing.Services.SpeechFileManager

    SensorCalibration.Controllers.BNO055Calibrator --> SensorCalibration.Models.SerialPortReader

    GestureRecognition.Services.GestureService --> GestureRecognition.Factories.HandFactory
    GestureRecognition.Models.Gesture --> GestureRecognition.Models.Hand
    GestureRecognition.Models.GestureDto --> GestureRecognition.Models.Hand
    GestureRecognition.Factories.ConcreteHandFactory --> GestureRecognition.Models.Hand
}

@enduml
"""

# Function to render PlantUML code
def render_plantuml(plantuml_code):
    server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
    image_data = server.processes(plantuml_code)
    image_stream = io.BytesIO(image_data)
    image = plt.imread(image_stream, format='png')
    return image

# Render and display the PlantUML diagram
image = render_plantuml(plantuml_code)
plt.figure(figsize=(30, 30))
plt.imshow(image)
plt.axis('off')
plt.show()
