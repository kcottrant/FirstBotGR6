
import numpy as np
import pypot.dynamixel
import cv2
import itertools
import time
import math
#import test

d=0.069 # distance entre centre du robot et les roues
r=0.0555 # rayon d'une roue


# cherche un port et se connecte au premier qu'il trouve
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io = pypot.dynamixel.DxlIO(ports[0])
print("Connected")

dxl_io.set_wheel_mode([1])
dxl_io.set_wheel_mode([2])

# fait avancer le robot a une vitesse v  en rpm
def avancer(v) :
	dxl_io.set_moving_speed({1: v})
	dxl_io.set_moving_speed({2: -v})

# fait reculer le robot a une vitesse v en rpm
def reculer(v) :
	dxl_io.set_moving_speed({1: -v})
	dxl_io.set_moving_speed({2: v})

# fait tourner sur lui meme le robot vers la droite a une vitesse v en rpm
def tourner_droite(v):
	dxl_io.set_moving_speed({1: v})
	dxl_io.set_moving_speed({2: v})

# fait tourner sur lui meme le robot vers la gauche a une vitesse ev en rpm
def tourner_gauche(v):
	dxl_io.set_moving_speed({1: -v})
	dxl_io.set_moving_speed({2: -v})

###############################################################################

video_capture = cv2.VideoCapture(0)

video_capture.set(3, 160)

video_capture.set(4, 120)

while(True):

    t0 = time.time()
    # Capture the frames

    ret, crop_img = video_capture.read()
    #print("I get ret");
#    crop_img = frame[60:120, 0:160]

    # Convert to grayscale
    if not (ret):
	print("Couldn't receive image from camera")
    else:
	
      #  print ("I get ret");        
        red = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
	lower_red = np.array([0,100,100]);
	upper_red = np.array([20,255,255]);

	mask1 = cv2.inRange(red, lower_red, upper_red)
	
# 	res = cv2.bitwise_and(crop_img,crop_img, mask=mask1)
#	print("I apply grayscale")
    # Gaussian blur

       # blur = cv2.GaussianBlur(res,(5,5),0)
 #   	print("I apply gaussian")
    # Color thresholding

        #ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
        #mask = cv2.erode(thresh.copy(), None, iterations=2)
        #mask = cv2.dilate(mask, None, iterations=2)
    # Find the contours of the frame
#	gray = cv2.cvtColor(res.copy(), cv2.COLOR_BGR2GRAY)
        contours,hierarchy = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the biggest contour (if detected)

        if len(contours) > 0:

            c = max(contours, key=cv2.contourArea)

            M = cv2.moments(c)

            if(M['m00']!=0):
	   	cx = int(M['m10']/M['m00'])
	        cy = int(M['m01']/M['m00'])
	    else: 
		cx = 93
		cy = 0
	    print(cx)


            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)

            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1) 

            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
        
            if cx >= 92:
                print ("Turn Right!")
                tourner_droite(9)
#		avancer(10)

            elif cx < 92 and cx >52:
                print ("On Track!")
                avancer(30)
     
            elif cx <= 52:
                print ("Turn Left")
                tourner_gauche(9)
#		avancer(10)
        
            else:
                print ("I don't see the line")
                #avancer(0)
	  
    #Display the resulting frame

        cv2.imshow('frame',crop_img)
        cv2.imshow('mask', mask1)
#	avancer(0)
	
        time.sleep(1/30.0)
	t1 = time.time()
    	delta = t1 - t0
    	if delta != 0:
	    print("freq={}".format(1.0/delta))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#        time.sleep(1/30.0)
