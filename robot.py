from __future__ import print_function
# -*- coding:utf8 -*-
import pygame
from math import acos, degrees, cos, sin, tan, pi
from random import randrange
from time import time
from projectile import *
# from webcam import *
from collision import *
from math_jeu import angle, decoupage_deplacement

if False: #si sur un ordi sous ubuntu
	chemin_projet = "/home/isn/projet/"
else:
	chemin_projet = ""
	
class Tank():
	def __init__(self, game_display, map, position_initiale, name="Player 1"):
		self.name = name
		self.game_display = game_display
		self.fenetre = pygame.display.get_surface().get_size()
		self.map = map
		#print("Dimension de la map pour robot:", pygame.display.get_surface().get_size())
		#Parametres du robot
		self.position = list(position_initiale)
		self.vitesse_max = 11 # pixel/image -> depend des fps donc des performances des pc qui sont inégales !
		self.constante_acceleration = 1 #pixel/images^2 pour atteindre la vitesse max en 2 secondes
		self.constante_freinage = 0.5
		
		self.vie = 100
		self.alive = True
		self.dernier_tir = 0 #temps du dernier tir
		self.temps_rechargement = 0.1 # seconde(s)
		self.angle_canon = 0 #en debut de partie
		self.angle_rotation_chassis = 0.1 # rad/img pour la rotation de la tourelle
		self.angle_chassis = 0
		
		self.angle_deplacement = 0
		self.longueur = 80 #longueur du canon
		self.duree_animation_touche = 0
		self.acceleration = [0, 0] #en x puis en y
		self.angle_acceleration = 0
		self.vitesse = 0 
		self.type_projectile = Projectile #bientot SnipProj ...
		self.projectiles = [] #liste des projectiles
		#images
		self.img_chassis = pygame.image.load(chemin_projet+"ressources/chassis.png")
		self.rayon = int(pygame.Surface.get_size(self.img_chassis)[0]/2)
		#chargement des images
		self.img_canon3 = pygame.image.load(chemin_projet+"ressources/canon tourelle.png").convert_alpha()
		self.img_chassis_touche = pygame.image.load(chemin_projet+"ressources/chassis3_touche.png").convert_alpha()
		self.img_chassis_mort = pygame.image.load(chemin_projet+"ressources/chassis3_mort.png").convert_alpha()
		self.fumee = pygame.image.load(chemin_projet+"ressources/fumee_tir.png").convert_alpha()
		self.fumee = pygame.transform.scale(self.fumee, (50, 50))
		pygame.font.init()
		#initialisation et chargement des bruitages
		pygame.mixer.pre_init(44100, -16, 1, 512) # a cause du delais
		pygame.mixer.init()
		self.sons = []
		self.sons.append(pygame.mixer.Sound(file=chemin_projet+'sounds/shot1.wav'))
		self.sons.append(pygame.mixer.Sound(file=chemin_projet+'sounds/shot2.wav'))
		self.sons.append(pygame.mixer.Sound(file=chemin_projet+'sounds/shot3.wav'))
		for sound in self.sons:
			sound.set_volume(0.1)
		self.son_touched = pygame.mixer.Sound(file=chemin_projet+'sounds/touched.wav')
		self.son_touched.set_volume(0.1)
		self.son_vie = pygame.mixer.Sound(file=chemin_projet+'sounds/vie.wav')
		self.son_vie.set_volume(0.1)
		#objet pour creer de la fumee lors du tir
		self.fumee = Fumee(self.game_display)
	
	def configurer_touches_deplacement(self, up, down, left, right):
		"choisir les touches pour faire deplacer le robot, ex:K_UP, K_Down...etc"
		self.deplacement = {up:0, down:0, left:0, right:0}
		self.touches = (up, down, left, right)

	def afficher(self, visible, camera_position, hitbox=False):
		"Couteux en ressources"
		self.fumee.afficher(camera_position)
		if visible:
			self.afficher_nom(camera_position)
			self.afficher_vie(camera_position)
			self.afficher_chassis(camera_position)
			self.afficher_canon(camera_position)
		self.afficher_projectiles(camera_position)
		if hitbox:
			self.afficher_aabb_hitbox(camera_position)
	
	def afficher_nom(self, camera_position):
		x1, y1 = self.position
		x0, y0 = camera_position
		x, y = x1-x0, y1-y0
		font = pygame.font.SysFont("Arial Black", 15)
		label = font.render(self.name, 1, (255,255,255))
		largeur, hauteur = font.size(self.name)
		self.game_display.blit(label, (x-largeur/2, y-self.rayon-30-hauteur))
	
	def afficher_vie(self, camera_position):
		x1, y1 = self.position
		x0, y0 = camera_position
		x, y = x1-x0, y1-y0
		largeur = 50 # pixels
		pygame.draw.rect(self.game_display, (0, 100, 0), (x-int(largeur/2), y-self.rayon-30, largeur, 10))
		if self.alive:
			pygame.draw.rect(self.game_display, (0, 200, 0), (x-int(largeur/2), y-self.rayon-30+1, int((largeur*self.vie/100)), 10-1))		
		else:
			pass
		
	def afficher_chassis(self, camera_position):
		x1, y1 = self.position
		x0, y0 = camera_position
		x, y = x1-x0, y1-y0
		
		if time() - self.duree_animation_touche < 0.05:
			img = pygame.transform.rotate(self.img_chassis_touche, degrees(self.angle_chassis))
		elif not self.alive:
			img = pygame.transform.rotate(self.img_chassis_mort, degrees(self.angle_chassis))
		else:
			img = pygame.transform.rotate(self.img_chassis, degrees(self.angle_chassis))
			
		w, h = pygame.Surface.get_size(img)
		self.game_display.blit(img, (x-w/2, y-h/2))
	
	def afficher_aabb_hitbox(self, camera_position):
		x1, y1 = self.position
		x0, y0 = camera_position
		x, y = x1-x0, y1-y0
		r = self.rayon
		pygame.draw.rect(self.game_display, (255, 0, 150), (x-r,y-r,r*2,r*2), 2)
		
	def afficher_canon(self, camera_position):
		# print("angle degrees (afficher_canon):", degrees(self.angle_canon)%360)
		largeur = 10
		longueur = self.longueur
		x1, y1 = self.position
		x0, y0 = camera_position
		x, y = x1-x0, y1-y0
		#image avec canon centre - plus simple !!!!!
		w, h = pygame.Surface.get_size(self.img_canon3)
		canon = pygame.transform.rotate(self.img_canon3, 360-degrees(self.angle_canon))
		canon_x, canon_y = pygame.Surface.get_size(canon)
		self.game_display.blit(canon, (x-canon_x/2, y-canon_y/2))
		
		
	def afficher_projectiles(self, camera_position):
		for projectile  in self.projectiles:
			if projectile.move(): # deplacement + etre dans la fenetre
				projectile.afficher(camera_position)
			else: # sinon on le supprime
				self.projectiles.remove(projectile)
		
	def changer_vitesse(self, touche_pygame):
		"deplacement du robot"
		try:
			self.deplacement[touche_pygame] = True
		except:
			print("touche non associée au déplacement du robot")
	
	def arreter(self, touche_pygame):
		"mets les vitesses de deplacement en x et y a 0"
		try:
			self.deplacement[touche_pygame] = False
		except:
			print("touche non associée au déplacement du robot")
	
	def move(self):
		"fonction qui gere le deplacement du robot (avec prise en compte des collisions)"
		
		#si touche left/right on toune la tourelle
		angle = self.angle_rotation_chassis*(self.deplacement[self.touches[2]] - self.deplacement[self.touches[3]])
		#si vitesse négative (aller en arrière) alors droite et gauche sont inversées
		if self.vitesse < 0:
			angle *= -1
		self.angle_chassis += angle
		
		if self.alive == True:
			# print("\nposition avant deplacement : ", self.position)
			x0, y0 = self.position
			x, y = self.position
			#determination des accelerations en x et y
			self.acceleration = self.deplacement[self.touches[0]] - self.deplacement[self.touches[1]]
			
			#on affecte la vitesse en fonction de l'acceleration
			#si le joueur n'appuie pas sur les touches on ralenti sa vitesse comme si acceleration negative
			if self.acceleration == 0:
				if abs(self.vitesse) <= self.constante_acceleration: #prochaine réduction mène à 0 -> on mets à 0
					v = 0
				else: #Pas d'acceleration -> réduction de la vitesse (les frottements imaginaires)
					if self.vitesse > 0:
						v = self.vitesse - self.constante_freinage
					else:
						v = self.vitesse + self.constante_freinage
			else:
				v = self.vitesse + self.acceleration*self.constante_acceleration*abs(cos(self.angle_acceleration))
			
			#acceleration jusqu'à vitesse maximale
			if v < -self.vitesse_max/2: #en arrière v_max/2
				v = -self.vitesse_max/2
			elif v > self.vitesse_max:
				v = self.vitesse_max
			
			self.vitesse = v
			message = "vitesse : ({:7.5n}".format(float(self.vitesse))
			# print("acceleration :", self.acceleration, "  vitesse :", self.vitesse)	
			
			if self.vitesse != 0 : #déplacement
				
				deplacement_relatif_x = int(self.vitesse*cos(self.angle_chassis))
				deplacement_relatif_y = -int(self.vitesse*sin(self.angle_chassis))
				if deplacement_relatif_x != 0 or deplacement_relatif_y != 0:
					# print("deplacements :", deplacement_relatif_x, deplacement_relatif_y)
					message += " deplacements ({}, {})".format(deplacement_relatif_x, deplacement_relatif_y)
					
					
					#test de collision dans le mur (obstacle)
					#faire du substeps !
					deplacement_accorde = True
					collision = False
		
					points = decoupage_deplacement(self.position, (x+deplacement_relatif_x, y+deplacement_relatif_y), self.vitesse_max) #interressant ou faire par pixel pres ?
					# print(points)
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
					if deplacement_relatif_x and not deplacement_accorde:
						collision = False
						points = decoupage_deplacement(self.position, (x+deplacement_relatif_x, y), self.vitesse_max)
						# print(points)
						for i, point in enumerate(points):
							if not collision and not self.deplacement_possible(point):
								if i != 0:
									self.position = points[i-1]
								collision = True
								break
						if i+1 == self.vitesse_max:
							#pas de collision : deplacement accepte
							self.position = (x+deplacement_relatif_x, y)
						if collision:#en x
							self.vitesse = 0
					# puis en y
					if deplacement_relatif_y and not deplacement_accorde:
						collision = False
						points = decoupage_deplacement(self.position, (x, y+deplacement_relatif_y), self.vitesse_max)
						# print(points)
						for i, point in enumerate(points):
							if not collision and not self.deplacement_possible(point):
								if i != 0:
									self.position = points[i-1]
								collision = True
								break
						if i+1 == self.vitesse_max:
							#pas de collision : deplacement accepte
							self.position = (x, y+deplacement_relatif_y)
						if collision:#en y
							self.vitesse = 0
					#aucune collision :
					if not collision and deplacement_accorde:
						# print("aucune collision")
						if self.deplacement_possible((x+deplacement_relatif_x, y+deplacement_relatif_y)): #necessaire ?
							self.position = (x+deplacement_relatif_x, y+deplacement_relatif_y)
					# else:
						# self.vitesse = [0, 0] #les 2 axes ?
						# print("collision vitesse -> 0")
					message +=  " " + str(self.position)
					# print(message)
					
	def deplacement_possible(self, position_voulu):
		"test si il n'y a pas collision avec la nouvelle position"
		x_voulu, y_voulu = position_voulu
		###la camera change la dimension de la fenetre, ce sont désormais les murs qui bloquent les joueurs aux contours de la map
		# if x_voulu - self.rayon <= 0 or x_voulu + self.rayon > self.fenetre[0]:
			# return False
		# elif y_voulu - self.rayon <= 0 or y_voulu + self.rayon > self.fenetre[1]:
			# return False
		#dans fenetre -> test de collision avec la map
		for rectangle in self.map:
			x1, y1, x2, y2 = rectangle
			aabb = (x1, y1, x2-x1, y2-y1)
			if Cercle_AABB((x_voulu, y_voulu), self.rayon, aabb):
				return False
		return True
				
	def orienter_canon(self, cible):
		if self.alive:
			self.angle_canon = angle(self.position, cible)
			 
	def tir(self):
		if self.alive:
			if time() - self.dernier_tir > self.temps_rechargement:
				#print("temps depuis le dernier tir :{:.3}".format(time()-self.dernier_tir))
				x, y = self.position
				x_canon = int(self.longueur*cos(self.angle_canon))
				y_canon = int(self.longueur*sin(self.angle_canon))
				self.projectiles.append(self.type_projectile(self.game_display, (x+x_canon, y+y_canon), self.angle_canon))
				#son
				pygame.mixer.Sound.play(self.sons[randrange(len(self.sons))])
				self.dernier_tir = time()
				#img fumee pour le tir
				self.fumee.nouvelle_fumee((x+x_canon, y+y_canon), self.angle_canon)
		
	def get_projectiles(self):
		return self.projectiles
	
	def toucher(self):
		"le robot est touche par un projectile"
		if self.alive == True:
			self.duree_animation_touche = time()
			if self.vie > 0:
				self.vie -= 5
			if self.vie <= 0:
				self.mort()
			pygame.mixer.Sound.play(self.son_touched)
	
	def mort(self):
		self.alive = False
	
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
