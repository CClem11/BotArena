# -*- coding:utf8 -*-

#pour le projectile
import pygame, threading
from math import cos, sin, radians, degrees
from time import sleep, time
from random import randrange

def couleur_aleatoire():
	return [127*randrange(3) for i in range(3)] # peut etre noir

class Projectile():
	def __init__(self, game_display, position_initiale, angle, vitesse=20):

		#print("projectile creer : angle : {}".format(angle))
		self.game_display = game_display
		self.dimension_fenetre = pygame.display.get_surface().get_size()
		self.color = couleur_aleatoire() #couleur aleatoire
		self.position_initiale, self.angle, self.vitesse = position_initiale, angle, vitesse
		self.rayon = 7
		self.position = (0, 0)
		self.deplacement = 0
		
		self.angle_dispersion = 0 # degrees (INT !)
		if self.angle_dispersion != 0:
			self.angle += radians(randrange(-self.angle_dispersion, +self.angle_dispersion))
			
		self.img = pygame.image.load("ressources/proj3.png").convert_alpha()
		#self.img = pygame.image.load("ressources/balle1.png")
		self.angle_img = 0
		
	def move(self):
		self.deplacement += 1
		#self.angle_img -= 8
		x, y = self.position_initiale
		x = x + int(self.deplacement*self.vitesse*cos(self.angle))
		y = y + int(self.deplacement*self.vitesse*sin(self.angle))
		self.position = (x, y)
		if 0 < x < self.dimension_fenetre[0] and 0 < y < self.dimension_fenetre[1]:
			return True
		else:
			#sorti de la fenetre -> on le supprime #voir robot
			return False
			
	
	def afficher(self):
		x, y = self.position
		pygame.draw.circle(self.game_display, self.color, self.position, self.rayon)
		# img = pygame.transform.rotate(self.img, self.angle_img)
		# w, h = pygame.Surface.get_size(img)
		# x -= w/2
		# y -= h/2
		# self.game_display.blit(img, (x, y))
	
class Explosion():
	
	def __init__(self, game_display,):
		self.game_display = game_display
		self.img = pygame.image.load("ressources/explosion2.png").convert_alpha()
		self.img = pygame.transform.scale(self.img, (50, 50))
		self.w, self.h = pygame.Surface.get_size(self.img)
		self.temps_explosion = 0.15
		
		self.explosions = []
		
	def afficher(self):
		for explosion in self.explosions:
			position, t0 = explosion
			if time() - t0 < self.temps_explosion:
				x, y = position
				self.game_display.blit(self.img, (x-self.w/2, y-self.h/2))
			else:
				self.explosions.remove(explosion)
				
	def nouvelle_explosion(self, position):
		self.explosions.append((position, time()))

#copie
class Fumee():
	def __init__(self, game_display,):
		self.game_display = game_display
		self.img = pygame.image.load("ressources/fumee_tir.png").convert_alpha()
		self.img = pygame.transform.scale(self.img, (50, 50))
		self.w, self.h = pygame.Surface.get_size(self.img)
		self.temps_tir = 0.05
		self.tirs = []
		
	def afficher(self):
		for tir in self.tirs:
			position, agle, t0, img = tir
			if time() - t0 < self.temps_tir:
				self.game_display.blit(img, position)
			else:
				self.tirs.remove(tir)
				
	def nouvelle_fumee(self, position, angle_radian):
		img = pygame.transform.rotate(self.img, 360-degrees(angle_radian))
		x, y = position
		w, h = pygame.Surface.get_size(img)
		position = (x-w/2, y-h/2)
		self.tirs.append((position, angle_radian, time(), img))	
