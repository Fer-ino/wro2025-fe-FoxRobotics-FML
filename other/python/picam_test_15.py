
from picamera2 import Picamera2
import cv2
import numpy as np
import os
import time
import serial
import RPi.GPIO as GPIO
from control_motor import control_motor #La func

try:
	while True:
		control_motor(1, 50)
		
except KeyboardInterrupt:  #poner esto obligatorio
	pwn_motor.stop()
	GPIO.cleanup()
