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
        self.instructions = instructions = [
            "Please, keep the glove horizontal in front of you and remain steady.",
            "Please, rotate the glove 180 degrees and keep it steady.",
            "Please, rotate the glove 90 degrees and keep it steady.",
            "Please, rotate the glove so your palm faces the oposite direction and keep it steady.",
            "Please, move the glove in a figure-8 pattern.",
            "Please, move the glove in a circular pattern.",
            "Please, raise the glove verticaly and keep it steady.",
            "Please, rotate the glove, keeping it steady every few seconds."
            ]
        
        print('Calibrator initialized successfully.')


    def _get_calibration_data(self, data_source):
        """
        Retrieve calibration data from the queue for the specified sensor index.

        :param data_source: Index (0 for left, 1 for right) to specify sensor.
        :return: List of calibration values as floats.
        """
        data_izq, data_der = self.serial_data_queue.get()
        if data_source == 0:
            data = data_izq.split('*')
        else:
            data = data_der.split('*')
        return [int(item) for item in data[2].split(',')]

    def _perform_calibration_routine(self, sensor_name):
        """
        Display calibration instructions to the user for the specified sensor.

        :param sensor_name: Name of the sensor (left or right) for user instructions.
        """
        print(f"Calibrating {sensor_name} BNO055 sensor...")
        
        for instruction in self.instructions:
            print(instruction)
            with self.serial_data_queue.mutex: self.serial_data_queue.queue.clear()
            print(self._get_calibration_data(0))
            time.sleep(7)

    def _wait_for_calibration(self, data_source, sensor_name):
        """
        Continuously check and guide calibration until the sensor is fully calibrated.

        :param data_source: Sensor index (0 for left, 1 for right).
        :param sensor_name: Name of the sensor for display purposes.
        """
        while True:
            self._perform_calibration_routine(sensor_name)
            calibration = self._get_calibration_data(data_source)
            if all(value == 3 for value in calibration):
                break
            print(f"{sensor_name} sensor not fully calibrated. Retrying...")

    def calibrate(self):
        """
        Perform calibration routines for both sensors.

        :return: Calibration data tuple for both sensors.
        """
        print("Starting calibration of both sensors.")
        self._wait_for_calibration(0, "left")
        self._wait_for_calibration(1, "right")
        print("BNO055 sensors calibrated.")