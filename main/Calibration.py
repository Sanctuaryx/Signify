# /main/Calibration.py

import time
import sys

class BNO055Calibrator:
    """Class for calibrating BNO055 sensors."""

    def __init__(self, serial_data_queue, stop_event):
        """
        Initialize the calibrator with a reference to an existing data queue.
        
        :param serial_data_queue: A queue object that provides sensor data.
        """
        self._serial_data_queue = serial_data_queue
        self._stop_event = stop_event
        self._last_saved_calibration = None
        
        print('Calibrator initialized successfully.')


    def _get_calibration_data(self, data_source):
        """
        Retrieve calibration data from the queue for the specified sensor index.

        :param data_source: Index (0 for left, 1 for right) to specify sensor.
        :return: List of calibration values as floats.
        """
        try:
            self._serial_data_queue.queue.clear()
            time.sleep(1)
            
            data_izq, data_der = self._serial_data_queue.get()
            if data_source == 0 or data_source == "left":
                data = data_izq.split('*')
            else:
                data = data_der.split('*')
            self._last_saved_calibration = [int(item) for item in data[2].split(',')]
            return self._last_saved_calibration
        
        except Exception:
            return self._last_saved_calibration

    def _perform_calibration_routine(self, sensor_name):
        """
        Display calibration instructions to the user for the specified sensor.

        :param sensor_name: Name of the sensor (left or right) for user instructions.
        """
        self.accel, self.gyro, self.mag, self.sys = self._get_calibration_data(sensor_name)
        print("Calibrating " + sensor_name + " BNO055 sensor...")
     
        print("\nGyroscope Calibration: Place the sensor on a flat surface, then move it slowly in different orientations.")
        while self.gyro < 3 and not self._stop_event.is_set():
            self.accel, self.gyro, self.mag, self.sys = self. _get_calibration_data(sensor_name)          
            sys.stdout.write(f"\rSystem: {self.sys}/3, Gyroscope: {self.gyro}/3, Accelerometer: {self.accel}/3, Magnetometer: {self.mag}/3\n")
            sys.stdout.flush()
            time.sleep(4)
                
        print("\nMagnetometer Calibration: Move the sensor in a figure-eight motion or rotate it around all three axes.")
        while self.mag < 3 and not self._stop_event.is_set():
            self.accel, self.gyro, self.mag, self.sys = self. _get_calibration_data(sensor_name)            
            sys.stdout.write(f"\rSystem: {self.sys}/3, Gyroscope: {self.gyro}/3, Accelerometer: {self.accel}/3, Magnetometer: {self.mag}/3\n")
            sys.stdout.flush()
            time.sleep(4)
            
        print("\nAccelerometer Calibration: Move the sensor in a figure-eight motion.")
        while self.accel < 3 and not self._stop_event.is_set():
            self.accel, self.gyro, self.mag, self.sys = self. _get_calibration_data(sensor_name)            
            sys.stdout.write(f"\rSystem: {self.sys}/3, Gyroscope: {self.gyro}/3, Accelerometer: {self.accel}/3, Magnetometer: {self.mag}/3\n")
            sys.stdout.flush()
            time.sleep(4)
           
    def _wait_for_calibration(self, data_source, sensor_name):
        """
        Continuously check and guide calibration until the sensor is fully calibrated.

        :param data_source: Sensor index (0 for left, 1 for right).
        :param sensor_name: Name of the sensor for display purposes.
        """
        while not self._stop_event.is_set():
            self._perform_calibration_routine(sensor_name)
            calibration = self._get_calibration_data(data_source)
            if all(value > 2 for value in calibration):
                break
            print("\nCalibration failed. Restarting calibration routine.")

    def calibrate(self):
        """
        Perform calibration routines for both sensors.

        :return: Calibration data tuple for both sensors.
        """
        try:
            print("\nStarting calibration of left sensors.")
            self._wait_for_calibration(0, "left")
            print("\nCalibration of left sensors complete, starting right sensors.")
            time.sleep(2)
            self._wait_for_calibration(1, "right")
            print("\nBNO055 sensors calibrated.")
            
        except KeyboardInterrupt:
                self._stop_event.set()