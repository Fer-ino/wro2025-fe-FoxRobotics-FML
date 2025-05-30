import smbus
import time

#Aparte del delay, esta cosa funciona
#conectar ado a gnd para 68

# Dirección I2C del MPU6050
MPU6050_ADDR = 0x68

# Registros importantes
PWR_MGMT_1   = 0x6B
GYRO_XOUT_H  = 0x43

# Inicializar bus I2C
bus = smbus.SMBus(1)  # Usualmente bus 1 en Raspberry Pi

# Despertar el MPU6050 (está dormido por defecto)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_raw_data(addr):
    # Leer dos bytes y combinarlos
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr+1)
    value = (high << 8) | low
    # Convertir a número negativo si es necesario
    if value > 32767:
        value -= 65536
    return value

print("Leyendo datos del giroscopio (velocidad angular en °/s)...\nPresiona Ctrl+C para salir.\n")

try:
    while True:
        # Leer valores en bruto del giroscopio
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_XOUT_H + 2)
        gyro_z = read_raw_data(GYRO_XOUT_H + 4)

        # Convertir a grados/segundo (según escala por defecto ±250 °/s => sensibilidad 131 LSB/°/s)
        Gx = gyro_x / 131.0
        Gy = gyro_y / 131.0
        Gz = gyro_z / 131.0

        print(f"X: {Gx:.2f} °/s, Y: {Gy:.2f} °/s, Z: {Gz:.2f} °/s")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nLectura detenida.")
