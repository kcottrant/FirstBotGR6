import pypot.dynamixel
import numpy
import itertools
import time
import math

d=0.069 # distance entre centre du robot et les roues
r=0.0555 # rayon d'une roue

# cherche un port et se connecte au premier qu'il trouve
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io = pypot.dynamixel.DxlIO(ports[0])
print("Connected")

#print("Scanning")
#found = dxl_io.scan()
#print(found)

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

# fait tourner le robot vers la droite  d'un angle angle en radian, a une vitesse vitesse en metre par seconde et pendant un temps 
# temps en seconde
def tourner_droite_angle(angle, vitesse, temps):
	theta=angle/temps
	w1 = (vitesse + theta * d)/r
	w2 = (vitesse - theta * d)/r
	w1 = (60/(2*math.pi))*w1*1.6
	w2 = (60/(2*math.pi))*w2*1.6
	dxl_io.set_moving_speed({1: w1})
	dxl_io.set_moving_speed({2: -w2})
	time.sleep(temps)
	dxl_io.set_moving_speed({1: 0})
	dxl_io.set_moving_speed({2: 0})


# fait tourner le robot vers la gauche d'un angle angle en radian, a une vitesse vitesse en metre par seconde et pendant un temps 
# temps en seconde
def tourner_gauche_angle(angle, vitesse, temps):
	theta=angle/temps
	w1 = (vitesse + theta * d)/r
	w2 = (vitesse - theta * d)/r
	w1 = (60/(2*math.pi))*w1*1.6 # convertion en rotation par minute
	w2 = (60/(2*math.pi))*w2*1.6
	dxl_io.set_moving_speed({1: -w1})
	dxl_io.set_moving_speed({2: w2})
	time.sleep(temps)
	dxl_io.set_moving_speed({1: 0})
	dxl_io.set_moving_speed({2: 0})

# dxl_io.enable_torque((1,2))
# dxl_io.disable_torque((1,2))

# fait aller le robot a la position (x,y) avec un angle de theta disant que son point de depart est (0, 0) et son angle de depart
# est 0 degre
def va_position (x, y, theta):
	theta = theta + 0.20
	
	a = math.atan2(y,x)
	print(a)
	if a>0:
		tourner_gauche_angle(a,0,4)
	elif a<0:
		tourner_droite_angle(-a,0,4)
	dist = calcul_distance(x, y)
	vitesse = 0.05
	time.sleep(1)
	avance_distance(vitesse, dist)
	a = theta - a
	print (a)
	time.sleep(1)
	if a>0:
		tourner_gauche_angle(a, 0 ,4)
	elif a<0:
		tourner_droite_angle(-a,0,4)

def avance_distance(vitesse, dist):
	tourner_droite_angle(0,vitesse, dist/vitesse)	

# angle a - angle b
def diff_angle (a, b):
	val = a - b
	if val>math.pi:
		val = val-(2*math.pi)
		return val
	if val<-math.pi:
		val = val + (2*math.pi)
	return val

def calcul_distance(x,y):
	return math.sqrt(math.pow(x,2)+math.pow(y,2))

# tourner_droite_angle(math.pi,0,4)
va_position(0.92,-0.25,math.pi)
#avance_distance(0.05,0.2)
