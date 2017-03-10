# -*- coding:utf8 -*-
from math import cos, sin, acos

def angle(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	distance = ((x2-x1)**2+(y2-y1)**2)**(1/2.)
	angle = acos((x2-x1)/(distance))
	if (y2-y1)/distance < 0:
		angle = angle * -1
	return angle

def distance_carre(x1, y1, x2, y2):
	"calcul distance au carre entre 2 points"
	return (x2-x1)**2 + (y2-y1)**2

def distance(x1, y1, x2, y2):
	return distance_carre(x1, y1, x2, y2)**(1/2.)
	
def decoupage_deplacement(position_initiale, position_finale, nombre_points):
	"pour faire du substeps :)"
	# print(position_initiale, "->", position_finale)
	if position_initiale != position_finale and nombre_points != 0:
		angle1 = angle(position_initiale, position_finale)
		x1, y1 = position_initiale
		x2, y2 = position_finale
		d = distance(x1, y1, x2, y2)
		delta_d = d/nombre_points
		points = []
		for i in range(1, nombre_points):
			x = x1 + int(i*delta_d*cos(angle1))
			y = y1 +int(i*delta_d*sin(angle1))
			points.append((x, y))
		points.append(position_finale)
		return points
	else:
		return [position_initiale]
			