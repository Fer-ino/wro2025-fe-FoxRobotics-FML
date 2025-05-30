import smbus
import time

# Dirección I2C del MPU6050
MPU6050_ADDR      = 0x68
PWR_MGMT_1        = 0x6B
GYRO_XOUT_H       = 0x43

# Constantes de configuración
GYRO_SENSITIVITY  = 131.0     
NOISE_THRESHOLD   = 0.6       
READ_DELAY_SEC    = 0.001     
LOOP_DELAY_SEC    = 0.1       

# Bus I2C global
bus = smbus.SMBus(1)

def initialize():
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)
    time.sleep(0.1)
    try:
        bus.read_byte_data(MPU6050_ADDR, PWR_MGMT_1)
    except Exception as e:
        raise RuntimeError("No se pudo conectar al MPU6050") from e

def read_raw_gyro_z():
    high = bus.read_byte_data(MPU6050_ADDR, GYRO_XOUT_H + 4)
    low  = bus.read_byte_data(MPU6050_ADDR, GYRO_XOUT_H + 5)
    val  = (high << 8) | low
    if val > 32767:
        val -= 65536
    return val

def calibrate_gyro_offset(sample_count=2000):
    acc = 0
    for _ in range(sample_count):
        acc += read_raw_gyro_z()
        time.sleep(READ_DELAY_SEC)
    return acc / sample_count

def update_angular_position(dt, offset, angle_prev):
    raw_z = read_raw_gyro_z()
    wz    = (raw_z - offset) / GYRO_SENSITIVITY
    if abs(wz) < NOISE_THRESHOLD:
        wz = 0.0
    angle_new = angle_prev + wz * dt
    return angle_new, wz
