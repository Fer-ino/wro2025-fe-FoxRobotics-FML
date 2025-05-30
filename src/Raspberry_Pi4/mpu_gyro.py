import smbus
import time

# Dirección I2C del MPU6050
MPU6050_ADDR      = 0x68
PWR_MGMT_1        = 0x6B
GYRO_XOUT_H       = 0x43

# Constantes de configuración
GYRO_SENSITIVITY  = 131.0     # LSB/(°/s) para ±250 °/s
NOISE_THRESHOLD   = 0.6       # °/s, umbral de ruido
READ_DELAY_SEC    = 0.001     # Pausa en calibración
LOOP_DELAY_SEC    = 0.1       # Pausa en loop principal

# Bus I2C global
bus = smbus.SMBus(1)

def initialize():
    """
    Despierta el MPU6050 y comprueba conexión.
    Lanza excepción si falla.
    """
    # Despertar
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)
    time.sleep(0.1)
    # Test de conexión
    try:
        bus.read_byte_data(MPU6050_ADDR, PWR_MGMT_1)
    except Exception as e:
        raise RuntimeError("No se pudo conectar al MPU6050") from e

def read_raw_gyro_z():
    """
    Lee y devuelve el valor crudo de giro en Z (signed 16-bit).
    """
    high = bus.read_byte_data(MPU6050_ADDR, GYRO_XOUT_H + 4)
    low  = bus.read_byte_data(MPU6050_ADDR, GYRO_XOUT_H + 5)
    val  = (high << 8) | low
    if val > 32767:
        val -= 65536
    return val

def calibrate_gyro_offset(sample_count=2000):
    """
    Toma `sample_count` lecturas de giro Z en reposo,
    y devuelve el offset promedio (LSB).
    """
    acc = 0
    for _ in range(sample_count):
        acc += read_raw_gyro_z()
        time.sleep(READ_DELAY_SEC)
    return acc / sample_count

def update_angular_position(dt, offset, angle_prev):
    """
    Lee la velocidad angular en Z, le resta el offset, convierte a °/s,
    filtra el ruido y devuelve (angle_new, wz).
   
    - dt: float, tiempo transcurrido en segundos.
    - offset: LSB promedio obtenido en calibración.
    - angle_prev: ángulo acumulado anterior (grados).
    """
    raw_z = read_raw_gyro_z()
    wz    = (raw_z - offset) / GYRO_SENSITIVITY
    if abs(wz) < NOISE_THRESHOLD:
        wz = 0.0
    angle_new = angle_prev + wz * dt
    return angle_new, wz
