import Bno055Controller
import FlexorController
import Calibration
import CloudSync
import DataHandler
import WordTransformer

import math
import socket
import time
from struct import unpack_from
import numpy as np
import pandas as pd
from sklearn import tree as ml
import serial

import serial as ser
from pyquaternion import Quaternion
from serial import tools
from serial.serialutil import SerialException
from serial.tools import list_ports

#This driver takes an instantiated and active I2C object as an argument to its constructor.
#i2c = board.I2C()
#sensor = adafruit_bno055.BNO055_I2C(i2c)

# reading of the data from the sensor
def read_serial_data():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        return line

# def calibrate_bno055(sensor):
    # sensor.mode = Mode.NDOF_MODE
    
    # Calibration.perform_calibration(sensor, sensor, flexors)
    
# Data filtering setup
# def filter_data(raw_data):
    # Apply your chosen filter here
    # return filtered_data

# Gesture recognition setup
# def extract_features(sensor_data):
    # Extract features suitable for machine learning
    # return features

def train_model(features, labels):
    # Train your machine learning model
    model = ml.DecisionTreeClassifier()  # Example model
    model.fit(features, labels)
    return model

def read_serial_data():
    """
    Reads data from a serial port and prints it to the console.

    This function opens a serial port connection, reads data from it, and prints the received data to the console.
    It continuously reads data until the program is terminated by a keyboard interrupt.

    Raises:
        serial.SerialException: If there is an error opening the serial port.
        PermissionError: If permission is denied when accessing the serial port.

    """
    try:
        ser = serial.Serial('COM8', 115200, timeout=1)
        time.sleep(2)  # wait for the connection to initialize

        # Load or train your machine learning model
        # model = train_model(training_features, training_labels)
        # Main loop
        while True:
            try:
                data = ser.readline().decode('utf-8').rstrip()
                if data:
                    # filtered_data = filter_data(raw_data)
                    # features = extract_features(filtered_data)
    
                    # Gesture recognition
                    #gesture = model.predict([features])[0]  # Predict the gesture
    
                    # Mapping gesture to word
                    # word = gesture_to_word_mapping.get(gesture, "")
                    # if word:
                    #print(f"The gesture means: {word}")
                    print(data)
            except KeyboardInterrupt:
                print("Program terminated")
                break

    except serial.SerialException as e:
        print(f"Error opening the serial port: {e}")
    except PermissionError as e:
        print(f"Permission denied accessing the serial port: {e}. Try running as Administrator or using sudo.")
