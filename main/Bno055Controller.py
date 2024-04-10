import serial
import time
        
try:
    serIzq = serial.Serial('COM8', 115200, timeout=1)
    serDer = serial.Serial('COM7', 115200, timeout=1)

    time.sleep(2)  # wait for the connection to initialize

    while True:
        try:
            dataIzq = serIzq.readline().decode('utf-8').rstrip()
            dataDer = serDer.readline().decode('utf-8').rstrip()
            if dataIzq and dataDer:
                print(dataIzq)
                print(dataDer)
        except KeyboardInterrupt:
            print("Program terminated")
            break

except serial.SerialException as e:
    print(f"Error opening the serial port: {e}")
except PermissionError as e:
    print(f"Permission denied accessing the serial port: {e}. Try running as Administrator or using sudo.")
