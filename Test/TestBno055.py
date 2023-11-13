import random
import time

class SimulatedBNO055:
    def __init__(self):
        # Initialize with some default values or random values
        self.temperature = 25  # in degrees Celsius
        self.acceleration = (0, 0, 0)  # in m/s^2
        self.magnetic = (0, 0, 0)  # in microteslas
        self.gyro = (0, 0, 0)  # in rad/sec
        self.euler = (0, 0, 0)
        self.quaternion = (0, 0, 0, 1)
        self.linear_acceleration = (0, 0, 0)  # in m/s^2
        self.gravity = (0, 0, 0)  # in m/s^2

    def update_readings(self):
        # Simulate sensor data updates
        self.temperature = 25 + random.uniform(-5, 5)
        self.acceleration = tuple(random.uniform(-1, 1) for _ in range(3))
        self.magnetic = tuple(random.uniform(-50, 50) for _ in range(3))
        self.gyro = tuple(random.uniform(-5, 5) for _ in range(3))
        self.euler = tuple(random.uniform(0, 360) for _ in range(3))
        self.quaternion = tuple(random.uniform(-1, 1) for _ in range(4))
        self.linear_acceleration = tuple(random.uniform(-1, 1) for _ in range(3))
        self.gravity = tuple(random.uniform(-9.8, 9.8) for _ in range(3))

    def read_sensor(self):
        # Simulate a sensor read
        self.update_readings()
        return {
            "temperature": self.temperature,
            "acceleration": self.acceleration,
            "magnetic": self.magnetic,
            "gyro": self.gyro,
            "euler": self.euler,
            "quaternion": self.quaternion,
            "linear_acceleration": self.linear_acceleration,
            "gravity": self.gravity
        }

# Example usage
sensor = SimulatedBNO055()
while True:
    data = sensor.read_sensor()
    print(data)
    time.sleep(1)  # Simulate delay
