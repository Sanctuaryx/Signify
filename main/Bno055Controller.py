import serial
import time
from queue import Queue
    
    
def start_serial_ports(queue, stop_event):    
    try:
        serIzq = serial.Serial('COM8', 115200, timeout=1)
        serDer = serial.Serial('COM7', 115200, timeout=1)

        time.sleep(2)  # wait for the connection to initialize

        while not stop_event.is_set():
                dataIzq = serIzq.readline().decode('utf-8').rstrip()
                dataDer = serDer.readline().decode('utf-8').rstrip()
                if dataIzq and dataDer:
                    queue.put(dataIzq, dataDer)
                    return dataIzq, dataDer

    except serial.SerialException as e:
        print(f"Error opening the serial port: {e}")
    except PermissionError as e:
        print(f"Permission denied accessing the serial port: {e}. Try running as Administrator or using sudo.")
    
    
