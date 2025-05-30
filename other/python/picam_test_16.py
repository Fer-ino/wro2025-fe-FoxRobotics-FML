
from picamera2 import Picamera2
import cv2
import numpy as np
import time
import serial
import RPi.GPIO as GPIO
from control_motor import control_motor #La func

#El servopin
SERVO_PIN = 12 #GPIO12

#Config RaspPi
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT) #Salidas

#Config PWM
pwm = GPIO.PWM(SERVO_PIN, 50) #Hz
pwm.start(0)

#Func ang
def move_servo(ang):
	ciclo_trabajo = 2 + (ang / 18)
	pwm.ChangeDutyCycle(ciclo_trabajo)
	time.sleep(0.5)
	pwm.ChangeDutyCycle(0)

try:
	while True:
		move_servo(0)
		print("0")
		time.sleep(2)
		move_servo(30)
		print("30")
		time.sleep(2)
		move_servo(60)
		print("60")
		time.sleep(2)
		move_servo(90)
		print("90")
		time.sleep(2)
		move_servo(120)
		print("120")
		time.sleep(2)
		move_servo(150)
		print("150")
		time.sleep(2)
		move_servo(180)
		print("180")
		time.sleep(2)
		move_servo(150)
		print("150")
		time.sleep(2)
		move_servo(120)
		print("120")
		time.sleep(2)
		move_servo(90)
		print("90")
		time.sleep(2)
		move_servo(60)
		print("60")
		time.sleep(2)
		move_servo(30)
		print("30")
		time.sleep(2)
		
except KeyboardInterrupt:  #poner esto obligatorio
	pwn.stop()
	GPIO.cleanup()
