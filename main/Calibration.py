from adafruit_bno055 import BNO055
import time


def calibrate_bno055(bno):
    """
    Calibrates the BNO055 sensor.

    Returns: tuple: A tuple containing the calibration data for the BNO055 sensor.
    """    
    sys, gyro, accel, mag = bno.calibrate()
    while sys != 3 and gyro != 3 and accel != 3 and mag != 3:
        sys, gyro, accel, mag = bno.calibration_status
        time.sleep(1)
            
    return bno.get_calibration()


def calibrate_flexors(flexors):
    """
    Calibrates the range for the flexor sensors. 
    """
    pass
    
    

def perform_calibration(bno_one, bno_two, flexors):
    """
    Performs calibration for the BNO055 and flexor sensors.

    Returns: tuple: A tuple containing the calibration data for the BNO055 and flexor sensors.
    """ 
    bno_calibration_one = calibrate_bno055(bno_one)
    bno_calibration_two = calibrate_bno055(bno_two)

    flexor_calibration = calibrate_flexors(flexors)
    return (bno_calibration_one, bno_calibration_two, flexor_calibration)
