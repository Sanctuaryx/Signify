import Bno055Controller
import Calibration
import CloudSync

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

# Event object used to send the stop signal to the serial port reading thread
stop_event = threading.Event()
# Queue used to store the received serial data
serial_data_queue = Queue()
# Thread used to read data from the serial port
serial_data_thread = threading.Thread(target=Bno055Controller.start_serial_ports, args=(serial_data_queue, stop_event))

gestures = {
    'A': lambda pos, ang, flx: pos[0] > 50 and all(f < 30 for f in flx),
    'B': lambda pos, ang, flx: pos[1] < 20 and sum(f < 50 for f in flx) > len(flx) / 2,
    'C': lambda pos, ang, flx: ang[2] > 45 and any(f > 40 for f in flx),
    # Define similar conditions for other letters...
}

def check_gestures(position, angle, flexors):
    """
    Checks the given position, angle, and flexor data against predefined gestures.

    Args:
        position (list): The position data.
        angle (list): The angle data.
        flexors (list): The flexor data.

    Returns:
        str or None: The recognized gesture letter if a gesture is matched, None otherwise.

    """
    return next((letter for letter, cond in gestures.items() if cond(position, angle, flexors)), None)


def read_serial_data():
    """
    Reads serial data from a queue and processes it.

    This function starts a thread to read data from a serial port and continuously
    processes the data until the program is interrupted by a keyboard interrupt.

    """
    serial_data_thread.start()

    try:
        while True:
            if not serial_data_queue.empty():
                dataIzq, dataDer = serial_data_queue.get()
                quat_izq, flexors_izq, Calibration_izq = parse_sensor_data(dataIzq)
                quat_der, flexors_der, Calibration_der = parse_sensor_data(dataDer)
            
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
    
    # Convert each part to a list of floats
    quat = list(map(float, splitData[0].split(',')))
    flexors = list(map(float, splitData[1].split(',')))
    Calibration = list(map(float, splitData[2].split(',')))
    

    return quat, flexors, Calibration
