import Calibration
import math
import socket
import time
from struct import unpack_from

import serial
from pyquaternion import Quaternion
from serial import tools
from serial.serialutil import SerialException
from serial.tools import list_ports
import adafruit_bno055
import WordTransformer
import board

class Mode:
    CONFIG_MODE = 0x00
    ACCONLY_MODE = 0x01
    MAGONLY_MODE = 0x02
    GYRONLY_MODE = 0x03
    ACCMAG_MODE = 0x04
    ACCGYRO_MODE = 0x05
    MAGGYRO_MODE = 0x06
    AMG_MODE = 0x07
    IMUPLUS_MODE = 0x08
    COMPASS_MODE = 0x09
    M4G_MODE = 0x0A
    NDOF_FMC_OFF_MODE = 0x0B
    NDOF_MODE = 0x0C

#This driver takes an instantiated and active I2C object as an argument to its constructor.
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

last_val = 0xFFFF 
flexors = [0, 1, 2, 3, 4, 5, 6, 7]

# reading of the data from the sensor
def read_serial_data():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        return line

def calibrate_bno055(sensor):
    sensor.mode = Mode.NDOF_MODE
    
    Calibration.perform_calibration(sensor, sensor, flexors)
    
# Data filtering setup
def filter_data(raw_data):
    # Apply your chosen filter here
    return filtered_data

# Gesture recognition setup
def extract_features(sensor_data):
    # Extract features suitable for machine learning
    return features

def train_model(features, labels):
    # Train your machine learning model
    model = ml.DecisionTreeClassifier()  # Example model
    model.fit(features, labels)
    return model

# Load or train your machine learning model
# model = train_model(training_features, training_labels)
# Main loop
while True:
    
    
    raw_data = sensor_library.read_all_sensors()
    filtered_data = filter_data(raw_data)
    features = extract_features(filtered_data)
    
    # Gesture recognition
    gesture = model.predict([features])[0]  # Predict the gesture
    
    # Mapping gesture to word
    word = gesture_to_word_mapping.get(gesture, "")
    if word:
        print(f"The gesture means: {word}")