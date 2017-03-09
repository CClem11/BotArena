# -*- coding:utf8 -*-
import pygame
from math import acos, degrees, cos, sin, tan, pi
from random import randrange
from time import time
from projectile import Projectile
# from webcam import *
from collision import *
from math_jeu import angle, decoupage_deplacement


class Robot():
	def __init__(self, game_display, map, position_initiale, name="Player 1"):
		self.name = name
		self.game_display = game_display
		self.fenetre = pygame.display.get_surface().get_size()
		self.map = map
		#print("Dimension de la map pour robot:", pygame.display.get_surface().get_size())
		self.position = list(position_initiale)
		self.color = (100, 100, 250)
		self.deplacement = {"Up":0, "Down":0, "Left":0, "Right":0, }
		self.vitesse_deplacement = 18 # pixel/frame
		self.t_touche = 0
		self.projectiles = []
		self.vie = 100
		self.alive = True
		self.canon_actif = True
		self.dernier_tir = 0
		self.longueur = 55
		self.temps_rechargement = 0 # secondes
		self.angle_canon = 0 #en debut de partie
		self.type_projectile = Projectile #bientot SnipProj ...
		#images
		self.img_chassis = pygame.image.load("ressources/chassis3.png")
		self.rayon = int(pygame.Surface.get_size(self.img_chassis)[0]/2)
		########
		# self.portrait = Portrait()
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
		
		# print(pygame.surfarray.get_arraytype())
		# print(pygame.surfarray.get_arraytypes())
		# print(self.map)	

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
		# self.afficher_aabb_hitbox()
	
	def afficher_nom(self):
		x, y = self.position
		font = pygame.font.SysFont("Arial Black", 15)
		label = font.render(self.name, 1, (255,255,255))
		# label = font.render(str(self.position), 1, (255,255,255))
		largeur, hauteur = font.size(self.name)
		self.game_display.blit(label, (x-largeur/2, y-self.rayon-30-hauteur))
	
	def afficher_vie(self):
		x, y = self.position
		largeur = 50 # pixels
		pygame.draw.rect(self.game_display, (0, 100, 0), (x-int(largeur/2), y-self.rayon-30, largeur, 10))
		if self.alive:
			pygame.draw.rect(self.game_display, (0, 200, 0), (x-int(largeur/2), y-self.rayon-30+1, int((largeur*self.vie/100)), 10-1))		
		else:
			pass
		
	def afficher_chassis(self):
		x, y = self.position
		if time() - self.t_touche < 0.05:
			self.game_display.blit(self.img_chassis_touche, (x-25, y-25))
		elif not self.alive:
			self.game_display.blit(self.img_chassis_mort, (x-25, y-25))
		else:
			w, h = pygame.Surface.get_size(self.img_chassis)
			# print(w, h)
			self.game_display.blit(self.img_chassis, (x-w/2, y-h/2))
	
	def afficher_aabb_hitbox(self):
		x, y = self.position
		r = self.rayon
		pygame.draw.rect(self.game_display, (0, 255, 0), (x-r,y-r,r*2,r*2), 1)
		
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
		self.deplacement[direction] = True
	
	def arreter(self, direction):
		"mets les vitesses de deplacement en x et y a 0"
		self.deplacement[direction] = False
	
	def move(self):
		if self.alive == True:
			x0, y0 = self.position
			x, y = self.position
			delta_x = self.deplacement["Right"]-self.deplacement["Left"]
			delta_y = self.deplacement["Down"]-self.deplacement["Up"]
			if delta_x != 0 or delta_y != 0: #déplacement
				angle_deplacement = angle((0, 0,), (delta_x, delta_y))
				partie_x_angle = int(self.vitesse_deplacement*cos(angle_deplacement))
				partie_y_angle = int(self.vitesse_deplacement*sin(angle_deplacement))
				#test de collision dans le mur (obstacle)
				#faire du substeps !
				deplacement_accorde = True
				collision = False
				points = decoupage_deplacement(self.position, (x+partie_x_angle, y+partie_y_angle), self.vitesse_deplacement)
				for i, point in enumerate(points):
					if not collision and not self.deplacement_possible(point):
						if i != 0:
							self.position = points[i-1]
						# print(i)
						collision = True
						deplacement_accorde = False
						break
				# pour permettre le glissage sur obstacle
				# on test egalement le déplacement pour la partie x uniquement, puis la partie y du mouvement
				if delta_x and not deplacement_accorde:
					collision = False
					points = decoupage_deplacement(self.position, (x+delta_x*self.vitesse_deplacement, y), self.vitesse_deplacement)
					for i, point in enumerate(points):
						if not collision and not self.deplacement_possible(point):
							if i != 0:
								self.position = points[i-1]
							collision = True
							break
					if i+1 == self.vitesse_deplacement:
						#pas de collision : deplacement accepte
						self.position = (x+partie_x_angle, y)
				# puis en y
				if delta_y and not deplacement_accorde:
					collision = False
					points = decoupage_deplacement(self.position, (x, y+delta_y*self.vitesse_deplacement), self.vitesse_deplacement)
					for i, point in enumerate(points):
						if not collision and not self.deplacement_possible(point):
							if i != 0:
								self.position = points[i-1]
							collision = True
							break
					if i+1 == self.vitesse_deplacement:
						#pas de collision : deplacement accepte
						self.position = (x, y+partie_y_angle)
				#aucune collision :
				if not collision and deplacement_accorde:
					print("aucune collision")
					self.position = (x+partie_x_angle, y+partie_y_angle)
					
	def deplacement_possible(self, position_voulu):
		"test si il n'y a pas collision avec la nouvelle position"
		x_voulu, y_voulu = position_voulu
		if x_voulu - self.rayon <= 0 or x_voulu + self.rayon > self.fenetre[0]:
			return False
		elif y_voulu - self.rayon <= 0 or y_voulu + self.rayon > self.fenetre[1]:
			return False
		#dans fenetre -> test de collision avec la map
		for rectangle in self.map:
			x1, y1, x2, y2 = rectangle
			aabb = (x1, y1, x2-x1, y2-y1)
			if Cercle_AABB((x_voulu, y_voulu), self.rayon, aabb, self.game_display):
				return False
		return True
				
	def orienter_canon(self, cible):
		if self.canon_actif:
			self.angle_canon = angle(self.position, cible)
			
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
