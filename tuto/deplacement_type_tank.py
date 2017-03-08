# -*- coding:utf8 -*-
import pygame
from random import randrange
from math import cos, sin, radians

class Application():
	def __init__(self):
		self.fenetre = (500, 500)
		
		self.image = pygame.image.load("voiture1.png")
		self.image = pygame.transform.rotate(self.image, 180)
		self.position = 250, 250
		self.orientation = 0
		self.vitesse = 0
		
		self.fps = 60
		self.game_display = pygame.display.set_mode(self.fenetre)
		pygame.display.set_caption("Deplacement ++")
		self.clock = pygame.time.Clock()
		self.boucle()
	
	def dessiner_voiture(self):
		x, y = self.position
		
		img = pygame.transform.rotate(self.image, 360-self.orientation)
		w, h = pygame.Surface.get_size(img)
		self.game_display.blit(img, (x-w/2, y-h/2))
	
	def avancer(self):
		"en fonction de l'angle"
		x, y = self.position
		v = self.vitesse
		x += v*cos(radians(self.orientation))
		y += v*sin(radians(self.orientation))
		self.position = x, y
	
	def boucle(self):
		move_angle = 0
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.fin()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.fin()
					if event.key == pygame.K_LEFT:
						move_angle = -5
					if event.key == pygame.K_RIGHT:
						move_angle = 5
					if event.key == pygame.K_UP:
						self.vitesse = 5
					if event.key == pygame.K_DOWN:
						self.vitesse = -3
						
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
						self.vitesse = 0
					if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
						move_angle = 0
			
			self.orientation += move_angle
			self.game_display.fill((0, 0, 0))	#clear
			self.dessiner_voiture()
			self.avancer()
			pygame.display.update()
			self.clock.tick(self.fps)
	
	def fin(self):
		pygame.quit()
		quit()

if __name__ == '__main__':
	Application()