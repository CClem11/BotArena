# -*- coding:utf8 -*-
import pygame
"""
Différents objets traités
-Point : définit par (x, y)
-Cercle : définit par (x, y) + rayon
-AABB : Axis Aligned Bounding Box : rectangle "droit" définit par 2 coins opposés 
						ou coin supérieur gauche plus longeur et hauteur 
-OBB:  Oriented Bounding Box : rectangle incliné définit par 4 points
"""
from math_jeu import distance_carre

def Point_AABB(point, aabb):
	x, y = point
	x1, y1, longueur, hauteur = aabb
	if x1 <= x <= x1+longueur:
		if y1 <= y <= y1+hauteur:
			return True
	return False

def Point_Cercle(point, centre_cercle, rayon):
	x, y = point
	x0, y0 = centre_cercle
	if distance_carre(x, y, x0, y0) <= rayon**2:
		return True
	else:
		return False
	
def AABB_AABB(aabb1, aabb2, game_display):
	x1, y1, w1, h1 = aabb1
	x2, y2, w2, h2 = aabb2
	# pygame.draw.rect(game_display, (255, 0, 0), aabb1, 3)
	# pygame.draw.rect(game_display, (255, 0, 0), aabb2, 3)
	if x1+w1 < x2 or x1 > x2+w2 or y1+h1 < y2 or y1 > y2+h2: #trop a gauche, droite, bas, haut
		return False
	else:
		return True
		
def Cercle_AABB(centre_cercle, rayon, aabb, display):
	x, y = centre_cercle
	x1, y1, w1, h1 = aabb
	aabb_cercle = (x-rayon, y-rayon, rayon*2, rayon*2)
	# pygame.draw.rect(display, (255, 0, 255), aabb_cercle, 5)
	#plusieurs tests 
	#Test 1 : test grossier entre les aabb du cercle et du rectangle
	if AABB_AABB(aabb_cercle, aabb, display):
		#Test 2 : test si un des sommet de aabb est dans cercle:
		for x_s, y_s in [(x1, y1), (x1+x1, y1), (x1, y1+h1), (x1+w1, y1+h1)]:
			if distance_carre(x_s, y_s, x, y) <= rayon**2:
				# print("Test 2 Point-Cercle")
				return True
		#Test 3 : centre du cercle dans aabb ?
		if Point_AABB((x, y), aabb):
			# print("Test 3 Point-AABB (centre dans obstacle) avec aabb:", aabb)
			return True
		#Test 4 : Projecter le centre du cercle sur les cotés de aabb
		# A FAIRE !!!
		# print("par défaut")
		return True
	else:
		# print("Test 1 AABB-AABB")
		return  False


class Vecteur():
	def __init__(self, p1, p2):
		self.p1, self.p2 = p1, p2
		self.x = p2[0] - p1[0]
		self.y = p2[1] - p1[1]
	def __repr__(self):
		return "Vecteur({}, {})".format(self.x, self.y)	
		
#non utilisé	
def collision_polygone_point(polygone, point):
	"entre polygone convexe et point - Point_OOBB"
	#si le point est a l'interieur du polygone alors collision
	#le point est a l'intereieur si et seulement si a gauche 
	#de chacun de ces cotes dans le sens anti-horaire
	if len(polygone) >= 3: # sinon pas polygone
		vecteurs = []
		p1 = polygone[-1]
		for p2 in polygone:
			vecteurs.append(Vecteur(p1, p2))
			p1 = p2
		print(vecteurs)
		
	for vecteur in vecteurs:
		vecteur_point = Vecteur(vecteur.p1, point)
		determinant = vecteur.x*vecteur_point.y - vecteur.y*vecteur_point.x
		print("determinant :", determinant)
		if determinant < 0:
			#point pas dans polygone
			return False
	return True # le point a passe tout les tests
	
if __name__ == '__main__':
	polygone = [(0, 0), (1, -2), (5, 0), (4, 2)]
	collision_polygone_point(polygone, (4, 3))