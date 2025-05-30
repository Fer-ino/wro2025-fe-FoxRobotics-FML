#include <Wire.h>
#include <MPU6050.h>

// Crear un objeto MPU6050
MPU6050 mpu;

// Variables para almacenar datos
int16_t axg,ayg,azg; // Aceleración medida por el Acelerómetro (medida en g)
float ax, ay, az; // Aceleración angular en m/s^2 (El valor medido por el Acelrómetro divido entre la sensibilidad multiplicada por la constante de gravedad 9.81 m/s^2)
float vx = 0, vy = 0, vz = 0; // Velocidad en m/s (Integral de la aceleración)
float vxa = 0, vya = 0, vza = 0, vxb = 0, vyb = 0, vzb = 0, dvx = 0, dvy = 0, dvz = 0; 

int16_t wxg,wyg,wzg; // Velocidad angular medida por el Acelerómetro con una sensibilidad de 131
float wx,wy,wz; // Velocidad angular en grados (El valor medido por el Acelerómetro dividido entre la sensibilidad de 131)
float pwx = 0, pwy = 0, pwz = 0; // Posición angular en grados (Integral de la velocidad angular)
float pwxa = 0, pwya = 0, pwza = 0, pwxb = 0, pwyb = 0, pwzb = 0, dpwx = 0, dpwy = 0, dpwz = 0; 
float offsetwx = 0, offsetwy = 0, offsetwz = 0;


float Tiempoinicial = 0; //Chat gpt me lo dio como "unsigned long" pero debe de jalar con un float segun yo
float Tiempoactual;
float dt;

void setup() {
  Serial.begin(115200);
  
  Wire.begin();
  mpu.initialize();
  
  if (!mpu.testConnection()) {
    Serial.println("No se logró conectar correctamente con MPU6050");
    while (1);
  }

  Serial.println("MPU6050 conectado");
}

void loop() {
  // Calcular el tiempo transcurrido
  Tiempoactual = millis();
  dt = (Tiempoinicial - Tiempoactual) / 1000.0;  // Tiempo en segundos
  Tiempoinicial = Tiempoactual;

  // Leer los valores de aceleración (en g)
  mpu.getAcceleration(&axg, &ayg, &azg);
  
  // Convertir la aceleración a metros por segundo al cuadrado (m/s^2)
  ax = axg / 16384.0 * 9.81;  // 16384 es el valor de sensibilidad en ±2g
  if (abs(ax) < 0.35){
    ax = 0;
  }

  ay = ayg / 16384.0 * 9.81;
  if (abs(ay) < 0.3){
      ay = 0;
  }
  
  az = azg / 16384.0 * 9.81;
  //if (abs(az) < 0.3){
  //    az = 0;
  //}

  // Calcular la velocidad (integración de la aceleración)
  vxa = vxa + (ax * dt);
  dvx = vxa - vxb;
  if (abs(dvx) < 0.2){
   vx = vx + (ax * dt);
  }
  else {
    vx = vx;
  }
  vxb = vxa;

  vya = vya + (ay * dt);
  dvy = vya - vyb;
  if (abs(dvy) < 0.2){
   vy = vy + (ay * dt);
  }
  else {
    vy = vy;
  }
  vyb = vya;
  
  vza = vza + (az * dt);
  dvz = vza - vzb;
  if (abs(dvz) < 0.2){
   vz = vz + (az * dt);
  }
  else {
    vz = vz;
  }
  vzb = vza;
  
  // Leer los valores de velocidad angular (en °)
  mpu.getRotation(&wxg, &wyg, &wzg);
  // Convertir a velocidad angular en °/s (para rango ±250°/s)
  offsetwx = 270;
  wx = (wxg - offsetwx) / 131.0;
  wx = wx;
  if (abs(wx) < 4.5){
      wx = 0;
  }

  offsetwy = 144;
  wy = (wyg - offsetwy)/ 131.0;
  if (abs(wy) < 2.5){
      wy = 0;
  }

  offsetwz = 56.5;
  wz = (wzg - offsetwz) / 131.0;
  if (abs(wz) < 0.3){
      wz = 0;
  }

  pwxa = pwxa + (wx * dt);
  dpwx = pwxa - pwxb;
  if (abs(dpwx) < 0.4){
   pwx = pwx + (wx * dt);
  }
  else {
      pwx = pwx;
  }
  pwxb = pwxa;
  
  pwya = pwya + (wy * dt);
  dpwy = pwya - pwyb;
  if (abs(dpwy) < 0.4){
   pwy = pwy + (wy * dt);
  }
  else {
      pwy = pwy;
  }
  pwyb = pwya;

  pwza = pwza + (wy * dt);
  dpwz = pwza - pwzb;
  if (abs(dpwz) < 0.4){
   pwz = pwz + (wz * dt);
  }
  else {
      pwz = pwz;
  }
  pwzb = pwza;

  // Imprimir los resultados
  Serial.print("Aceleración X: "); Serial.print(ax); Serial.print(" m/s^2\t");
  Serial.print("Aceleración Y: "); Serial.print(ay); Serial.print(" m/s^2\t");
  Serial.print("Aceleración Z: "); Serial.print(az); Serial.print(" m/s^2\t");

  Serial.print("Velocidad X: "); Serial.print(vx); Serial.print(" m/s\t");
  Serial.print("Velocidad Y: "); Serial.print(vy); Serial.print(" m/s\t");
  Serial.print("Velocidad Z: "); Serial.print(vz); Serial.print(" m/s\t");

  Serial.print("Velocidad Angular X: "); Serial.print(wx); Serial.print(" °/s\t");
  Serial.print("Velocidad Angular Y: "); Serial.print(wy); Serial.print(" °/s\t");
  Serial.print("Velocidad Angular Z: "); Serial.print(wz); Serial.print(" °/s\t");

  Serial.print("Posición Angular X: "); Serial.print(pwx); Serial.print(" °\t");
  Serial.print("Posición Angular Y: "); Serial.print(pwy); Serial.print(" °\t");
  Serial.print("Posición Angular Z: "); Serial.print(pwz); Serial.println(" °");

  delay(100);
}


/*
#include <Wire.h>
#include <MPU6050.h>

// Crear un objeto MPU6050
MPU6050 mpu;

// Variables para almacenar datos
int16_t wzg; // Velocidad angular del eje Z medida por el sensor
float wz;    // Velocidad angular del eje Z en °/s
float pwz = 0; // Posición angular acumulada del eje Z en grados

unsigned long tiempoActual, tiempoPrevio; // Variables para calcular dt
float dt;  // Tiempo transcurrido en segundos

void setup() {
  Serial.begin(9600);
  
  Wire.begin();
  mpu.initialize();
  
  if (!mpu.testConnection()) {
    Serial.println("No se logró conectar correctamente con MPU6050");
    while (1); // Detener si no hay conexión
  }

  Serial.println("MPU6050 conectado");
  tiempoPrevio = millis(); // Inicialización del tiempo previo
}

void loop() {
  // Calcular el tiempo transcurrido
  tiempoActual = millis();
  dt = (tiempoActual - tiempoPrevio) / 1000.0;  // Tiempo en segundos
  tiempoPrevio = tiempoActual;

  // Leer la velocidad angular (raw data para todos los ejes)
  int16_t wxg, wyg; // Variables temporales para los otros ejes
  mpu.getRotation(&wxg, &wyg, &wzg);


  // Convertir a velocidad angular en °/s (sensibilidad para rango ±250°/s)
  wz = (wzg + 230 ) / 131.0;

  // Filtrar señales bajas
  if (abs(wz) < 0.6) {
    wz = 0; // Reducir ruido
  }

  // Calcular posición angular acumulada en el eje Z
  pwz += wz * dt;

  // Imprimir resultados
  Serial.print("Velocidad Angular Z: "); Serial.print(wzg); Serial.print(" °/s\t");
  Serial.print("Posición Angular Z: "); Serial.print(pwz); Serial.println(" °");
  
  delay(100); // Retardo para evitar datos excesivos
}
*/