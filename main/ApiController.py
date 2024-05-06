import threading

import main.Bno055Controller
import main.Calibration
import main.CloudSync

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

gestures = {
    'A': lambda eul, flx: eul[0] > 50 and -10 <= eul[1] <= 10 and -10 <= eul[2] <= 10 and all(f < 30 for f in flx),  # Roll > 50, all fingers flexed
    'B': lambda eul, flx: eul[1] < 50 and eul[2] < 50 and sum(f < 50 for f in flx) > len(flx) / 2,  # Pitch < 20, majority of fingers lightly flexed
    'C': lambda eul, flx: eul[2] > 45 and any(f > 40 for f in flx),  # Yaw > 45, any finger significantly flexed
    'D': lambda eul, flx: eul[0] < -30 and flx[0] < 20 and all(f < 20 for f in flx[1:]),  # Negative roll, thumb less flexed, other fingers flat
    'E': lambda eul, flx: abs(eul[1]) > 30 and flx[2] < 15,  # Absolute pitch over 30, middle finger very flat
    'F': lambda eul, flx: abs(eul[2]) < 10 and all(f > 45 for f in flx),  # Low yaw variation, all fingers highly flexed
    
}

def check_gestures(euler, flexors):
    """
    Checks the given position, angle, and flexor data against predefined gestures.

    Args:
        position (list): The position data.
        angle (list): The angle data.
        flexors (list): The flexor data.

    Returns:
        str or None: The recognized gesture letter if a gesture is matched, None otherwise.

    """
    return next((letter for letter, cond in gestures.items() if cond(euler, flexors)), None)


def read_serial_data():
    """
    Reads serial data from a queue and processes it.

    This function starts a thread to read data from a serial port and continuously
    processes the data until the program is interrupted by a keyboard interrupt.

    """
    
    # Event object used to send the stop signal to the serial port reading thread
    stop_event = threading.Event()
    # Queue used to store the received serial data
    serial_data_queue = Queue(maxsize=100)
    # Thread used to read data from the serial port
    serial_data_thread = threading.Thread(target=main.Bno055Controller.start_serial_ports, args=(serial_data_queue, stop_event))
    serial_data_thread.start()

    try:
        while True:
            if not serial_data_queue.empty():
                dataIzq, dataDer = serial_data_queue.get()
                euler_izq, flexors_izq, calibration_izq = parse_sensor_data(dataIzq)
                euler_der, flexors_der, calibration_der = parse_sensor_data(dataDer)
                
                if calibration_der[0] < 2 or calibration_izq[0] < 2 or calibration_der[1] < 2 or calibration_izq[1] < 2 or calibration_der[2] < 2 or calibration_izq[2] < 2 or calibration_der[3] < 2 or calibration_izq[3] < 2:
                    print("Calibrating needed...")
                    main.Calibration.calibrate(euler_izq, euler_der)
                    serial_data_queue.queue.clear()
                else:
                    
                    gesture = check_gestures(euler_izq, euler_der, flexors_izq, flexors_der)
                    if gesture:
                        print(f"Recognized gesture: {gesture}")
                        main.CloudSync.send_data(gesture)
                
            
    except KeyboardInterrupt:
        print("Stopping...")
        stop_event.set()  # Signal the thread to stop
        serial_data_thread.join()  # Wait for the thread to finish

def parse_sensor_data(data):
    """
    Parses the sensor data received from the serial port.
    
    Args:
        data (str): The raw sensor data received from the serial port.
        
    Returns:
        tuple: A tuple containing the position, angle, and flexor data as lists.
        
    """
    
    splitData = [part for part in data.strip('*').split('*') if part]
    
    if len(splitData) != 3:
        print("Error: Unexpected data format")
        return None
    
    quat = list(map(float, splitData[0].split(',')))
    flexors = list(map(float, splitData[1].split(',')))
    Calibration = list(map(float, splitData[2].split(',')))
    
    roll=math.atan2(2*(quat[0]*quat[1]+quat[2]*quat[3]),1-2*(quat[1]*quat[1]+quat[2]*quat[2]))
    pitch=math.asin(2*(quat[0]*quat[2]-quat[3]*quat[1]))
    yaw=math.atan2(2*(quat[0]*quat[3]+quat[1]*quat[2]),1-2*(quat[2]*quat[2]+quat[3]*quat[3]))-np.pi/2

    return [roll, pitch, yaw], flexors, Calibration
