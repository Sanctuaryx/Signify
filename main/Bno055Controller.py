"""
`adafruit_bno055`
=======================================================================================

This is a CircuitPython driver for the Bosch BNO055 nine degree of freedom
inertial measurement unit module with sensor fusion.

* Author(s): Raúl Juan García

* Adafruit `9-DOF Absolute Orientation IMU Fusion Breakout - BNO055
  <https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor>`_ (Product ID: 4646)


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register

"""
import time
import struct

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_struct import Struct, UnaryStruct

try:
    from typing import Any, Optional, Tuple, Type, Union
    from busio import I2C, UART
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BNO055.git"

NOT_IMPLEMENTED_MSG = "NOT_IMPLEMENTED_MSG"
ERROR_MSG = "Mode must not be a fusion mode"


_CHIP_ID = const(0xA0)

CONFIG_MODE = const(0x00) # Default mode
ACCONLY_MODE = const(0x01) # Accelerometer only
MAGONLY_MODE = const(0x02) # Magnetometer only
GYRONLY_MODE = const(0x03) # Gyroscope only
ACCMAG_MODE = const(0x04) # Accelerometer and magnetometer only
ACCGYRO_MODE = const(0x05) # Accelerometer and gyroscope only
MAGGYRO_MODE = const(0x06) # Magnetometer and gyroscope only
AMG_MODE = const(0x07) # Accelerometer, magnetometer, and gyroscope 
IMUPLUS_MODE = const(0x08) 
COMPASS_MODE = const(0x09) 
M4G_MODE = const(0x0A) 
NDOF_FMC_OFF_MODE = const(0x0B) 
NDOF_MODE = const(0x0C) 

ACCEL_2G = const(0x00)  # accel_range property
ACCEL_4G = const(0x01)  # Default
ACCEL_8G = const(0x02) 
ACCEL_16G = const(0x03)

ACCEL_7_81HZ = const(0x00)  # accel_bandwidth property
ACCEL_15_63HZ = const(0x04)
ACCEL_31_25HZ = const(0x08)
ACCEL_62_5HZ = const(0x0C)  # Default
ACCEL_125HZ = const(0x10)
ACCEL_250HZ = const(0x14)
ACCEL_500HZ = const(0x18)
ACCEL_1000HZ = const(0x1C)

ACCEL_NORMAL_MODE = const(0x00)  # Default. accel_mode property
ACCEL_SUSPEND_MODE = const(0x20)
ACCEL_LOWPOWER1_MODE = const(0x40)
ACCEL_STANDBY_MODE = const(0x60)
ACCEL_LOWPOWER2_MODE = const(0x80)
ACCEL_DEEPSUSPEND_MODE = const(0xA0)

GYRO_2000_DPS = const(0x00)  # Default. gyro_range property
GYRO_1000_DPS = const(0x01)
GYRO_500_DPS = const(0x02)
GYRO_250_DPS = const(0x03)
GYRO_125_DPS = const(0x04)

GYRO_523HZ = const(0x00)  # gyro_bandwidth property
GYRO_230HZ = const(0x08)
GYRO_116HZ = const(0x10)
GYRO_47HZ = const(0x18)
GYRO_23HZ = const(0x20)
GYRO_12HZ = const(0x28)
GYRO_64HZ = const(0x30)
GYRO_32HZ = const(0x38)  # Default

GYRO_NORMAL_MODE = const(0x00)  # Default. gyro_mode property
GYRO_FASTPOWERUP_MODE = const(0x01) # Fast power up mode
GYRO_DEEPSUSPEND_MODE = const(0x02) # Deep suspend mode
GYRO_SUSPEND_MODE = const(0x03) # Suspend mode
GYRO_ADVANCEDPOWERSAVE_MODE = const(0x04) # Advanced power save mode

MAGNET_2HZ = const(0x00)  # magnet_rate property
MAGNET_6HZ = const(0x01)
MAGNET_8HZ = const(0x02)
MAGNET_10HZ = const(0x03)
MAGNET_15HZ = const(0x04)
MAGNET_20HZ = const(0x05)  # Default
MAGNET_25HZ = const(0x06)
MAGNET_30HZ = const(0x07)

MAGNET_LOWPOWER_MODE = const(0x00)  # magnet_operation_mode property
MAGNET_REGULAR_MODE = const(0x08)  # Default
MAGNET_ENHANCEDREGULAR_MODE = const(0x10)
MAGNET_ACCURACY_MODE = const(0x18)

MAGNET_NORMAL_MODE = const(0x00)  # magnet_power_mode property
MAGNET_SLEEP_MODE = const(0x20)
MAGNET_SUSPEND_MODE = const(0x40)
MAGNET_FORCEMODE_MODE = const(0x60)  # Default

_POWER_NORMAL = const(0x00) # power_mode property
_POWER_LOW = const(0x01) # Low power mode
_POWER_SUSPEND = const(0x02) # Suspend mode

_MODE_REGISTER = const(0x3D) 
_PAGE_REGISTER = const(0x07) 
_ACCEL_CONFIG_REGISTER = const(0x08)
_MAGNET_CONFIG_REGISTER = const(0x09)
_GYRO_CONFIG_0_REGISTER = const(0x0A)
_GYRO_CONFIG_1_REGISTER = const(0x0B)
_CALIBRATION_REGISTER = const(0x35)
_OFFSET_ACCEL_REGISTER = const(0x55)
_OFFSET_MAGNET_REGISTER = const(0x5B)
_OFFSET_GYRO_REGISTER = const(0x61)
_RADIUS_ACCEL_REGISTER = const(0x67)
_RADIUS_MAGNET_REGISTER = const(0x69)
_TRIGGER_REGISTER = const(0x3F)
_POWER_REGISTER = const(0x3E)
_ID_REGISTER = const(0x00)

# Axis remap registers and values
_AXIS_MAP_CONFIG_REGISTER = const(0x41) 
_AXIS_MAP_SIGN_REGISTER = const(0x42)
AXIS_REMAP_X = const(0x00)
AXIS_REMAP_Y = const(0x01)
AXIS_REMAP_Z = const(0x02)
AXIS_REMAP_POSITIVE = const(0x00)
AXIS_REMAP_NEGATIVE = const(0x01)


class _ScaledReadOnlyStruct(Struct):  
    """
    Represents a scaled read-only struct.

    Attributes:
        register_address (int): The register address of the struct.
        struct_format (str): The format string specifying the struct's layout.
        scale (float): The scaling factor for the values returned by the `__get__` method.
    """
    def __init__(self, register_address: int, struct_format: str, scale: float) -> None:
        super().__init__(register_address, struct_format) 
        self.scale = scale

    def __get__(
        self, obj: Optional["BNO055_I2C"], objtype: Optional[Type["BNO055_I2C"]] = None
    ) -> Tuple[float, float, float]:
        """
        Get the scaled values of the struct.

        Args:
            obj (Optional[BNO055_I2C]): The instance of the BNO055_I2C class.
            objtype (Optional[Type[BNO055_I2C]]): The type of the BNO055_I2C class.

        Returns:
            Tuple[float, float, float]: The scaled values of the struct.
        """
        result = super().__get__(obj, objtype)
        return tuple(self.scale * v for v in result)

    def __set__(self, obj: Optional["BNO055_I2C"], value: Any) -> None:
        """
        Set the value of the struct (not implemented).

        Args:
            obj (Optional[BNO055_I2C]): The instance of the BNO055_I2C class.
            value (Any): The value to be set.

        Raises:
            NotImplementedError: This method is not implemented.
        """
        raise NotImplementedError()



class _ReadOnlyUnaryStruct(UnaryStruct):
    """
    Represents a read-only unary struct.

    This class is used to define a descriptor
    that allows read-only access to a single value within a struct.

    Attributes:
        None

    Methods:
        __set__(self, obj: Optional["BNO055_I2C"], value: Any) -> None:
            Raises a NotImplementedError when attempting to set the value of the struct.

    """
    def __set__(self, obj: Optional["BNO055_I2C"], value: Any) -> None:
        raise NotImplementedError()


class _ModeStruct(Struct): 
    """
    Represents a mode-specific struct for the BNO055 controller.

    Args:
        register_address (int): The register address of the struct.
        struct_format (str): The format string specifying the struct's layout.
        mode (int): The mode associated with the struct.

    Attributes:
        mode (int): The mode associated with the struct.

    Methods:
        __get__(self, obj, objtype): Get the value of the struct.
        __set__(self, obj, value): Set the value of the struct.
    """

    def __init__(self, register_address: int, struct_format: str, mode: int) -> None:
        super().__init__(register_address, struct_format)
        self.mode = mode

    def __get__(
        self, obj: Optional["BNO055_I2C"], objtype: Optional[Type["BNO055_I2C"]] = None
    ) -> Union[int, Tuple[int, int, int]]:
        """
        Get the value of the struct.

        Args:
            obj (Optional[BNO055_I2C]): The BNO055_I2C object.
            objtype (Optional[Type[BNO055_I2C]]): The type of the BNO055_I2C object.

        Returns:
            Union[int, Tuple[int, int, int]]: The value of the struct.
        """
        last_mode = obj.mode
        obj.mode = self.mode
        result = super().__get__(obj, objtype)
        obj.mode = last_mode
        # single value comes back as a one-element tuple
        return result[0] if isinstance(result, tuple) and len(result) == 1 else result

    def __set__(
        self, obj: Optional["BNO055_I2C"], value: Union[int, Tuple[int, int, int]]
    ) -> None:
        """
        Set the value of the struct.

        Args:
            obj (Optional[BNO055_I2C]): The BNO055_I2C object.
            value (Union[int, Tuple[int, int, int]]): The value to set.

        Returns:
            None
        """
        last_mode = obj.mode
        obj.mode = self.mode
        # underlying __set__() expects a tuple
        set_val = value if isinstance(value, tuple) else (value,)
        super().__set__(obj, set_val)
        obj.mode = last_mode


class BNO055:
    """
    This class represents the BNO055 sensor.

    The BNO055 is a 9-DOF (degree of freedom) sensor that combines an accelerometer, a gyroscope,
    and a magnetometer. It provides absolute orientation data by fusing the measurements from these
    three sensors.

    The class provides methods to initialize the sensor, set the operating mode, read sensor data,
    and check the calibration status.

    Usage:
        bno = BNO055()  # Initialize the sensor
        bno.set_normal_mode()  # Set the sensor to normal mode
        bno.mode = BNO055.ACCONLY_MODE  # Set the sensor mode to accelerometer only
        accel_data = bno.acceleration  # Read the accelerometer data

    Note:
        The BNO055 sensor must be properly calibrated for accurate orientation data. Use the
        `calibrated` property to check the calibration status before using the sensor data.

    Attributes:
        accel_range (int): The range of the accelerometer. Default is 4G.
        gyro_range (int): The range of the gyroscope. Default is 2000 degrees per second.
        magnet_rate (int): The data rate of the magnetometer. Default is 20Hz.

    Methods:
        __init__(): Initializes the BNO055 sensor.
        
        set_normal_mode(): Sets the sensor to normal mode.
        
        _reset(): Resets the sensor to default settings.
        
        mode: Gets or sets the operating mode of the sensor.
        
        calibration_status: Gets the calibration status of the sensor.
        
        calibrated: Checks if the sensor is fully calibrated.
        
        external_crystal: Gets or sets the use of an external crystal.
        
        temperature: Gets the temperature of the sensor.
        
        acceleration: Gets the raw accelerometer readings.
        
        magnetic: Gets the raw magnetometer readings.
        
        gyro: Gets the raw gyroscope readings.
        
        euler: Gets the Euler angles representing the orientation.

    Constants:
        CONFIG_MODE: The configuration mode of the sensor.
        ACCONLY_MODE: The accelerometer only mode.
        MAGONLY_MODE: The magnetometer only mode.
        GYRONLY_MODE: The gyroscope only mode.
        ACCMAG_MODE: The accelerometer and magnetometer mode.
        ACCGYRO_MODE: The accelerometer and gyroscope mode.
        MAGGYRO_MODE: The magnetometer and gyroscope mode.
        AMG_MODE: The accelerometer, magnetometer, and gyroscope mode.
        IMUPLUS_MODE: The IMU mode with high output data rate.
        COMPASS_MODE: The compass mode for measuring magnetic field.
        M4G_MODE: The mode using magnetometer for rotation detection.
        NDOF_FMC_OFF_MODE: The fusion mode with fast magnetometer calibration off.
        NDOF_MODE: The fusion mode with 9 degrees of freedom.
    """

    def __init__(self) -> None:
        """
        Initializes the BNO055 sensor.

        Raises:
            RuntimeError: If the chip ID read from the sensor does not match the expected chip ID.
        """
        # Initialize the sensor
        chip_id = self._read_register(_ID_REGISTER)
        if chip_id != _CHIP_ID:
            raise RuntimeError(f"bad chip id ({chip_id:#x} != {_CHIP_ID:#x})")
        self._reset()
        self.set_normal_mode()
        self._write_register(_PAGE_REGISTER, 0x00)
        self._write_register(_TRIGGER_REGISTER, 0x00)
        self.accel_range = ACCEL_4G
        self.gyro_range = GYRO_2000_DPS
        self.magnet_rate = MAGNET_20HZ
        time.sleep(0.01)
        self.mode = NDOF_MODE
        time.sleep(0.01)
        
    def _reset(self) -> None:
        """Resets the sensor to default settings."""
        self.mode = CONFIG_MODE
        try:
            self._write_register(_TRIGGER_REGISTER, 0x20)
        except OSError:  # error due to the chip resetting
            pass
        # wait for the chip to reset (650 ms typ.)
        time.sleep(0.7)

    @property
    def mode(self) -> int:
        """
        legend: x=on, -=off

        +------------------+-------+---------+------+----------+----------+
        | Mode             | Accel | Compass | Gyro | Fusion   | Fusion   |
        |                  |       | (Mag)   |      | Absolute | Relative |
        +==================+=======+=========+======+==========+==========+
        | CONFIG_MODE      |   -   |   -     |  -   |     -    |     -    |
        +------------------+-------+---------+------+----------+----------+
        | ACCONLY_MODE     |   X   |   -     |  -   |     -    |     -    |
        +------------------+-------+---------+------+----------+----------+
        | MAGONLY_MODE     |   -   |   X     |  -   |     -    |     -    |
        +------------------+-------+---------+------+----------+----------+
        | GYRONLY_MODE     |   -   |   -     |  X   |     -    |     -    |
        +------------------+-------+---------+------+----------+----------+
        | ACCMAG_MODE      |   X   |   X     |  -   |     -    |     -    |
        +------------------+-------+---------+------+----------+----------+
        | ACCGYRO_MODE     |   X   |   -     |  X   |     -    |     -    |
        +------------------+-------+---------+------+----------+----------+
        | MAGGYRO_MODE     |   -   |   X     |  X   |     -    |     -    |
        +------------------+-------+---------+------+----------+----------+
        | AMG_MODE         |   X   |   X     |  X   |     -    |     -    |
        +------------------+-------+---------+------+----------+----------+
        | IMUPLUS_MODE     |   X   |   -     |  X   |     -    |     X    |
        +------------------+-------+---------+------+----------+----------+
        | COMPASS_MODE     |   X   |   X     |  -   |     X    |     -    |
        +------------------+-------+---------+------+----------+----------+
        | M4G_MODE         |   X   |   X     |  -   |     -    |     X    |
        +------------------+-------+---------+------+----------+----------+
        | NDOF_FMC_OFF_MODE|   X   |   X     |  X   |     X    |     -    |
        +------------------+-------+---------+------+----------+----------+
        | NDOF_MODE        |   X   |   X     |  X   |     X    |     -    |
        +------------------+-------+---------+------+----------+----------+

        The default mode is :const:`NDOF_MODE`.

        | You can set the mode using the line below:
        | ``sensor.mode = adafruit_bno055.ACCONLY_MODE``
        | replacing :const:`ACCONLY_MODE` with the mode you want to use

        .. data:: CONFIG_MODE

           This mode is used to configure BNO, wherein all output data is reset to zero and sensor
           fusion is halted.

        .. data:: ACCONLY_MODE

           In this mode, the BNO055 behaves like a stand-alone acceleration sensor. In this mode the
           other sensors (magnetometer, gyro) are suspended to lower the power consumption.

        .. data:: MAGONLY_MODE

           In MAGONLY mode, the BNO055 behaves like a stand-alone magnetometer, with acceleration
           sensor and gyroscope being suspended.

        .. data:: GYRONLY_MODE

           In GYROONLY mode, the BNO055 behaves like a stand-alone gyroscope, with acceleration
           sensor and magnetometer being suspended.

        .. data:: ACCMAG_MODE

           Both accelerometer and magnetometer are switched on, the user can read the data from
           these two sensors.

        .. data:: ACCGYRO_MODE

           Both accelerometer and gyroscope are switched on; the user can read the data from these
           two sensors.

        .. data:: MAGGYRO_MODE

           Both magnetometer and gyroscope are switched on, the user can read the data from these
           two sensors.

        .. data:: AMG_MODE

           All three sensors accelerometer, magnetometer and gyroscope are switched on.

        .. data:: IMUPLUS_MODE

           In the IMU mode the relative orientation of the BNO055 in space is calculated from the
           accelerometer and gyroscope data. The calculation is fast (i.e. high output data rate).

        .. data:: COMPASS_MODE

           The COMPASS mode is intended to measure the magnetic earth field and calculate the
           geographic direction.

        .. data:: M4G_MODE

           The M4G mode is similar to the IMU mode, but instead of using the gyroscope signal to
           detect rotation, the changing orientation of the magnetometer in the magnetic field is
           used.

        .. data:: NDOF_FMC_OFF_MODE

           This fusion mode is same as NDOF mode, but with the Fast Magnetometer Calibration turned
           OFF.

        .. data:: NDOF_MODE

           This is a fusion mode with 9 degrees of freedom where the fused absolute orientation data
           is calculated from accelerometer, gyroscope and the magnetometer.

        """
        return self._read_register(_MODE_REGISTER) & 0b00001111  # mask off the power and mode bits


    @mode.setter
    def mode(self, new_mode: int) -> None:
        """
        Sets the operating mode of the Bno055Controller.

        Args:
            new_mode (int): The new operating mode to set.

        Returns:
            None
        """
        self._write_register(_MODE_REGISTER, CONFIG_MODE)  # Empirically necessary
        time.sleep(0.02)  # give time to switch modes
        if new_mode != CONFIG_MODE:
            self._write_register(_MODE_REGISTER, new_mode)
            time.sleep(0.01)  # give time to switch modes

    @property
    def calibration_status(self) -> Tuple[int, int, int, int]:
        """Tuple containing sys, gyro, accel, and mag calibration data."""
        calibration_data = self._read_register(_CALIBRATION_REGISTER)
        sys = (calibration_data >> 6) & 0x03
        gyro = (calibration_data >> 4) & 0x03
        accel = (calibration_data >> 2) & 0x03
        mag = calibration_data & 0x03
        return sys, gyro, accel, mag

    @property
    def calibrated(self) -> bool:
        """Boolean indicating calibration status."""
        sys, gyro, accel, mag = self.calibration_status
        return sys == gyro == accel == mag == 0x03

    @property
    def external_crystal(self) -> bool:
        """Switches the use of external crystal on or off."""
        last_mode = self.mode
        self.mode = CONFIG_MODE
        self._write_register(_PAGE_REGISTER, 0x00)
        value = self._read_register(_TRIGGER_REGISTER)
        self.mode = last_mode
        return value == 0x80

    @external_crystal.setter
    def use_external_crystal(self, value: bool) -> None:
        last_mode = self.mode
        self.mode = CONFIG_MODE
        self._write_register(_PAGE_REGISTER, 0x00)
        self._write_register(_TRIGGER_REGISTER, 0x80 if value else 0x00)
        self.mode = last_mode
        time.sleep(0.01)

    @property
    def temperature(self) -> int:
        """Measures the temperature of the chip in degrees Celsius."""
        return self._temperature

    @property
    def _temperature(self) -> None:
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    @property
    def acceleration(self) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Gives the raw accelerometer readings, in m/s.
        Returns an empty tuple of length 3 when this property has been disabled by the current mode.
        """
        if self.mode not in [0x00, 0x02, 0x03, 0x06]:
            return self._acceleration
        return (None, None, None)

    @property
    def _acceleration(self) -> None:
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    @property
    def magnetic(self) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Gives the raw magnetometer readings in microteslas.
        Returns an empty tuple of length 3 when this property has been disabled by the current mode.
        """
        if self.mode not in [0x00, 0x01, 0x03, 0x05, 0x08]:
            return self._magnetic
        return (None, None, None)

    @property
    def _magnetic(self) -> None:
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    @property
    def gyro(self) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Gives the raw gyroscope reading in radians per second.
        Returns an empty tuple of length 3 when this property has been disabled by the current mode.
        """
        if self.mode not in [0x00, 0x01, 0x02, 0x04, 0x09, 0x0A]:
            return self._gyro
        return (None, None, None)

    @property
    def _gyro(self) -> None:
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    @property
    def euler(self) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Gives the calculated orientation angles, in degrees.
        Returns an empty tuple of length 3 when this property has been disabled by the current mode.
        """
        if self.mode in [0x08, 0x09, 0x0A, 0x0B, 0x0C]:
            return self._euler
        return (None, None, None)

    @property
    def _euler(self) -> None:
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    @property
    def quaternion(
        self,
    ) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
        """Gives the calculated orientation as a quaternion.
        Returns an empty tuple of length 4 when this property has been disabled by the current mode.
        """
        if self.mode in [0x08, 0x09, 0x0A, 0x0B, 0x0C]:
            return self._quaternion
        return (None, None, None, None)

    @property
    def _quaternion(self) -> None:
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    @property
    def linear_acceleration(
        self,
    ) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Returns the linear acceleration, without gravity, in m/s.
        Returns an empty tuple of length 3 when this property has been disabled by the current mode.
        """
        if self.mode in [0x08, 0x09, 0x0A, 0x0B, 0x0C]:
            return self._linear_acceleration
        return (None, None, None)

    @property
    def _linear_acceleration(self) -> None:
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    @property
    def gravity(self) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Returns the gravity vector, without acceleration in m/s.
        Returns an empty tuple of length 3 when this property has been disabled by the current mode.
        """
        if self.mode in [0x08, 0x09, 0x0A, 0x0B, 0x0C]:
            return self._gravity
        return (None, None, None)

    @property
    def _gravity(self) -> None:
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    @property
    def accel_range(self) -> int:
        """Switch the accelerometer range and return the new range. Default value: +/- 4g
        See table 3-8 in the datasheet.
        """
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_ACCEL_CONFIG_REGISTER)
        self._write_register(_PAGE_REGISTER, 0x00)
        return 0b00000011 & value

    @accel_range.setter
    def accel_range(self, rng: int = ACCEL_4G) -> None:
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_ACCEL_CONFIG_REGISTER)
        masked_value = 0b11111100 & value
        self._write_register(_ACCEL_CONFIG_REGISTER, masked_value | rng)
        self._write_register(_PAGE_REGISTER, 0x00)

    @property
    def accel_bandwidth(self) -> int:
        """Switch the accelerometer bandwidth and return the new bandwidth. Default value: 62.5 Hz
        See table 3-8 in the datasheet.
        """
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_ACCEL_CONFIG_REGISTER)
        self._write_register(_PAGE_REGISTER, 0x00)
        return 0b00011100 & value

    @accel_bandwidth.setter
    def accel_bandwidth(self, bandwidth: int = ACCEL_62_5HZ) -> None:
        if self.mode in [0x08, 0x09, 0x0A, 0x0B, 0x0C]:
            raise RuntimeError(ERROR_MSG)
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_ACCEL_CONFIG_REGISTER)
        masked_value = 0b11100011 & value
        self._write_register(_ACCEL_CONFIG_REGISTER, masked_value | bandwidth)
        self._write_register(_PAGE_REGISTER, 0x00)

    @property
    def accel_mode(self) -> int:
        """Switch the accelerometer mode and return the new mode. Default value: Normal
        See table 3-8 in the datasheet.
        """
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_ACCEL_CONFIG_REGISTER)
        self._write_register(_PAGE_REGISTER, 0x00)
        return 0b11100000 & value

    @accel_mode.setter
    def accel_mode(self, mode: int = ACCEL_NORMAL_MODE) -> None:
        if self.mode in [0x08, 0x09, 0x0A, 0x0B, 0x0C]:
            raise RuntimeError(ERROR_MSG)
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_ACCEL_CONFIG_REGISTER)
        masked_value = 0b00011111 & value
        self._write_register(_ACCEL_CONFIG_REGISTER, masked_value | mode)
        self._write_register(_PAGE_REGISTER, 0x00)

    @property
    def gyro_range(self) -> int:
        """Switch the gyroscope range and return the new range. Default value: 2000 dps
        See table 3-9 in the datasheet.
        """
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_GYRO_CONFIG_0_REGISTER)
        self._write_register(_PAGE_REGISTER, 0x00)
        return 0b00000111 & value

    @gyro_range.setter
    def gyro_range(self, rng: int = GYRO_2000_DPS) -> None:
        if self.mode in [0x08, 0x09, 0x0A, 0x0B, 0x0C]:
            raise RuntimeError(ERROR_MSG)
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_GYRO_CONFIG_0_REGISTER)
        masked_value = 0b00111000 & value
        self._write_register(_GYRO_CONFIG_0_REGISTER, masked_value | rng)
        self._write_register(_PAGE_REGISTER, 0x00)

    @property
    def gyro_bandwidth(self) -> int:
        """Switch the gyroscope bandwidth and return the new bandwidth. Default value: 32 Hz
        See table 3-9 in the datasheet.
        """
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_GYRO_CONFIG_0_REGISTER)
        self._write_register(_PAGE_REGISTER, 0x00)
        return 0b00111000 & value

    @gyro_bandwidth.setter
    def gyro_bandwidth(self, bandwidth: int = GYRO_32HZ) -> None:
        if self.mode in [0x08, 0x09, 0x0A, 0x0B, 0x0C]:
            raise RuntimeError(ERROR_MSG)
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_GYRO_CONFIG_0_REGISTER)
        masked_value = 0b00000111 & value
        self._write_register(_GYRO_CONFIG_0_REGISTER, masked_value | bandwidth)
        self._write_register(_PAGE_REGISTER, 0x00)

    @property
    def gyro_mode(self) -> int:
        """Switch the gyroscope mode and return the new mode. Default value: Normal
        See table 3-9 in the datasheet.
        """
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_GYRO_CONFIG_1_REGISTER)
        self._write_register(_PAGE_REGISTER, 0x00)
        return 0b00000111 & value

    @gyro_mode.setter
    def gyro_mode(self, mode: int = GYRO_NORMAL_MODE) -> None:
        if self.mode in [0x08, 0x09, 0x0A, 0x0B, 0x0C]:
            raise RuntimeError(ERROR_MSG)
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_GYRO_CONFIG_1_REGISTER)
        masked_value = 0b00000000 & value
        self._write_register(_GYRO_CONFIG_1_REGISTER, masked_value | mode)
        self._write_register(_PAGE_REGISTER, 0x00)

    @property
    def magnet_rate(self) -> int:
        """Switch the magnetometer data output rate and return the new rate. Default value: 20Hz
        See table 3-10 in the datasheet.
        """
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_MAGNET_CONFIG_REGISTER)
        self._write_register(_PAGE_REGISTER, 0x00)
        return 0b00000111 & value

    @magnet_rate.setter
    def magnet_rate(self, rate: int = MAGNET_20HZ) -> None:
        if self.mode in [0x08, 0x09, 0x0A, 0x0B, 0x0C]:
            raise RuntimeError(ERROR_MSG)
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_MAGNET_CONFIG_REGISTER)
        masked_value = 0b01111000 & value
        self._write_register(_MAGNET_CONFIG_REGISTER, masked_value | rate)
        self._write_register(_PAGE_REGISTER, 0x00)

    @property
    def magnet_operation_mode(self) -> int:
        """Switch the magnetometer operation mode and return the new mode. Default value: Regular
        See table 3-10 in the datasheet.
        """
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_MAGNET_CONFIG_REGISTER)
        self._write_register(_PAGE_REGISTER, 0x00)
        return 0b00011000 & value

    @magnet_operation_mode.setter
    def magnet_operation_mode(self, mode: int = MAGNET_REGULAR_MODE) -> None:
        if self.mode in [0x08, 0x09, 0x0A, 0x0B, 0x0C]:
            raise RuntimeError(ERROR_MSG)
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_MAGNET_CONFIG_REGISTER)
        masked_value = 0b01100111 & value
        self._write_register(_MAGNET_CONFIG_REGISTER, masked_value | mode)
        self._write_register(_PAGE_REGISTER, 0x00)

    @property
    def magnet_mode(self) -> int:
        """Switch the magnetometer power mode and return the new mode. Default value: Forced
        See table 3-10 in the datasheet.
        """
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_MAGNET_CONFIG_REGISTER)
        self._write_register(_PAGE_REGISTER, 0x00)
        return 0b01100000 & value

    @magnet_mode.setter
    def magnet_mode(self, mode: int = MAGNET_FORCEMODE_MODE) -> None:
        if self.mode in [0x08, 0x09, 0x0A, 0x0B, 0x0C]:
            raise RuntimeError(ERROR_MSG)
        self._write_register(_PAGE_REGISTER, 0x01)
        value = self._read_register(_MAGNET_CONFIG_REGISTER)
        masked_value = 0b00011111 & value
        self._write_register(_MAGNET_CONFIG_REGISTER, masked_value | mode)
        self._write_register(_PAGE_REGISTER, 0x00)

    def _write_register(self, register: int, value: int) -> None:
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    def _read_register(self, register: int) -> None:
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    @property
    def axis_remap(self):
        """Return a tuple with the axis remap register values.

        This will return 6 values with the following meaning:
          - X axis remap (a value of AXIS_REMAP_X, AXIS_REMAP_Y, or AXIS_REMAP_Z.
                          which indicates that the physical X axis of the chip
                          is remapped to a different axis)
          - Y axis remap (see above)
          - Z axis remap (see above)
          - X axis sign (a value of AXIS_REMAP_POSITIVE or AXIS_REMAP_NEGATIVE
                         which indicates if the X axis values should be positive/
                         normal or negative/inverted.  The default is positive.)
          - Y axis sign (see above)
          - Z axis sign (see above)

        Note that the default value, per the datasheet, is NOT P0,
        but rather P1 ()
        """
        # Get the axis remap register value.
        map_config = self._read_register(_AXIS_MAP_CONFIG_REGISTER)
        z = (map_config >> 4) & 0x03
        y = (map_config >> 2) & 0x03
        x = map_config & 0x03
        # Get the axis remap sign register value.
        sign_config = self._read_register(_AXIS_MAP_SIGN_REGISTER)
        x_sign = (sign_config >> 2) & 0x01
        y_sign = (sign_config >> 1) & 0x01
        z_sign = sign_config & 0x01
        # Return the results as a tuple of all 3 values.
        return (x, y, z, x_sign, y_sign, z_sign)

    @axis_remap.setter
    def axis_remap(self, remap):
        """Pass a tuple consisting of x, y, z, x_sign, y-sign, and z_sign.

        Set axis remap for each axis.  The x, y, z parameter values should
        be set to one of AXIS_REMAP_X (0x00), AXIS_REMAP_Y (0x01), or
        AXIS_REMAP_Z (0x02) and will change the BNO's axis to represent another
        axis.  Note that two axises cannot be mapped to the same axis, so the
        x, y, z params should be a unique combination of AXIS_REMAP_X,
        AXIS_REMAP_Y, AXIS_REMAP_Z values.
        The x_sign, y_sign, z_sign values represent if the axis should be
        positive or negative (inverted). See section 3.4 of the datasheet for
        information on the proper settings for each possible orientation of
        the chip.
        """
        x, y, z, x_sign, y_sign, z_sign = remap
        # Switch to configuration mode. Necessary to remap axes
        current_mode = self._read_register(_MODE_REGISTER)
        self.mode = CONFIG_MODE
        # Set the axis remap register value.
        map_config = 0x00
        map_config |= (z & 0x03) << 4
        map_config |= (y & 0x03) << 2
        map_config |= x & 0x03
        self._write_register(_AXIS_MAP_CONFIG_REGISTER, map_config)
        # Set the axis remap sign register value.
        sign_config = 0x00
        sign_config |= (x_sign & 0x01) << 2
        sign_config |= (y_sign & 0x01) << 1
        sign_config |= z_sign & 0x01
        self._write_register(_AXIS_MAP_SIGN_REGISTER, sign_config)
        # Go back to normal operation mode.
        self._write_register(_MODE_REGISTER, current_mode)

    def set_normal_mode(self) -> None:
        """Sets the sensor to Normal power mode"""
        self._write_register(_POWER_REGISTER, _POWER_NORMAL)

    def set_suspend_mode(self) -> None:
        """Sets the sensor to Suspend power mode"""
        self._write_register(_POWER_REGISTER, _POWER_SUSPEND)


class BNO055I2C(BNO055):
    """
    Driver for the BNO055 9DOF IMU sensor via I2C.
    """

    _temperature = _ReadOnlyUnaryStruct(0x34, "b")
    _acceleration = _ScaledReadOnlyStruct(0x08, "<hhh", 1 / 100)
    _magnetic = _ScaledReadOnlyStruct(0x0E, "<hhh", 1 / 16)
    _gyro = _ScaledReadOnlyStruct(0x14, "<hhh", 0.001090830782496456)
    _euler = _ScaledReadOnlyStruct(0x1A, "<hhh", 1 / 16)
    _quaternion = _ScaledReadOnlyStruct(0x20, "<hhhh", 1 / (1 << 14))
    _linear_acceleration = _ScaledReadOnlyStruct(0x28, "<hhh", 1 / 100)
    _gravity = _ScaledReadOnlyStruct(0x2E, "<hhh", 1 / 100)

    offsets_accelerometer = _ModeStruct(_OFFSET_ACCEL_REGISTER, "<hhh", CONFIG_MODE)
    """Calibration offsets for the accelerometer"""
    offsets_magnetometer = _ModeStruct(_OFFSET_MAGNET_REGISTER, "<hhh", CONFIG_MODE)
    """Calibration offsets for the magnetometer"""
    offsets_gyroscope = _ModeStruct(_OFFSET_GYRO_REGISTER, "<hhh", CONFIG_MODE)
    """Calibration offsets for the gyroscope"""

    radius_accelerometer = _ModeStruct(_RADIUS_ACCEL_REGISTER, "<h", CONFIG_MODE)
    """Radius for accelerometer (cm?)"""
    radius_magnetometer = _ModeStruct(_RADIUS_MAGNET_REGISTER, "<h", CONFIG_MODE)
    """Radius for magnetometer (cm?)"""

    def __init__(self, i2c: I2C, address: int = 0x28) -> None:
        """
        Initializes a Bno055Controller object.

        Args:
            i2c (I2C): The I2C bus object to communicate with the BNO055 sensor.
            address (int, optional): The I2C address of the BNO055 sensor. Defaults to 0x28.
        """
        self.buffer = bytearray(2)
        self.i2c_device = I2CDevice(i2c, address)
        super().__init__()

    def _write_register(self, register: int, value: int) -> None:
        """
        Writes a value to the specified register.

        Args:
            register (int): The register address to write to.
            value (int): The value to write to the register.

        Returns:
            None
        """
        self.buffer[0] = register
        self.buffer[1] = value
        with self.i2c_device as i2c:
            i2c.write(self.buffer)

    def _read_register(self, register: int) -> int:
        """
        Reads the value from the specified register.

        Args:
            register (int): The register address to read from.

        Returns:
            int: The value read from the register.
        """
        self.buffer[0] = register
        with self.i2c_device as i2c:
            i2c.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)
        return self.buffer[1]


class BNO055UART(BNO055):
    """
    Driver for the BNO055 9DOF IMU sensor via UART.
    """

    def __init__(self, uart: UART) -> None:
        self._uart = uart
        self._uart.baudrate = 115200 # set the default baudrate to 115200 
        super().__init__()

    def _write_register(  
        self, register: int, data: int
    ) -> None:
        if not isinstance(data, bytes):
            data = bytes([data])
        self._uart.write(bytes([0xAA, 0x00, register, len(data)]) + data) # write the data that is sent to the UART 
        now = time.monotonic() 
        while self._uart.in_waiting < 2 and time.monotonic() - now < 0.25:
            pass
        resp = self._uart.read(self._uart.in_waiting)
        if len(resp) < 2:
            raise OSError("UART access error.")
        if resp[0] != 0xEE or resp[1] != 0x01:
            raise RuntimeError(f"UART write error: {resp[1]}")

    def _read_register(  # pylint: disable=arguments-differ
        self, register: int, length: int = 1
    ) -> int:
        i = 0
        while i < 3:
            self._uart.write(bytes([0xAA, 0x01, register, length]))
            now = time.monotonic()
            while self._uart.in_waiting < length + 2 and time.monotonic() - now < 0.1:
                pass
            resp = self._uart.read(self._uart.in_waiting)
            if len(resp) >= 2 and resp[0] == 0xBB:
                break
            i += 1
        if len(resp) < 2:
            raise OSError("UART access error.")
        if resp[0] != 0xBB:
            raise RuntimeError(f"UART read error: {resp[1]}")
        if length > 1:
            return resp[2:]
        return int(resp[2])

    @property
    def _temperature(self) -> int:
        return self._read_register(0x34)

    @property
    def _acceleration(self) -> Tuple[float, float, float]:
        resp = struct.unpack("<hhh", self._read_register(0x08, 6))
        return tuple(x / 100 for x in resp)

    @property
    def _magnetic(self) -> Tuple[float, float, float]:
        resp = struct.unpack("<hhh", self._read_register(0x0E, 6))
        return tuple(x / 16 for x in resp)

    @property
    def _gyro(self) -> Tuple[float, float, float]:
        resp = struct.unpack("<hhh", self._read_register(0x14, 6))
        return tuple(x * 0.001090830782496456 for x in resp)

    @property
    def _euler(self) -> Tuple[float, float, float]:
        resp = struct.unpack("<hhh", self._read_register(0x1A, 6))
        return tuple(x / 16 for x in resp)

    @property
    def _quaternion(self) -> Tuple[float, float, float]:
        resp = struct.unpack("<hhhh", self._read_register(0x20, 8))
        return tuple(x / (1 << 14) for x in resp)

    @property
    def _linear_acceleration(self) -> Tuple[float, float, float]:
        resp = struct.unpack("<hhh", self._read_register(0x28, 6))
        return tuple(x / 100 for x in resp)

    @property
    def _gravity(self) -> Tuple[float, float, float]:
        resp = struct.unpack("<hhh", self._read_register(0x2E, 6))
        return tuple(x / 100 for x in resp)

    @property
    def offsets_accelerometer(self) -> Tuple[int, int, int]:
        """Calibration offsets for the accelerometer"""
        return struct.unpack("<hhh", self._read_register(_OFFSET_ACCEL_REGISTER, 6))

    @offsets_accelerometer.setter
    def offsets_accelerometer(self, offsets: Tuple[int, int, int]) -> None:
        data = bytearray(6)
        struct.pack_into("<hhh", data, 0, *offsets)
        self._write_register(_OFFSET_ACCEL_REGISTER, bytes(data))

    @property
    def offsets_magnetometer(self) -> Tuple[int, int, int]:
        """Calibration offsets for the magnetometer"""
        return struct.unpack("<hhh", self._read_register(_OFFSET_MAGNET_REGISTER, 6))

    @offsets_magnetometer.setter
    def offsets_magnetometer(self, offsets: Tuple[int, int, int]) -> None:
        data = bytearray(6)
        struct.pack_into("<hhh", data, 0, *offsets)
        self._write_register(_OFFSET_MAGNET_REGISTER, bytes(data))

    @property
    def offsets_gyroscope(self) -> Tuple[int, int, int]:
        """Calibration offsets for the gyroscope"""
        return struct.unpack("<hhh", self._read_register(_OFFSET_GYRO_REGISTER, 6))

    @offsets_gyroscope.setter
    def offsets_gyroscope(self, offsets: Tuple[int, int, int]) -> None:
        data = bytearray(6)
        struct.pack_into("<hhh", data, 0, *offsets)
        self._write_register(_OFFSET_GYRO_REGISTER, bytes(data))

    @property
    def radius_accelerometer(self) -> int:
        """Radius for accelerometer (cm?)"""
        return struct.unpack("<h", self._read_register(_RADIUS_ACCEL_REGISTER, 2))[0]

    @radius_accelerometer.setter
    def radius_accelerometer(self, radius: int) -> None:
        data = bytearray(2)
        struct.pack_into("<h", data, 0, radius)
        self._write_register(_RADIUS_ACCEL_REGISTER, bytes(data))

    @property
    def radius_magnetometer(self) -> int:
        """Radius for magnetometer (cm?)"""
        return struct.unpack("<h", self._read_register(_RADIUS_MAGNET_REGISTER, 2))[0]

    @radius_magnetometer.setter
    def radius_magnetometer(self, radius: int) -> None:
        data = bytearray(2)
        struct.pack_into("<h", data, 0, radius)
        self._write_register(_RADIUS_MAGNET_REGISTER, bytes(data))