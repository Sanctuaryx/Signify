# /main/Calibration.py

import time

class BNO055Calibrator:
    """Class for calibrating BNO055 sensors."""

    def __init__(self, serial_data_queue):
        """
        Initialize the calibrator with a reference to an existing data queue.
        
        :param serial_data_queue: A queue object that provides sensor data.
        """
        self.serial_data_queue = serial_data_queue
        print('Calibrator initialized successfully.')


    def _get_calibration_data(self, data_source):
        """
        Retrieve calibration data from the queue for the specified sensor index.

        :param data_source: Index (0 for left, 1 for right) to specify sensor.
        :return: List of calibration values as floats.
        """
        data = self.serial_data_queue.get()[data_source]
        return list(map(float, data[2].split(',')))

    def _perform_calibration_routine(self, sensor_name):
        """
        Display calibration instructions to the user for the specified sensor.

        :param sensor_name: Name of the sensor (left or right) for user instructions.
        """
        print(f"Calibrating {sensor_name} BNO055 sensor...")
        instructions = [
            "Please keep the sensor steady.",
            "Please, move the sensor in a figure-8 pattern.",
            "Please, move the sensor in a circular pattern.",
            "Please, rotate the sensor 180 degrees in all directions."
        ]
        for instruction in instructions:
            print(instruction)
            time.sleep(1)

    def _wait_for_calibration(self, data_source, sensor_name):
        """
        Continuously check and guide calibration until the sensor is fully calibrated.

        :param data_source: Sensor index (0 for left, 1 for right).
        :param sensor_name: Name of the sensor for display purposes.
        """
        calibration = self._get_calibration_data(data_source)
        while all(value < 2 for value in calibration):
            self._perform_calibration_routine(sensor_name)
            calibration = self._get_calibration_data(data_source)

    def calibrate(self):
        """
        Perform calibration routines for both sensors.

        :return: Calibration data tuple for both sensors.
        """
        print("Starting calibration of both sensors.")
        self._wait_for_calibration(0, "left")
        self._wait_for_calibration(1, "right")
        print("BNO055 sensors calibrated.")