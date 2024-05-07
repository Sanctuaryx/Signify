import threading

import main.Bno055Controller
import main.Calibration
import main.CloudSync
import main.GestureClass

import math
import socket
import time
from struct import unpack_from
import threading
from queue import Queue
import numpy as np
import pandas as pd
from sklearn import tree as ml
import serial

import serial as ser
from pyquaternion import Quaternion
from serial import tools
from serial.serialutil import SerialException
from serial.tools import list_ports

class GestureProcessor:
    def __init__(self, cooldown_time=2):
        self.last_gesture = None
        self.last_gesture_time = 0
        self.cooldown_time = cooldown_time
        self.serial_data_queue = Queue(maxsize=100)
        self.stop_event = threading.Event()
        self.serial_data_thread = threading.Thread(target=self.read_serial_ports)
        self.serial_data_thread.start()

    def read_serial_ports(self):
        """Function to read data from the serial ports."""
        main.Bno055Controller.start_serial_ports(self.serial_data_queue, self.stop_event)

    def is_calibration_needed(self, calibration_izq, calibration_der):
        """Check if calibration is needed based on the calibration data."""
        return any(value < 2 for value in calibration_izq) or any(value < 2 for value in calibration_der)

    def process_gesture(self, gesture):
        """Process a recognized gesture and ensure it follows the cooldown rules."""
        current_time = time.time()
        if gesture and (gesture != self.last_gesture or current_time - self.last_gesture_time > self.cooldown_time):
            print(f"Recognized gesture: {gesture}")
            main.CloudSync.send_data(gesture)
            self.last_gesture = gesture
            self.last_gesture_time = current_time
    
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
            while True:
                if not self.serial_data_queue.empty():
                    data_izq, data_der = self.serial_data_queue.get()
                    euler_izq, flexors_izq, calibration_izq = self.parse_sensor_data(data_izq)
                    euler_der, flexors_der, calibration_der = self.parse_sensor_data(data_der)

                    if self.is_calibration_needed(calibration_izq, calibration_der):
                        print("Calibrating needed...")
                        main.Calibration.BNO055Calibrator(self.serial_data_queue)
                        self.serial_data_queue.queue.clear()
                    else:
                        gesture = main.GestureClass.recognize_letter(euler_izq, euler_der, flexors_izq, flexors_der)
                        if gesture:
                            self.process_gesture(gesture)

        except KeyboardInterrupt:
            print("Stopping...")
            self.stop_event.set()  # Signal the thread to stop
            self.serial_data_thread.join()  # Wait for the thread to finish


processor = GestureProcessor(cooldown_time=2)
processor.run()
