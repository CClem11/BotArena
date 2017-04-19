from __future__ import print_function
# -*- coding:utf8 -*-
import pygame
import numpy as np

if False: #si sur un ordi sous ubuntu
	chemin_projet = "/home/isn/projet/"
else:
	chemin_projet = ""

marqueur_vide = "-"
marqueur_plein = "#"

class Map():
	def __init__(self, game_display, fenetre, taille_obstacle):
		self.chemin_fichier = chemin_projet+"ressources/arena.txt"	#"ressources/map_kayhan_fred.txt"
		self.chemin_obstacle = chemin_projet+"ressources/mur.png"
		self.img_obstacle = pygame.image.load(self.chemin_obstacle).convert_alpha()
		self.map = []
		self.map_pixel = []
		self.fenetre = fenetre
		self.taille_obstacle = taille_obstacle #longueur=hauteur
		self.ouvrir_map()
		self.create_map_pixel()
		self.game_display = game_display
		self.creer_image_map()
		self.mini_map = pygame.transform.scale(self.image_map, (304, 171))
		self.mini_map.set_alpha(100)
		
		#objet de Map (différentes représentation) : 
			#map_pixel : liste de rectangle (bloc) mais en pixel (x1, y1, x2, y2)
			#map_bloc : tableau de la position des blocs avec comme valeur True/False <=> obstacle/vide
			#map : liste des bloc (seulement les True de map_bloc)
			#image_map : image de la map entière
	
	def give_empty_bloc(self):
		"retourne un emplacement vide"
		return self.map[randrange(len(self.map))]
	
	def ouvrir_map(self):
		with open(self.chemin_fichier, 'r') as fichier:
			self.map = []
			self.map_bloc = {} #pour collision optimisée
			max_bloc_x, max_bloc_y = 0, 0
			for l, ligne in enumerate(fichier.readlines()):
				if ligne != "" and ligne != "\n":
					if l > max_bloc_y:
						max_bloc_y = l
					for c, caractere in enumerate(ligne):
						if c > max_bloc_x:
							max_bloc_x = c
						if caractere == marqueur_plein:
							self.map.append((c, l))
							self.map_bloc[(c, l)] = True
						else:
							self.map_bloc[(c, l)] = False
			self.nombre_bloc_max = max_bloc_x, max_bloc_y
			# print(self.nombre_bloc_max, "or :", self.fenetre[1]/self.taille_obstacle)
			# print(self.map)
			# print(self.map_bloc)
	
	def create_map_pixel(self):
		for position in self.map:
			x, y = position
			x *= self.taille_obstacle
			y *= self.taille_obstacle
			self.map_pixel.append((x, y, x+self.taille_obstacle, y+self.taille_obstacle))
		# print(self.map_pixel)
		
	def creer_image_map(self):
		"fonction qui créer l'image de la map"
		#récuperer le nombre d'image a utilisé pour faire l'image map
		w, h = self.nombre_bloc_max
		t = self.taille_obstacle
		obstacle = pygame.transform.scale(self.img_obstacle, (t, t))
		obstacle = pygame.surfarray.array3d(obstacle)
		image = np.zeros(((w)*t, (h+1)*t, 3), np.uint8)
		for position in self.map_pixel:
			# print(position[:2])
			x, y = position[:2]
			image[x:x+t, y:y+t] = obstacle
		self.image_map = pygame.surfarray.make_surface(image)
		pygame.image.save(self.image_map, "ressources/map_generee.jpg")
			
	def afficher(self, camera_position):
		x0, y0 = camera_position
		img = pygame.transform.scale(self.img_obstacle, (self.taille_obstacle, self.taille_obstacle))
		for position in self.map_pixel:
			x, y = position[:2]
			x, y = x-x0, y-y0
			self.game_display.blit(img, (x, y))
			# pygame.draw.rect(self.game_display, (100, 100, 100), (x, y, self.taille_obstacle, self.taille_obstacle), 2)
		# self.afficher_grille()
	
	def afficher2(self, camera_position):
		"qui affiche l'image fabriquée en début de partie"
		x, y = camera_position
		self.game_display.blit(self.image_map, (-x, -y))
	
	def afficher_grille(self):
		for x in range(1, int(self.fenetre[0]/self.taille_obstacle)+1):
			pygame.draw.line(self.game_display, (0, 200, 0), (x*self.taille_obstacle, 0), (x*self.taille_obstacle, self.fenetre[1]))
		for y in range(1, int(self.fenetre[1]/self.taille_obstacle)+1):
			pygame.draw.line(self.game_display, (0, 200, 0), (0, y*self.taille_obstacle), (self.fenetre[0], y*self.taille_obstacle))
	
	def afficher_minimap(self, position):
		self.game_display.blit(self.mini_map, position)
	
	def get_map(self):
		return self.map_pixel
	def get_map_bloc(self):
		return self.map_bloc
	
	def afficher_bloc(self, position, color):
		x, y = position
		l = self.taille_obstacle
		pygame.draw.rect(self.game_display, color, (x*l,y*l,l,l))
	
	def get_bloc_ligne(self, p1, p2):
		"retourne tous les bloc entre 2 positions"
		#retourne les blocs qui sont sur la droit reliant les 2 points
		#pour eviter de faire de la collision aux pixel pres : optimisation
		x1, y1 = p1
		x2, y2 = p2
		#equation cartesienne de la droite
		a = y2-y1
		b = x1-x2
		c = x2*y1-y2*x1
		# print("(d): {}x+{}y+{}=0".format(a, b, c))
		amplitude_x = int(min(x1, x2)/self.taille_obstacle), min(int(max(x1, x2)/self.taille_obstacle), self.nombre_bloc_max[0])
		amplitude_y = int(min(y1, y2)/self.taille_obstacle), min(int(max(y1, y2)/self.taille_obstacle), self.nombre_bloc_max[1])
		# print("amplitude bloc : ({}, {}) -> ({}, {})".format(amplitude_x[0],amplitude_y[0],amplitude_x[1], amplitude_y[1]))
		grille = []
		i = 100 #intensite de la couleur
		if b != 0:
			for x in range(amplitude_x[0],amplitude_x[1]+1):
				y1 = int((-c-a*x*self.taille_obstacle)/(b*self.taille_obstacle))
				y2 = int((-c-a*(x+1)*self.taille_obstacle)/(b*self.taille_obstacle))
				for y in range(min(y1, y2), max(y1, y2)+1):
					if amplitude_y[0] <= y <= amplitude_y[1]:
						# self.afficher_bloc((x, y), (i, 0, 0))
						grille.append((x, y))
		if a != 0:
			for y in range(amplitude_y[0],amplitude_y[1]+1):
				x1 = int((-c-b*y*self.taille_obstacle)/(a*self.taille_obstacle))
				x2 = int((-c-b*(y+1)*self.taille_obstacle)/(a*self.taille_obstacle))
				for x in range(min(x1, x2), max(x1, x2)+1):
					if amplitude_x[0] <= x <= amplitude_x[1]:
						if (x, y) not in grille:
							# self.afficher_bloc((x, y), (i, 0, 0))
							grille.append((x, y))
		# print(grille)
		# pygame.draw.line(self.game_display, (0, 255, 0), p1, p2, 1) 
		return grille

if __name__ == '__main__':
	ouvrir_map(map2)