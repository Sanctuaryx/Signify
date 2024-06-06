# /main/serial_port_reader.py

import serial
import time
from queue import Queue
import threading
from threading import Event

class SerialPortReader:
    def __init__(self, port_left: str, port_right: str, data_queue: Queue, stop_event: Event, baud_rate: int = 115200, timeout: float = 0.2):
        """
        Initializes the SerialPortReader class with two serial ports.

        Args:
            port_left (str): The name of the left serial port.
            port_right (str): The name of the right serial port.
            baud_rate (int): The baud rate for both serial ports.
            timeout (float): The timeout for reading data from the serial ports.
        """
        self.port_left = port_left
        self.port_right = port_right
        self.baud_rate = baud_rate
        self.timeout = timeout
        self._data_queue = data_queue
        self._stop_event = stop_event

        # Initialize serial port objects
        self.ser_left = None
        self.ser_right = None
        
        print('BNO055 controller initialized successfully.')


    def start(self):
        """
        Starts reading from the configured serial ports and puts the data into a queue.

        Args:
            data_queue (Queue): The queue to store read data.
            stop_event (Event): An event used to stop the serial reading.
        """
        try:
            # Open the serial ports
            self.ser_left = serial.Serial(self.port_left, self.baud_rate, timeout=self.timeout)
            self.ser_right = serial.Serial(self.port_right, self.baud_rate, timeout=self.timeout)

            print(f"Serial ports {self.port_left} and {self.port_right} opened successfully.")
            # Allow some time for ports to initialize
            time.sleep(2)

            while not self._stop_event.is_set():
                # Read and decode data from both ports
                data_left = self.ser_left.readline().decode('utf-8').rstrip()
                data_right = self.ser_right.readline().decode('utf-8').rstrip()
                    
                # If data is available, put it in the queue
                if data_left and data_right and self._data_queue.not_full:
                    data_left = [part for part in data_left.strip('*').split('*') if part]
                    data_right = [part for part in data_right.strip('*').split('*') if part]
                    if len(data_left) == 3 and len(data_right) == 3:
                        self._data_queue.put((data_left, data_right))
                        
                    self.ser_left.reset_input_buffer()
                    self.ser_right.reset_input_buffer()
                    
        except serial.SerialException as e:
            print(f"Error opening the serial port: {e}")
            self._stop_event.set()
        except PermissionError as e:
            print(f"Permission denied accessing the serial port: {e}. Try running as Administrator or using sudo.")
            self._stop_event.set()
        except Exception as e:
            self._data_queue.get()  # Remove the invalid data
        finally:
            self._close_ports()

    def _close_ports(self):
        """Close the serial ports if they are open."""
        if self.ser_left and self.ser_left.is_open:
            self.ser_left.close()
        if self.ser_right and self.ser_right.is_open:
            self.ser_right.close()
            
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

