#include <Wire.h>
#include <VL53L0X.h>

int XSHUT1 = 32;  
int XSHUT2 = 33; 
int XSHUT3 = 25;  
int XSHUT4 = 26;  

VL53L0X sensor1;
VL53L0X sensor2;
VL53L0X sensor3;
VL53L0X sensor4;


void setup() {
    Serial.begin(115200); // Inicialización para comunicación con Raspberry
    Wire.begin();
    
    pinMode(XSHUT1, OUTPUT);
    pinMode(XSHUT2, OUTPUT);
    pinMode(XSHUT3, OUTPUT);
    pinMode(XSHUT4, OUTPUT);
    
    // Apagar sensores
    digitalWrite(XSHUT1, LOW);
    digitalWrite(XSHUT2, LOW);
    digitalWrite(XSHUT3, LOW);
    digitalWrite(XSHUT4, LOW);
    delay(10);
    
    // Inicializar sensores con diferentes direcciones
    digitalWrite(XSHUT1, HIGH);
    delay(10);
    sensor1.init();
    sensor1.setAddress(0x30);

    digitalWrite(XSHUT2, HIGH);
    delay(10);
    sensor2.init();
    sensor2.setAddress(0x31);

    digitalWrite(XSHUT3, HIGH);
    delay(10);
    sensor3.init();
    sensor3.setAddress(0x32);

    digitalWrite(XSHUT4, HIGH);
    delay(10);
    sensor4.init();
    sensor4.setAddress(0x33);
    
    sensor1.startContinuous();
    sensor2.startContinuous();
    sensor3.startContinuous();
    sensor4.startContinuous();
}

void loop() {
    

    // Leer datos de los sensores
    int distancia1 = sensor1.readRangeContinuousMillimeters();
    int distancia2 = sensor2.readRangeContinuousMillimeters();
    int distancia3 = sensor3.readRangeContinuousMillimeters();
    int distancia4 = sensor4.readRangeContinuousMillimeters();

    // Enviar datos a Raspberry Pi en formato CSV
    Serial.print(distancia1); Serial.print(",");
    Serial.print(distancia2); Serial.print(",");
    Serial.print(distancia3); Serial.print(",");
    Serial.print(distancia4); Serial.println("");
    
    delay(100);
}
