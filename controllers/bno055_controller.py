import serial
import time
from queue import Queue
import psutil
from threading import Event
import numpy as np

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
        self.__data_left = None
        self.__data_right = None
        self.__expected_lengths = [3, 3, 3, 5, 4]
        
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
                if self._data_queue.not_full and self.__low_pass_filter(data_left, data_right):
                    self._data_queue.put((self.__data_left, self.__data_right))
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
    
    def __low_pass_filter(self, string_left: str, string_right: str):
        """
        Applies a low-pass filter to the input strings and returns wether the filtered data is usable or not.

        Args:
            string_left (str): The left string to be filtered.
            string_right (str): The right string to be filtered.

        Returns:
            bool: True if the filtering is successful, False otherwise.
        """
        def validate_and_parse(string: str):
            """
            Validates and parses a string into a list of float arrays.

            Args:
                string (str): The string to be validated and parsed.

            Returns:
                list: A list of float arrays if the string is valid and can be parsed, None otherwise.
            """
            segments = string.split('*')
            
            # Validate the number of segments
            if len(segments) != len(self.__expected_lengths):
                return None
            
            try:
                # Split each segment by ',' and convert to float arrays
                parsed_data = [
                    np.fromstring(segment, sep=',', dtype=float)
                    for segment in segments
                ]
                
                # Validate the length of each segment
                if any(len(elements) != expected_length 
                    for elements, expected_length in zip(parsed_data, self.__expected_lengths)):
                    return None
            except ValueError:
                return None
            
            return parsed_data
        
        self.__data_left = validate_and_parse(string_left)
        self.__data_right = validate_and_parse(string_right)
        
        if self.__data_left is None or self.__data_right is None:
            return False
        
        return True

    def __close_ports(self):
        """Close the serial ports if they are open."""
        if self.ser_left and self.ser_left.is_open:
            self.ser_left.close()
        if self.ser_right and self.ser_right.is_open:
            self.ser_right.close()
            
    def stop(self):
        self._stop_event.set()

