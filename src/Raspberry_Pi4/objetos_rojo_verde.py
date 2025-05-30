from picamera2 import Picamera2
import cv2
import numpy as np

#La func
def detectar_objeto_mas_grande(picam2):

	#Definir rojos HSV
	lower_red1 = np.array([0, 120, 70]) #Oscuro
	upper_red1 = np.array([10, 255, 255])
	lower_red2 = np.array([170, 120, 70]) #Brillante
	upper_red2 = np.array([180, 255, 255])
	
	#Definir verdes HSV
	lower_green = np.array([40, 90, 65])
	upper_green = np.array([80, 250, 235])
	
	#Frame
	frame = picam2.capture_array()
		
	#Frame a HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
		
	#Mask for red
	mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
	mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
	red_mask = cv2.bitwise_or(mask1, mask2)
	
	#Mask for green
	green_mask = cv2.inRange(hsv, lower_green, upper_green)
	
	#LOs dos
	combined_mask = cv2.bitwise_or(red_mask, green_mask)
	
	#Min rojo y verde
	pixel_count = cv2.countNonZero(combined_mask)
	if pixel_count  >= 200: 
		
		#Contornos de imagen CON MASK
		contours,_ = cv2.findContours(combined_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		#The one (rectangulo)
		largest_contour = None
		largest_area = 0
		detected_color = None
		
		#Busca the one
		for contour in contours:
			area = cv2.contourArea(contour)
			if area > largest_area:
				#Cual?
				mask = np.zeros(hsv.shape[:2], dtype="uint8")
				cv2.drawContours(mask, [contour], -1, 255, -1)
				mean_color = cv2.mean(hsv, mask=mask)
				if 0 <= mean_color[0] <= 10 or 170 <= mean_color[0] <= 180:
					detected_color = "RED"
				elif 40 <= mean_color[0] <= 80:
					detected_color = "GREEN"
				else:
					continue
				
				largest_area = area
				largest_contour = contour
		
		#Procesar the one
		if largest_contour is not None:
			#Calcular centroide the one
			M = cv2.moments(largest_contour)
			if M["m00"] != 0:
				cX = int(M["m10"] / M["m00"]) #Centroide X
		#EL rectangulo
				x, y, w, h = cv2.boundingRect(largest_contour)
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	
				return frame, cX, detected_color #Le cX y frame dar
	return frame, None, None