import serial
import time
from queue import Queue
    
    
def start_serial_ports(queue, stop_event):    
    try:
        ser_izq = serial.Serial('COM8', 115200, timeout=1)
        ser_der = serial.Serial('COM7', 115200, timeout=1)

        time.sleep(2)  # wait for the connection to initialize

        while not stop_event.is_set():
                data_izq = ser_izq.readline().decode('utf-8').rstrip()
                data_der = ser_der.readline().decode('utf-8').rstrip()
                if data_izq and data_der:
                    queue.put((data_izq, data_der))

    except serial.SerialException as e:
        print(f"Error opening the serial port: {e}")
        print("Stopping...")
        stop_event.set()  # Signal the thread to stop
    except PermissionError as e:
        print(f"Permission denied accessing the serial port: {e}. Try running as Administrator or using sudo.")
        print("Stopping...")
        stop_event.set()  # Signal the thread to stop
    
    
