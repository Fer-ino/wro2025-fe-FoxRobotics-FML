
import time
import RPi.GPIO as GPIO

# Config pin
PIN_PWM = 18  # Pin PWM GPIO18
PIN_IN1 = 23  # Pin control GPIO23
PIN_IN2 = 24  # Pin control GPIO24
PIN_STANDBY = 25  # Pin standby GPIO25
SERVO_PIN = 12  # Pin servo GPIO12

# Config RaspPi
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_PWM, GPIO.OUT)
GPIO.setup(PIN_IN1, GPIO.OUT)
GPIO.setup(PIN_IN2, GPIO.OUT)
GPIO.setup(PIN_STANDBY, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Config PWM
pwm_motor = GPIO.PWM(PIN_PWM, 100)  # 100 Hz
pwm_motor.start(0)
pwm_servo = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz
pwm_servo.start(0)

# Esto es motor
def control_motor(rot, vel, ang):
    # Activar puente H
    GPIO.output(PIN_STANDBY, GPIO.HIGH)

    # Giro
    if rot == 1:  # Sentido 1
        GPIO.output(PIN_IN1, GPIO.HIGH)
        GPIO.output(PIN_IN2, GPIO.LOW)
    elif rot == 2:  # Sentido 2
        GPIO.output(PIN_IN1, GPIO.LOW)
        GPIO.output(PIN_IN2, GPIO.HIGH)
    else:  # Sin Sentido
        GPIO.output(PIN_IN1, GPIO.LOW)
        GPIO.output(PIN_IN2, GPIO.LOW)

    # Velocidad
    pwm_motor.ChangeDutyCycle(vel)

    # Esto es servo
    ciclo_trabajo = 2 + (ang / 18)  # Conversión de ángulo a ciclo de trabajo
    pwm_servo.ChangeDutyCycle(ciclo_trabajo)
    time.sleep(0.02) #Checa quitar el delay y reemplazarlo
    pwm_servo.ChangeDutyCycle(0)
