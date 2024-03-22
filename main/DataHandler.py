import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


#Mean: The average value of the bno055 sensor readings in the window. It gives a central tendency of the data.
def mean(data):
    return np.mean(data)

#Standard Deviation: Measures the amount of variation or dispersion in the sensor readings.
def std(data):
    return np.std(data) 

#Minimum/Maximum Values: The lowest and highest readings in the window, which can be crucial for capturing the range of motion.
def min_max(data):
    return np.min(data), np.max(data) 

#Sum: The total sum of the sensor readings, useful for understanding the cumulative effect over the window.
def sum(data):
    return np.sum(data)

#Skewness: measure of asymmetry. It can be used to identify outliers that are far from the mean.
def skewness(data):
    return pd.Series(data).skew()

#kurtosis: measure of whether the data are heavy-tailed or light-tailed relative to a normal distribution.
def kurtosis(data):
    return pd.Series(data).kurtosis()
def median(data):
    return np.median(data)


data = {
    'bno055_reading1': [0.1, 0.2, 0.3],
    'bno055_reading2': [0.4, 0.5, 0.6],
    'bno055_reading3': [0.4, 0.5, 0.6],
    'pressure_flexor1': [0.7, 0.8, 0.9],
    'pressure_flexor2': [0.7, 0.8, 0.9],
    'pressure_flexor3': [0.7, 0.8, 0.9],
    'pressure_flexor4': [0.7, 0.8, 0.9],
    'pressure_flexor5': [0.7, 0.8, 0.9]
}

df = pd.DataFrame(data)

# Normalize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)