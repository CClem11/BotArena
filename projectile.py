from __future__ import print_function
# -*- coding:utf8 -*-

#pour le projectile
import pygame
from math import cos, sin, radians, degrees, pi
from time import sleep, time
from random import randrange

if False: #si sur un ordi sous ubuntu
	chemin_projet = "/home/isn/projet/"
else:
	chemin_projet = ""

def couleur_aleatoire():
	return [127*randrange(3) for i in range(3)] # peut etre noir

class Projectile():
	def __init__(self, game_display, position_initiale, angle, vitesse=28):

		#print("projectile creer : angle : {}".format(angle))
		self.game_display = game_display
		self.dimension_fenetre = pygame.display.get_surface().get_size()
		self.color = couleur_aleatoire() #couleur aleatoire
		self.position, self.angle, self.vitesse = list(position_initiale), angle, vitesse
		self.rayon = 20
		
		self.angle_dispersion = 0 # degrees (INT !)
		if self.angle_dispersion != 0:
			self.angle += radians(randrange(-self.angle_dispersion, +self.angle_dispersion))
			
		self.img = pygame.image.load(chemin_projet+"ressources/proj3.png").convert_alpha()
		# self.img = pygame.image.load("ressources/balle1.png")
		self.angle_img = 0
		
	def move(self):
		self.position[0] += int(self.vitesse*cos(self.angle))
		self.position[1] += int(self.vitesse*sin(self.angle))
		return True
	
	def afficher(self, camera_position):
		x1, y1 = self.position
		x0, y0 = camera_position
		x, y = x1-x0, y1-y0
		pygame.draw.circle(self.game_display, self.color, (x, y), self.rayon)
		# img = pygame.transform.rotate(self.img, self.angle_img)
		# w, h = pygame.Surface.get_size(img)
		# x -= w/2
		# y -= h/2
		# self.game_display.blit(self.img, (x, y))

class Projectile2(Projectile):
	"avec rebonds"
	def __init__(self, game_display, position_initiale, angle, vitesse=25):
		Projectile.__init__(self, game_display, position_initiale, angle)
		self.rebond = True
		
	def move(self):
		#self.angle_img -= 8

		x, y = self.position
		# print("x, y :", x, ", ", y)
		x += int(self.vitesse*cos(self.angle))
		y += int(self.vitesse*sin(self.angle))
		# print("x, y :", x, ", ", y)
		self.position = (x, y)
			
		# if 0 > x or x > self.dimension_fenetre[0]: #marche si fenetre fixe
			# if self.rebond:
				# self.angle = -1*(self.angle + pi)
				# self.rebond = False
				# return True
			# else:
				# return False
		# elif 0 > y or y > self.dimension_fenetre[1]:
			# if self.rebond:
				# self.angle = -1*self.angle
				# self.rebond = False
				# return True
			# else:
				# return False
		# else:
			# return True
		return True
			
		
class Explosion():
	
	def __init__(self, game_display,):
		self.game_display = game_display
		self.img = pygame.image.load(chemin_projet+"ressources/explosion2.png").convert_alpha()
		self.img = pygame.transform.scale(self.img, (50, 50))
		self.w, self.h = pygame.Surface.get_size(self.img)
		self.temps_explosion = 0.15
		
		self.explosions = []
		
	def afficher(self, camera_position):
		x0, y0 = camera_position
		for explosion in self.explosions:
			position, t0 = explosion
			if time() - t0 < self.temps_explosion:
				x1, y1 = position
				x, y = x1-x0, y1-y0
				self.game_display.blit(self.img, (x-self.w/2, y-self.h/2))
			else:
				self.explosions.remove(explosion)
				
	def nouvelle_explosion(self, position):
		self.explosions.append((position, time()))

#copie
class Fumee():
	def __init__(self, game_display,):
		self.game_display = game_display
		self.img = pygame.image.load(chemin_projet+"ressources/fumee_tir.png").convert_alpha()
		self.img = pygame.transform.scale(self.img, (50, 50))
		self.w, self.h = pygame.Surface.get_size(self.img)
		self.temps_tir = 0.05
		self.tirs = []
		
	def afficher(self, camera_position):
		x0, y0 = camera_position
		for tir in self.tirs:
			position, agle, t0, img = tir
			x1, y1 = position
			x, y = x1-x0, y1-y0
			if time() - t0 < self.temps_tir:
				self.game_display.blit(img, (x, y))
			else:
				self.tirs.remove(tir)
				
	def nouvelle_fumee(self, position, angle_radian):
		img = pygame.transform.rotate(self.img, 360-degrees(angle_radian))
		x, y = position
		w, h = pygame.Surface.get_size(img)
		position = (x-w/2, y-h/2)
		self.tirs.append((position, angle_radian, time(), img))	
