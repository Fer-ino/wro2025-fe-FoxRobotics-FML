import time
from mpu_gyro import initialize, calibrate_gyro_offset, update_angular_position
from control_1 import control_motor

def main():
    # 1) Inicializar y despertar sensor
    try:
        initialize()
        print("MPU6050 listo.")
    except RuntimeError as e:
        print(e)
        return

    # 2) Calibrar offset de giroscopio Z
    print("Calibrando giroscopio Z (reposo)...")
    offset_z = calibrate_gyro_offset()
    print(f"Offset Z obtenido: {offset_z:.2f} LSB")

    # 3) Bucle principal de lectura e integración
    angle_z = 0.0
    t_prev  = time.time()
    print("\nLeyendo datos (Ctrl+C para salir)\n")

    try:
        while True:
            t_now = time.time()
            dt    = t_now - t_prev
            t_prev = t_now

            angle_z, wz = update_angular_position(dt, offset_z, angle_z)

            print(f"ω_z = {wz:6.2f} °/s    θ_z = {angle_z:7.2f} °")
            control_motor(1, 50, 90)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nLectura detenida por el usuario.")

if __name__ == "__main__":
    main()
