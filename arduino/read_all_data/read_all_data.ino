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
# define BNO055_SAMPLERATE_DELAY_MS (100)

/** The sensor mode will be Nine Degrees of Freedom mode, enabling all sensors and the fusion algorithm **/
# define BNO055_OPERATION_MODE (Adafruit_BNO055::OPERATION_MODE_NDOF)

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

void setup(void){
  Serial.begin(115200);

  while (!Serial) delay(10);  // wait for serial port to open

  Serial.println("Orientation Sensor Test"); Serial.println("");

  /* Initialise the sensor */
  int timeout = 850; // can take up to 850 ms to boot up
  while (timeout > 0) {
    if (bno.begin()) {
      bno.setMode(BNO055_OPERATION_MODE);
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

  sensors_event_t orientationData , angVelocityData , linearAccelData, magnetometerData, accelerometerData, gravityData;
  bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  bno.getEvent(&angVelocityData, Adafruit_BNO055::VECTOR_GYROSCOPE);
  bno.getEvent(&linearAccelData, Adafruit_BNO055::VECTOR_LINEARACCEL);
  bno.getEvent(&magnetometerData, Adafruit_BNO055::VECTOR_MAGNETOMETER);
  bno.getEvent(&accelerometerData, Adafruit_BNO055::VECTOR_ACCELEROMETER);
  bno.getEvent(&gravityData, Adafruit_BNO055::VECTOR_GRAVITY);

  printEvent(&orientationData);
  printEvent(&angVelocityData);
  printEvent(&linearAccelData);
  printEvent(&magnetometerData);
  printEvent(&accelerometerData);

  flexorEvent();

  calibrarionEvent();


  delay(BNO055_SAMPLERATE_DELAY_MS);
}

/*!
* @brief  Display the flexor data
*
* @return void
*/
void flexorEvent() {
 V0 = analogRead(P0); // Lee el valor de la entrada analógica en el pin A0
  Serial.println(V0); // Imprime el valor analógico en el monitor serial

  V1 = analogRead(P1); // Lee el valor de la entrada analógica en el pin A1
  Serial.println(V1); // Imprime el valor analógico en el monitor serial
  
  V2 = analogRead(P2); // Lee el valor de la entrada analógica en el pin A2
  Serial.println(V2); // Imprime el valor analógico en el monitor serial
  
  V3 = analogRead(P3); // Lee el valor de la entrada analógica en el pin A3
  Serial.println(V3); // Imprime el valor analógico en el monitor serial
  
  V4 = analogRead(P4); // Lee el valor de la entrada analógica en el pin A7
  Serial.println(V4); // Imprime el valor analógico en el monitor serial

}


/*!
* @brief  Display the sensor calibration status
*
* @return void
*/
void calibrarionEvent() {

  uint8_t system, gyro, accel, mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  Serial.println("_");
  Serial.print(system);
  Serial.print(",");
  Serial.print(gyro);
  Serial.print(",");
  Serial.print(accel);
  Serial.print(",");
  Serial.println(mag);
  Serial.println("_");

}

/*!
* @brief  Display the sensor data regarding the given event
* @param  event
*         The event to be displayed
*
* @return void
*/
void printEvent(sensors_event_t* event) {
  double x = -1000000, y = -1000000 , z = -1000000; //dumb values, easy to spot problem
  if (event->type == SENSOR_TYPE_ACCELEROMETER) {
    Serial.print("Accl:");
    x = event->acceleration.x;
    y = event->acceleration.y;
    z = event->acceleration.z;
  }
  else if (event->type == SENSOR_TYPE_ORIENTATION) {
    Serial.print("Orient:");
    x = event->orientation.x;
    y = event->orientation.y;
    z = event->orientation.z;
  }
  else if (event->type == SENSOR_TYPE_MAGNETIC_FIELD) {
    Serial.print("Mag:");
    x = event->magnetic.x;
    y = event->magnetic.y;
    z = event->magnetic.z;
  }
  else if (event->type == SENSOR_TYPE_GYROSCOPE) {
    Serial.print("Gyro:");
    x = event->gyro.x;
    y = event->gyro.y;
    z = event->gyro.z;
  }
  else if (event->type == SENSOR_TYPE_ROTATION_VECTOR) {
    Serial.print("Rot:");
    x = event->gyro.x;
    y = event->gyro.y;
    z = event->gyro.z;
  }
  else if (event->type == SENSOR_TYPE_LINEAR_ACCELERATION) {
    Serial.print("Linear:");
    x = event->acceleration.x;
    y = event->acceleration.y;
    z = event->acceleration.z;
  }
  else if (event->type == SENSOR_TYPE_GRAVITY) {
    Serial.print("Gravity:");
    x = event->acceleration.x;
    y = event->acceleration.y;
    z = event->acceleration.z;
  }
  else {
    Serial.print("Unk:");
  }

  Serial.println("*");
  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");
  Serial.println(z);
  Serial.println("*");
}


