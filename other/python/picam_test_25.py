import serial
import time

def encontrar_puerto_serial():
    import glob
    puertos = glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*')
    if not puertos:
        raise IOError("No se encontró ningún puerto serial USB")
    return puertos[0]

def main():
    # Parámetros de conexión
    puerto = encontrar_puerto_serial()       # e.g. '/dev/ttyUSB0'
    baudios = 115200                        # Coincide con Serial.begin(115200)
    timeout_s = 1.0                         # Segundos de espera para readline()

    print(f"Iniciando lectura desde {puerto} a {baudios} baudios...")
    try:
        ser = serial.Serial(puerto, baudios, timeout=timeout_s)
        time.sleep(2)  # Pausa de conexión
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial: {e}")
        return

    try:
        while True:
            linea = ser.readline().decode('utf-8', errors='replace').strip()
            if not linea:
                # Timeout sin datos
                continue

            if linea.endswith(','):
                linea = linea[:-1]
            partes = linea.split(',')

            # Convertir a enteros
            try:
                distancias = [int(p) for p in partes]
            except ValueError:
                print(f"Línea mal formada, no se pudo convertir a int")
                continue

            d1, d2, d3, d4 = distancias

            print(f"Sensor1: {d1} mm | Sensor2: {d2} mm | "
                  f"Sensor3: {d3} mm | Sensor4: {d4} mm")

    except KeyboardInterrupt:
        print("\nLectura interrumpida.")
    finally:
        ser.close()
        print("Puerto serial cerrado.")

if __name__ == "__main__":
    main()
