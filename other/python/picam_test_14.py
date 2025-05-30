
from picamera2 import Picamera2
import cv2
import numpy as np
import os
import time #importante
import serial
import RPi.GPIO as GPIO #importante

#Config pin
PIN_PWN = 18 #Pin PWN GPIO18
PIN_IN1 = 23 #Pin control GPIO23
PIN_IN2 = 24 #Pin control GPIO24
PIN_STANDBY = 25 #Pin standby GPIO25

#Config RaspPi
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_PWN, GPIO.OUT) #Salidas
GPIO.setup(PIN_IN1, GPIO.OUT)
GPIO.setup(PIN_IN2, GPIO.OUT)
GPIO.setup(PIN_STANDBY, GPIO.OUT)

#Config PWN
pwn_motor = GPIO.PWM(PIN_PWN, 100) #100 Hz
pwn_motor.start(0) #off

try:
	while True:
		#Summon H
		GPIO.output(PIN_STANDBY, GPIO.HIGH)
		
		#Giro 1
		GPIO.output(PIN_IN1, GPIO.HIGH)
		GPIO.output(PIN_IN2, GPIO.LOW)
		pwn_motor.ChangeDutyCycle(50) #%
		print("w")
		time.sleep(4)
		
		#Giro 1
		GPIO.output(PIN_IN1, GPIO.LOW)
		GPIO.output(PIN_IN2, GPIO.HIGH)
		pwn_motor.ChangeDutyCycle(80) #%
		print("s")
		time.sleep(4)
		
except KeyboardInterrupt:
	pwn_motor.stop()
	GPIO.cleanup()
