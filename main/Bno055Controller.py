import serial
import time
        
try:
    ser = serial.Serial('COM8', 115200, timeout=1)
    time.sleep(2)  # wait for the connection to initialize

    while True:
        try:
            data = ser.readline().decode('utf-8').rstrip()
            if data:
                print(data)
        except KeyboardInterrupt:
            print("Program terminated")
            break

except serial.SerialException as e:
    print(f"Error opening the serial port: {e}")
except PermissionError as e:
    print(f"Permission denied accessing the serial port: {e}. Try running as Administrator or using sudo.")
