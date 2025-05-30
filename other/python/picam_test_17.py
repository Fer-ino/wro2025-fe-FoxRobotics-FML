
from picamera2 import Picamera2
import cv2
import numpy as np
import os
import time
import serial
import RPi.GPIO as GPIO
from control import control_motor, control_servo

try:
	while True:
		control_motor(1, 50)
		control_servo(90)
		
except KeyboardInterrupt:  #poner esto obligatorio
	pwm_motor.ChangeDutyCycle(1)
	pwm_motor.stop()
	pwm_servo.stop()
	GPIO.cleanup()
