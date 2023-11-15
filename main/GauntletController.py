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

# Sensor calibration
adafruit_bno055.calibrate()

# Setup serial connection (adjust the COM port as needed)
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Wait for connection to establish

# reading of the data from the sensor
def read_serial_data():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        return line

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