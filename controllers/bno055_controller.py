# /main/serial_port_reader.py

import serial
import time
from queue import Queue
import psutil
from threading import Event

class SerialPortReader:
    def __init__(self, port_left: str, port_right: str, data_queue: Queue, stop_event: Event, baud_rate: int = 115200, timeout: float = 0.3):
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
            #make sure the ports are not in use
            if self.__is_port_in_use(self.port_left) or self.__is_port_in_use(self.port_right):
                self.__reset_arduino()
                
            # Open the serial ports
            self.ser_left = serial.Serial(self.port_left, self.baud_rate, timeout=self.timeout)
            self.ser_right = serial.Serial(self.port_right, self.baud_rate, timeout=self.timeout)
            print(f"Serial ports {self.port_left} and {self.port_right} opened successfully.")
            # Allow some time for ports to initialize
            time.sleep(4)

            while not self._stop_event.is_set():
                # Read and decode data from both ports
                data_left = self.ser_left.readline().decode('utf-8').rstrip()
                data_right = self.ser_right.readline().decode('utf-8').rstrip()
                    
                # If data is available, put it in the queue
                if data_left and data_right and self._data_queue.not_full:
                    data_left = [part for part in data_left.strip('*').split('*') if part]
                    data_right = [part for part in data_right.strip('*').split('*') if part]
                    if len(data_left) == 5 and len(data_right) == 5:
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
            self.__close_ports()
            
    def __reset_arduino(self):
        """
        Reset the Arduino by toggling the DTR (Data Terminal Ready) line.
        
        :param ser: The serial connection object.
        """
        self.ser_left.close()
        self.ser_right.close()
        time.sleep(1)
        self.ser_left.open()
        self.ser_right.open()
                    
    def __is_port_in_use(self, port):
        """
        Check if a given serial port is currently in use by any process.
        
        :param port: The serial port to check (e.g., 'COM3', '/dev/ttyUSB0').
        :return: Boolean indicating whether the port is in use.
        """
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            for conn in proc.info['connections']:
                if conn.laddr.port == int(port.split('COM')[1]) or port in conn.laddr:
                    return True
        return False

    def __close_ports(self):
        """Close the serial ports if they are open."""
        if self.ser_left and self.ser_left.is_open:
            self.ser_left.close()
        if self.ser_right and self.ser_right.is_open:
            self.ser_right.close()
            
    def stop(self):
        self._stop_event.set()

