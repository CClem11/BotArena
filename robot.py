# -*- coding:utf8 -*-
import pygame
from math import acos, degrees, cos, sin, tan, pi
from random import randrange
from time import time
from projectile import *
from webcam import *



def angle(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	distance = ((x2-x1)**2+(y2-y1)**2)**(1/2.)
	angle = acos((x2-x1)/(distance))
	if (y2-y1)/distance < 0:
		angle = angle * -1
	return angle

class Robot():
	def __init__(self, game_display, position_initiale, name="Player 1"):
		self.name = name
		self.game_display = game_display
		#print("Dimension de la map pour robot:", pygame.display.get_surface().get_size())
		self.position = position_initiale
		self.color = (100, 100, 250)
		self.deplacement_up = 0
		self.deplacement_down = 0
		self.deplacement_right = 0
		self.deplacement_left = 0
		self.vitesse_deplacement = 15
		self.t_touche = 0
		self.projectiles = []
		self.vie = 100
		self.alive = True
		self.canon_actif = True
		self.dernier_tir = 0
		self.longueur = 55
		self.temps_rechargement = 0 # secondes
		self.angle_canon = 0
		self.rayon = 25
		self.type_projectile = Projectile
		#images
		self.img_chassis = pygame.image.load("ressources/chassis3.png")
		########
		self.portrait = Portrait()
		# self.img_chassis = pygame.image.load("ressources/img.png").convert_alpha()
		# self.img_chassis = pygame.transform.scale(self.img_chassis, (300, 200))
		############
		self.img_canon3 = pygame.image.load("ressources/canon tourelle.png")
		self.img_chassis_touche = pygame.image.load("ressources/chassis3_touche.png")
		self.img_chassis_mort = pygame.image.load("ressources/chassis3_mort.png")
		pygame.font.init()
		pygame.mixer.pre_init(44100, -16, 1, 512) # a cause du delais
		pygame.mixer.init()
		self.sons = []
		self.sons.append(pygame.mixer.Sound(file='ressources/shot1.wav'))
		self.sons.append(pygame.mixer.Sound(file='ressources/shot2.wav'))
		self.sons.append(pygame.mixer.Sound(file='ressources/shot3.wav'))
		for sound in self.sons:
			sound.set_volume(0.1)
		self.son_touched = pygame.mixer.Sound(file='ressources/touched.wav')
		self.son_touched.set_volume(0.1)
		self.son_vie = pygame.mixer.Sound(file='ressources/vie.wav')
		self.son_vie.set_volume(0.1)
		
		print(pygame.surfarray.get_arraytype())
		print(pygame.surfarray.get_arraytypes())
		
		

	def afficher(self):
		# self.img_chassis = self.portrait.actualiser()
		# self.img_chassis = pygame.surfarray.make_surface(self.img_chassis)
		# self.img_chassis = pygame.transform.rotate(self.img_chassis, 270)
		# self.portrait.actualiser()
		# self.img_chassis = pygame.image.load("ressources/img.png").convert_alpha()
		# self.img_chassis = pygame.transform.scale(self.img_chassis, (300, 200))
		self.afficher_nom()
		self.afficher_vie()
		self.afficher_chassis()
		self.afficher_canon()
		self.afficher_projectiles()
	
	def afficher_nom(self):
		x, y = self.position
		font = pygame.font.SysFont("Arial Black", 15)
		label = font.render(self.name, 1, (255,255,255))
		largeur, hauteur = font.size(self.name)
		self.game_display.blit(label, (x-largeur/2, y-self.rayon-30-hauteur))
	
	def afficher_vie(self):
		x, y = self.position
		largeur = 50 # pixels
		pygame.draw.rect(self.game_display, (0, 100, 0), (x-int(largeur/2), y-self.rayon-30, largeur, 10))
		pygame.draw.rect(self.game_display, (0, 200, 0), (x-int(largeur/2), y-self.rayon-30+1, int((largeur*self.vie/100)), 10-1))		
	
	def afficher_chassis(self):
		x, y = self.position
		if time() - self.t_touche < 0.05:
			self.game_display.blit(self.img_chassis_touche, (x-25, y-25))
		elif not self.alive:
			self.game_display.blit(self.img_chassis_mort, (x-25, y-25))
		else:
			w, h = pygame.Surface.get_size(self.img_chassis)
			self.game_display.blit(self.img_chassis, (x-w/2, y-h/2))
		
	def afficher_canon(self):
		largeur = 10
		longueur = self.longueur
		x, y = self.position
		#image avec canon centre - plus simple !!!!!
		w, h = pygame.Surface.get_size(self.img_canon3)
		canon = pygame.transform.rotate(self.img_canon3, 360-degrees(self.angle_canon))
		canon_x, canon_y = pygame.Surface.get_size(canon)
		self.game_display.blit(canon, (x-canon_x/2, y-canon_y/2))
		
	def afficher_projectiles(self):
		for projectile  in self.projectiles:
			if projectile.move(): # deplacement + etre dans la fenetre
				projectile.afficher()
			else: # sinon on le supprime
				self.projectiles.remove(projectile)
		
	def changer_vitesse(self, direction):
		"deplacement du robot"
		if direction == 'N':
			self.deplacement_up = self.vitesse_deplacement
		elif direction == 'S':
			self.deplacement_down = self.vitesse_deplacement
		if direction == 'W':
			self.deplacement_left = self.vitesse_deplacement
		elif direction == 'E':
			self.deplacement_right = self.vitesse_deplacement
	
	def move(self):
		# vitesse cheated en diagonale !
		if self.alive == True:
			x, y = self.position
			delta_x = self.deplacement_right-self.deplacement_left
			delta_y = self.deplacement_down-self.deplacement_up
			if delta_x != 0 and delta_y != 0: # deplacement sur 2 axes
				#print("Deplacement sur les 2 axes")
				delta_x /= 2**(1/2.) #racine de 2
				delta_y /= 2**(1/2.) #racine de 2
			x += int(delta_x)
			y += int(delta_y)
			fenetre = pygame.display.get_surface().get_size()
			if x - self.rayon <= 0 or x + self.rayon > fenetre[0]:
				x = self.position[0]
			if y - self.rayon <= 0 or y + self.rayon > fenetre[1]:
				y = self.position[1]
			self.position = (x, y)
	
	def orienter_canon(self, cible):
		if self.canon_actif:
			self.angle_canon = angle(self.position, cible)
	
	def arreter(self, direction):
		"mets les vitesses de deplacement en x et y a 0"
		if direction == 'N':
			self.deplacement_up = 0
		elif direction == 'S':
			self.deplacement_down = 0
		if direction == 'W':
			self.deplacement_left = 0
		elif direction == 'E':
			self.deplacement_right = 0
			
	def tir(self):
		if time() - self.dernier_tir > self.temps_rechargement:
			#print("temps depuis le dernier tir :{:.3}".format(time()-self.dernier_tir))
			x, y = self.position
			x_canon = int(self.longueur*cos(self.angle_canon))
			y_canon = int(self.longueur*sin(self.angle_canon))
			self.projectiles.append(self.type_projectile(self.game_display, (x+x_canon, y+y_canon), self.angle_canon))
			#son
			pygame.mixer.Sound.play(self.sons[randrange(len(self.sons))])
			self.dernier_tir = time()
		
	def get_projectiles(self):
		return self.projectiles
	
	def toucher(self):
		"le robot est touche par un projectile"
		if self.alive == True:
			self.t_touche = time()
			if self.vie > 0:
				self.vie -= 5
			if self.vie <= 0:
				self.mort()
			pygame.mixer.Sound.play(self.son_touched)
	
	def mort(self):
		self.alive = False
		self.canon_actif = False
		new_color = []
		for c in self.color:
			new_color.append(int(c/2))
		self.color = new_color
	
	def get_informations(self):
		"retourne une chaine au bon format (pour envoyer les donnees)"
		parametres = {}
		parametres["position"] = self.position
		parametres["angle"] = self.angle_canon
		parametres["vie"] = self.vie
		message = "actualiser_informations/"
		for parametre, valeur in parametres.items():
			message += str(parametre) + ':' + str(valeur) + '*'
		message = message[:-1] # enleve le dernier '-' (separateur de parametre)
		return message
	
	def ressuciter(self):
		self.alive = True
		self.vie = 100
		pygame.mixer.Sound.play(self.son_vie)
