/*!
 *   @file read_all_data.ino
 *
 *    2024, Raúl Juan García
 *    Proyect: "Signify, Sign language identification, translation and transmission system"
 *    University of Salamanca, Bachelor's Degree in Computer Engineering
 * 
 *    This driver uses the Adafruit unified sensor library (Adafruit_Sensor),
 *    which provides a common 'type' for sensor data and some helper functions.
 * 
 *    Connections
 *    ===========
 *    Connect SCL to analog 5
 *    Connect SDA to analog 4
 *    Connect VDD to 3.3-5V DC
 *    Connect GROUND to common ground
 *
 */

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

/** Set the delay between fresh samples **/
# define BNO055_SAMPLERATE_DELAY_MS (300)

/** The sensor mode will be Nine Degrees of Freedom mode, enabling all sensors and the fusion algorithm **/
# define BNO055_OPERATION_MODE ()

int P0 = A0;   // select the input pin for the thummb's potentiometer
int P1 = A1;   // select the input pin for the index's potentiometer
int P2 = A2;   // select the input pin for the middle finger's potentiometer
int P3 = A3;   // select the input pin for the ring finger's potentiometer
int P4 = A7;   // select the input pin for the little finger's potentiometer

int V0 = 0;  // variable to store the value coming from the thumb sensor 
int V1 = 0;  // variable to store the value coming from the index sensor 
int V2 = 0;  // variable to store the value coming from the middle sensor 
int V3 = 0;  // variable to store the value coming from the ring finger sensor 
int V4 = 0;  // variable to store the value coming from the little finger sensor 

// I2C device address and line (default I2C address is 0x28 and 0x29)
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire);
int8_t temp;

void setup(void){
  
  Serial.begin(115200);

  while (!Serial) delay(10);  // wait for serial port to open

  /* Initialise the sensor */
  int timeout = 850; // can take up to 850 ms to boot up
  while (timeout > 0) {
    if (bno.begin()) {
      temp = bno.getTemp();
      bno.setExtCrystalUse(true);
      break;
    }
    
    delay(10);
    timeout -= 10;
  }
  if (timeout <= 0){
    Serial.print("No BNO055 detected ... Check your wiring or I2C ADDR!");
  }
}

/*!
 *  @brief   Gets a vector reading from the specified source
 *  @param   vector_type
 *           possible vector type values
 *           [VECTOR_ACCELEROMETER
 *            VECTOR_MAGNETOMETER
 *            VECTOR_GYROSCOPE
 *            VECTOR_EULER
 *            VECTOR_LINEARACCEL
 *            VECTOR_GRAVITY]
 *  @return  vector from specified source
 */
void loop(void){

  sensors_event_t orientationData, angVelocityData , linearAccelData;
  bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  bno.getEvent(&angVelocityData, Adafruit_BNO055::VECTOR_GYROSCOPE);
  bno.getEvent(&linearAccelData, Adafruit_BNO055::VECTOR_LINEARACCEL);

  eulerEvent(&orientationData);
  gyroEvent(&angVelocityData);
  accelEvent(&linearAccelData);
  flexorEvent();
  calibrationEvent();

  Serial.println();
  delay(BNO055_SAMPLERATE_DELAY_MS);
}

/*!
* @brief  Display the flexor data
*
* @return void
*/
void flexorEvent() {
  V0 = analogRead(P0); // Lee el valor de la entrada analógica en el pin A0
  Serial.print(V0); // Imprime el valor analógico en el monitor serial
  Serial.print(",");

  V1 = analogRead(P1); // Lee el valor de la entrada analógica en el pin A1
  Serial.print(V1); // Imprime el valor analógico en el monitor serial
  Serial.print(",");

  V2 = analogRead(P2); // Lee el valor de la entrada analógica en el pin A2
  Serial.print(V2); // Imprime el valor analógico en el monitor serial
  Serial.print(",");

  V3 = analogRead(P3); // Lee el valor de la entrada analógica en el pin A3
  Serial.print(V3); // Imprime el valor analógico en el monitor serial
  Serial.print(",");
  
  V4 = analogRead(P4); // Lee el valor de la entrada analógica en el pin A7
  Serial.print(V4); // Imprime el valor analógico en el monitor serial

  Serial.print("*");


}

/*!
* @brief  Display the Euler data
*
* @return void
*/
void eulerEvent(sensors_event_t* orientationEvent) {
  Serial.print(orientationEvent->orientation.x);
  Serial.print(",");
  Serial.print(orientationEvent->orientation.y);
  Serial.print(",");
  Serial.print(orientationEvent->orientation.z);
  Serial.print("*");
}

/*!
* @brief  Display the angular velocity data
*
* @return void
*/
void gyroEvent(sensors_event_t* gyroEvent) {
  if (gyroEvent->type == SENSOR_TYPE_GYROSCOPE) {
    Serial.print(gyroEvent->gyro.x);
    Serial.print(",");
    Serial.print(gyroEvent->gyro.y);
    Serial.print(",");
    Serial.print(gyroEvent->gyro.z);
    Serial.print("*");
  }
  
}

/*!
* @brief  Display the linear acceleration data
*
* @return void
*/
void accelEvent(sensors_event_t* accelEvent) {
  if (accelEvent->type == SENSOR_TYPE_LINEAR_ACCELERATION) {
    Serial.print(accelEvent->acceleration.x);
    Serial.print(",");
    Serial.print(accelEvent->acceleration.y);
    Serial.print(",");
    Serial.print(accelEvent->acceleration.z);
    Serial.print("*");
  }
}


/*!
* @brief  Display the sensor calibration status
*
* @return void
*/
void calibrationEvent() {

  uint8_t system, gyro, accel, mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  Serial.print(accel);
  Serial.print(",");
  Serial.print(gyro);
  Serial.print(",");
  Serial.print(mag);
  Serial.print(",");
  Serial.print(system);

}


