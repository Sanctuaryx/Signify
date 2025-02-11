# /main/Calibration.py

import time
import sys
from queue import Queue

class BNO055Calibrator:
    """Class for calibrating BNO055 sensors."""

    def __init__(self, serial_data_queue: Queue, stop_event):
        """
        Initialize the calibrator with a reference to an existing data queue.
        
        :param serial_data_queue: A queue object that provides sensor data.
        """
        self.__data_queue = serial_data_queue
        self._stop_event = stop_event
        self._last_saved_calibration = [0,0,0,0]
        
        print('Calibrator initialized successfully.')


    def _get_calibration_data(self, data_source):
        """
        Retrieve calibration data from the queue for the specified sensor index.

        :param data_source: Index (0 for left, 1 for right) to specify sensor.
        :return: List of calibration values as floats.
        """
        if not self.__data_queue.empty():
            try:
                with self.__data_queue.mutex: self.__data_queue.queue.clear()
                time.sleep(1)
                
                data_izq, data_der = self.__data_queue.get()
                if data_source == 0 or data_source == "left":
                    self._last_saved_calibration = list(map(int, data_izq[4]))
                else:
                    self._last_saved_calibration = list(map(int, data_der[4]))
                        
            except Exception:
                return self._last_saved_calibration
        return self._last_saved_calibration

    def _perform_calibration_routine(self, sensor_name):
        """
        Display calibration instructions to the user for the specified sensor.

        :param sensor_name: Name of the sensor (left or right) for user instructions.
        """
        self.accel, self.gyro, self.mag, self.sys = self._get_calibration_data(sensor_name)
        print("Calibrating " + sensor_name + " BNO055 sensor...")
     
        print("\nGyroscope Calibration: Place the sensor on a flat surface.")
        while self.gyro < 3 and not self._stop_event.is_set():
            self.accel, self.gyro, self.mag, self.sys = self. _get_calibration_data(sensor_name)          
            sys.stdout.write(f"\rSystem: {self.sys}/3, Gyroscope: {self.gyro}/3, Accelerometer: {self.accel}/3, Magnetometer: {self.mag}/3")
            sys.stdout.flush()
                
        print("\nMagnetometer Calibration: Move the sensor slowly in different orientations while rotating it around all three axes.")
        while self.mag < 3 and not self._stop_event.is_set():
            self.accel, self.gyro, self.mag, self.sys = self. _get_calibration_data(sensor_name)            
            sys.stdout.write(f"\rSystem: {self.sys}/3, Gyroscope: {self.gyro}/3, Accelerometer: {self.accel}/3, Magnetometer: {self.mag}/3")
            sys.stdout.flush()
            
        print("\nAccelerometer Calibration: Move the sensor slowly in a figure-eight motion around all three axes.")
        while self.accel < 3 and not self._stop_event.is_set():
            self.accel, self.gyro, self.mag, self.sys = self. _get_calibration_data(sensor_name)            
            sys.stdout.write(f"\rSystem: {self.sys}/3, Gyroscope: {self.gyro}/3, Accelerometer: {self.accel}/3, Magnetometer: {self.mag}/3")
            sys.stdout.flush()
           
    def _wait_for_calibration(self, data_source, sensor_name):
        """
        Continuously check and guide calibration until the sensor is fully calibrated.

        :param data_source: Sensor index (0 for left, 1 for right).
        :param sensor_name: Name of the sensor for display purposes.
        """
        
        self._perform_calibration_routine(sensor_name)
        self._get_calibration_data(data_source)
        

    def calibrate(self):
        """
        Perform calibration routines for both sensors.

        :return: Calibration data tuple for both sensors.
        """
        try:
            print("\nStarting calibration of left sensor.")
            self._wait_for_calibration(0, "left")
            print("\nCalibration of left sensors complete, starting right sensor.")
            self._wait_for_calibration(1, "right")
            print("\nBNO055 sensors calibrated.")
            
        except KeyboardInterrupt:
                self._stop_event.set()