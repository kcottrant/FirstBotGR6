import pypot.dynamixel
import numpy
import itertools
import time
import math

d=0.069
r=0.0255

def diff_angle (a, b):
        val = a - b
        if val>math.pi:
                val = val-(2*math.pi)
                return val
        if val<-math.pi:
                val = val + (2*math.pi)
        return val

ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')

dxl_io = pypot.dynamixel.DxlIO(ports[0])
print("Connected")

dxl_io.set_wheel_mode([1])
dxl_io.set_wheel_mode([2])

dxl_io.disable_torque((1,2))

roule = False

dist_tot= 0
angle_tot = 0
coor_x=0
coor_y=0

while roule == False:
	w1 = dxl_io.get_present_speed((1,))[0]
        w2 = -dxl_io.get_present_speed((2,))[0]
	if abs(w1) >= 0.6 and  abs(w2)>=0.6:
		roule = True
t_passe = 0.005

while roule:
	to = time.time()
	w1 = dxl_io.get_present_speed((1,))[0]
	w2 = -dxl_io.get_present_speed((2,))[0]

	# transforme les rpm en rad/s
	w1 = (w1*1.339*2*math.pi)/60
	w2 = (w2*1.339*2*math.pi)/60

	# condition pour arreter la boucle
	if w1==0 and w2 ==0:
		roule = False

	# cinematique inverse
	vit_lin = (r*w1 + r*w2)/2
	vit_ang = (r*w1 - r*w2)/(2*d)

	# calcul distances et angles
	dist = vit_lin*t_passe
	ang = -vit_ang*t_passe

	# distance et angle depuis le debut
	dist_tot = dist_tot + dist
	angle_tot = angle_tot + ang
	if angle_tot >= math.pi*2:
		angle_tot = diff_angle(angle_tot, ((angle_tot//(2*math.pi)) * 2*math.pi))
#		angle_tot = angle_tot - ((angle_tot//(2*math.pi)) * 2*math.pi)
		print("boucle 1 ")
	if angle_tot<=-math.pi*2:
		print("angle tot :")
		print(angle_tot)
		angle_tot = diff_angle(angle_tot, ((angle_tot//(2*math.pi)) * 2*math.pi))
#		angle_tot = angle_tot - ((angle_tot//(2*math.pi)) * 2*math.pi)
		print("boucle 2")

	# calul des nouvelles coordonnees:
	if vit_ang != 0:
		print("tourne")
		R = vit_lin/vit_ang #rayon
		print("R : ")
		print(R)
		#  nouvelle position
		print("****")
		print("sinus ang")
		print(math.sin(ang))
		print("cos ang")
		print(math.cos(ang))
		print("******")
		
		alpha = R*math.sin(ang)
		betha = R-R*math.cos(ang)

#		if math.sin(ang)>=0:
#			alpha = R*math.sin(ang)
#			print("coor x")
#			print(coor_x)
#			if math.cos(ang) <=0:
#				betha = R-R*math.cos(ang)
#			else:
#				betha =  -1* R-R*math.cos(ang)
#		else :
#			alpha= -1*R*math.sin(ang)
 #                       if math.cos(ang) <=0:
  #                              betha =  R-R*math.cos(ang)
   #                     else:
    #                            betha =  -1*R-R*math.cos(ang)
	else:
		print("droit")
		alpha =  dist
		betha =  0
	t_passe = time.time() - to
	
	#coordonee dans le monde
	coor_y += alpha*math.cos(angle_tot) - math.sin(angle_tot)*betha
	coor_x += -math.sin(angle_tot)*alpha - math.cos(angle_tot)*betha
coor_y = -coor_y
coor_x = -coor_x	
print("-----")
print("la distance totale parcourue par le robot (en metre) est :")
print (dist_tot)
print("l\'angle d\'arrive du robot (en rad) est:")
print(angle_tot)
print("----")
print("Coord de x :")
print(coor_x)
print("Coord de y :")
print(coor_y)
print("******")
