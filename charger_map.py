# -*- coding:utf8 -*-
import pygame

marqueur_vide = "-"
marqueur_plein = "#"

class Map():
	def __init__(self, game_display, fenetre, taille_obstacle):
		self.chemin_fichier = "ressources/map2.txt"
		self.chemin_obstacle = "ressources/mur.png"
		self.img_obstacle = pygame.image.load(self.chemin_obstacle).convert_alpha()
		self.map = []
		self.map_pixel = []
		self.fenetre = fenetre
		self.taille_obstacle = taille_obstacle
		self.ouvrir_map()
		self.create_map_pixel()
		self.game_display = game_display
	
	def ouvrir_map(self):
		with open(self.chemin_fichier, 'r') as fichier:
			self.map = []
			for l, ligne in enumerate(fichier.readlines()):
				for c, caractere in enumerate(ligne):
					if caractere == marqueur_plein:
						self.map.append((c, l))
			# print(self.map)
	
	def create_map_pixel(self):
		for position in self.map:
			x, y = position
			x *= self.taille_obstacle
			y *= self.taille_obstacle
			self.map_pixel.append((x, y, x+self.taille_obstacle, y+self.taille_obstacle))
		# print(self.map_pixel)
			
	def afficher(self):
		img = pygame.transform.scale(self.img_obstacle, (self.taille_obstacle, self.taille_obstacle))
		for position in self.map_pixel:
			x, y = position[:2]
			self.game_display.blit(img, position)
			# pygame.draw.rect(self.game_display, (100, 100, 100), (x, y, self.taille_obstacle, self.taille_obstacle), 2)
	def get_map(self):
		return self.map_pixel

if __name__ == '__main__':
	ouvrir_map(map2)