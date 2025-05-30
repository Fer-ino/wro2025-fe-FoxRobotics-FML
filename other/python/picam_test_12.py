#checa iluminacion

from picamera2 import Picamera2
import cv2
import numpy as np
import os
import time
from detectar_objeto_mas_grande import detectar_objeto_mas_grande

#init
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640,480)})
picam2.configure(config)
picam2.start()
print("cam ON")

try:
	
	while True:
		
		#La func
		frame, cX, detected_color = detectar_objeto_mas_grande(picam2)
		
		if cX is not None:
			#Haz linea por favor
			cv2.line(frame, (cX, 0), (cX, frame.shape[0]), (0, 255, 0), 2)
			print(detected_color)
		else:
			print("no :(")
		
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
