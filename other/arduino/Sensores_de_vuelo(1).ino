#include <Wire.h>
#include <VL53L0X.h>

int XSHUT1 = 32;  // Pin XSHUT del primer sensor
int XSHUT2 = 26; // Pin XSHUT del segundo sensor
int XSHUT3 = 25;  // Pin XSHUT del tercer sensor
int XSHUT4 = 33;  // Pin XSHUT del cuarto sensor

VL53L0X sensor1;
VL53L0X sensor2;
VL53L0X sensor3;
VL53L0X sensor4;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  pinMode(XSHUT1, OUTPUT);
  pinMode(XSHUT2, OUTPUT);
  pinMode(XSHUT3, OUTPUT);
  pinMode(XSHUT4, OUTPUT);
    
  // Apagar ambos sensores
  digitalWrite(XSHUT1, LOW);
  digitalWrite(XSHUT2, LOW);
  digitalWrite(XSHUT3, LOW);
  digitalWrite(XSHUT4, LOW);
  delay(10);
    
  // Encender primer sensor y asignar dirección
  digitalWrite(XSHUT1, HIGH);
  delay(10);
  sensor1.init();
  sensor1.setAddress(0x30);
    
  // Encender segundo sensor y asignar dirección
  digitalWrite(XSHUT2, HIGH);
  delay(10);
  sensor2.init();
  sensor2.setAddress(0x30);

  digitalWrite(XSHUT3, HIGH);
  delay(10);
  sensor3.init();
  sensor3.setAddress(0x32);

  digitalWrite(XSHUT4, HIGH);
  delay(10);
  sensor4.init();
  sensor4.setAddress(0x33);
    
  // Configurar sensores
  sensor1.startContinuous();
  sensor2.startContinuous();
  sensor3.startContinuous();
  sensor4.startContinuous();
}

void loop() {
  Serial.print("Distancia Sensor 1: ");
  Serial.print(sensor1.readRangeContinuousMillimeters());
  Serial.print(" mm\t");
  
  Serial.print("Distancia Sensor 2: ");
  Serial.print(sensor2.readRangeContinuousMillimeters());
  Serial.print(" mm\t"); 
  
  Serial.print("Distancia Sensor 3: ");
  Serial.print(sensor3.readRangeContinuousMillimeters());
  Serial.print(" mm\t");
  
  Serial.print("Distancia Sensor 4: ");
  Serial.print(sensor4.readRangeContinuousMillimeters());
  Serial.println(" mm");
  
  delay(100);
}