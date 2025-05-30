#hay rojo, falta verde
#omitir este, la linea vertical esta en medio

from picamera2 import Picamera2
import cv2
import numpy as np
import os
import time

#init
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640,480)})
picam2.configure(config)
picam2.start()
print("cam ON")

#Definir rojos HSV
lower_red1 = np.array([0, 120, 70]) #Oscuro
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70]) #Brillante
upper_red2 = np.array([180, 255, 255])

try:
	
	while True:
		#Frame
		frame = picam2.capture_array()
		
		#Frame a HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
		
		#Mask for red
		mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
		mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
		red_mask = cv2.bitwise_or(mask1, mask2)
		
		#Min rojo
		red_pixels = cv2.countNonZero(red_mask)
		if red_pixels  >= 500: 
		
			#Contornos de imagen CON MASK
			contours,_ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
			#The one (rectangulo)
			largest_contour = None
			largest_area = 0
		
			#Busca the one
			for contour in contours:
				area = cv2.contourArea(contour)
				if area > largest_area:
					largest_area = area
					largest_contour = contour
		
			#Procesar the one
			if largest_contour is not None:
				#Calclar centroide the one
				M = cv2.moments(largest_contour)
				if M["m00"] != 0:
					cX = int(M["m10"] / M["m00"]) #Centroide X
					#La linea
					cv2.line(frame, (cX, 0), (cX, frame.shape[0]), (0, 255, 0), 2)
		else:
			#Mas rojo
			print("DAme mas roo")
		
		#Ver 
		cv2.imshow("Video", frame)
		
		#Ext q
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
			
except KeyboardInterrupt:
	print("STOP")
	
	

#Del res
picam2.stop()
cv2.destroyAllWindows()


#instala open cv

#sudo apt upgrade
#sudo apt update
#libcamera-hello

# #ver si hacer carpetas o paquetes
# #hacer micrcontrolador

#Detect red and green
#square red and green
#centroid red geen
#put lines on camera
#line of suare must be at side of line of camera
