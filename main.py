from __future__ import print_function
# -*- coding:utf8 -*-
from builtins import input
print("lol")
import pygame
pygame.init()
from projectile import Explosion
from robot import *
from random import randrange
import socket, sys
from reception_client import *
from map import *
from math_jeu import *
from collision import Point_AABB
from time import time
from camera import Camera
from math import degrees
HOST, PORT = "37.187.127.237", 100
mode = input("Choisir le mode (Tapez quelque chose -> Serveur; Entrée -> Client):")

if False: #si sur un ordi sous ubuntu
	chemin_projet = "/home/isn/projet/"
else:
	chemin_projet = ""

background = ["bg2.jpg", "bg4.jpg", "bg5.jpg"]
#background = background[int(input("Quel image de background ? (entre 0 et {}):".format(len(background)-1)))]
# background = chemin_projet + background[randrange(len(background))]

class Joueur():	
	def __init__(self, mode=""):
		self.mode = mode
		if not "test" in mode:
			global HOST, PORT
			self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				if len(mode) > 0:
					print("Mode Serveur")
					HOST = socket.gethostbyname(socket.gethostname())
					self.mysocket.bind((HOST, PORT))
					self.mysocket.listen(1)
					print("Ip du serveur :", HOST)
					print("Attente de connexion...")
					self.connexion_adversaire, adresse = self.mysocket.accept()
				else:
					# HOST = input("Adresse IP de l'hote :")
					PORT = int(input("port :"))
					print("Mode Client")
					# print("parametres : ({}, {})".format(HOST, PORT))
					self.mysocket.connect((HOST, PORT))
					self.connexion_adversaire = self.mysocket
					print("Connecte ! (port : {})".format(PORT))
			except Exception as e:
				# print(e)
				print("Erreur lors de la connexion (problème de port ?)")
				sys.exit()
		
		self.fps = 40
		#projecteur lycee
		# self.fenetre = (1440, 900)
		self.fenetre = (1600, 900)
				# Pygame initialisation
		self.clock = pygame.time.Clock()
		if "fenetre" in mode:
			self.fenetre = (800, 450)
			self.game_display = pygame.display.set_mode(self.fenetre)
		else:
			self.game_display = pygame.display.set_mode(self.fenetre, pygame.FULLSCREEN)
		
		pygame.display.set_caption("Bot/Tank Arena") # title
		
		#Creation de la Map
		self.nombre_bloc = 25 #visible à l'écran en longueur
		self.taille_mur = int(self.fenetre[0]/self.nombre_bloc) #pixels
		# print("taille du mur:", self.taille_mur)
		self.camera = Camera(self.nombre_bloc*self.taille_mur, int(self.nombre_bloc*self.taille_mur*9/16)) # taille de l'ecran de "vision" en x puis y
		self.map = Map(self.game_display, self.fenetre, self.taille_mur)
		self.map_pixel = self.map.get_map_obstacle()
		position_initiale1 = self.taille_mur*2, self.taille_mur*2
		# position_initiale2 = self.fenetre[0]-self.taille_mur, self.fenetre[1]-self.taille_mur
		position_initiale2 = int(self.fenetre[0]/2), int(self.fenetre[1]/2)
		self.robot_joueur = Tank(self.game_display, self.map_pixel, position_initiale1, "Moi")
		self.robot_joueur.configurer_touches_deplacement(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
		self.tir = False 
		self.robot_adversaire = Tank(self.game_display, self.map_pixel, position_initiale2, "Robbie")
		self.robot_adversaire.configurer_touches_deplacement(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
		if "test" not in mode:
			ActualiserRobot(self.connexion_adversaire, self.robot_adversaire) # va mettre a jour la position de l'adversaire et autre parametres
		
		#chargement de l'image fleche pour indiquer direction de l'adversaire
		fleche = pygame.image.load("ressources/arrow.png").convert_alpha()
		fleche = pygame.transform.scale(fleche, (150, 150))
		fleche = pygame.transform.rotate(fleche, 90)
		fleche.set_alpha(50)
		self.image_fleche = fleche
		
		#lancement de la boucle principale
		# self.liste_robots = [self.robot_joueur]
		self.liste_robots = [self.robot_joueur, self.robot_adversaire]
		
		self.main()
	
	def collision(self):
		self.collision_projectiles() #robot et projectile
		self.collision_map() # projectiles et map
	
	def collision_projectiles(self):
		"test si des robots sont en collision avec des projectiles"
		#test entre projectile et robot
		for robot in self.liste_robots:
			projectiles = robot.get_projectiles()
			for projectile in projectiles:
				x_p, y_p = projectile.position
				for robot_cible in self.liste_robots:
					x, y = robot_cible.position
					# if (x_p - x)**2 + (y_p - y)**2 < robot_cible.rayon**2: #distance du projectile au robot < rayon du robot ?
					if Cercle_Cercle(x, y, robot_cible.rayon, x_p, y_p, projectile.rayon):
						robot_cible.toucher()
						self.explosion.nouvelle_explosion(projectile.position)
						projectiles.remove(projectile)
		
	def collision_map(self):
		for robot in self.liste_robots:
			projectiles = robot.get_projectiles()
			for projectile in projectiles:
				x_p, y_p = projectile.position
				r_p = projectile.rayon
				for x, y, x1, y1 in self.map.get_map_obstacle():
					if x < x_p < x1 and y < y_p < y1: #dans l'image mur
						self.explosion.nouvelle_explosion(projectile.position)
						projectiles.remove(projectile)
						
		
	def afficher_robots(self):
		# for robot in self.liste_robots:
			# robot.afficher(True, self.camera.get_position(), self.show_hitbox)
		self.robot_joueur.afficher(True, self.camera.get_position(), self.show_hitbox)
		self.robot_adversaire.afficher(self.adversaire_visible, self.camera.get_position(), self.show_hitbox)
			
	def afficher_map(self):
		self.map.afficher(self.camera.get_position())
	
	def afficher_explosions(self):
		self.explosion.afficher(self.camera.get_position())
	
	def afficher_fleche(self):
		teta = -1*degrees(angle(self.robot_joueur.position, self.robot_adversaire.position))
		img = pygame.transform.rotate(self.image_fleche, teta)
		w, h = pygame.Surface.get_size(img)
		self.game_display.blit(img, (self.fenetre[0]-100-int(w/2), self.fenetre[1]-100-int(h/2)))
	
	def afficher_minimap(self):
		self.map.afficher_minimap((int(self.fenetre[0]/2-304/2), self.fenetre[1]-171))
	
	def fin(self):
		pygame.quit()
		#fermer la connexion
		try:
			self.connexion_adversaire.send("stop".encode("utf8"))
		except:
			pass
		quit()
		
		
	def main(self):
		# global background
		
		# pygame.mouse.set_visible(False)   #  cacher la souris
		cursor = pygame.cursors.compile(pygame.cursors.textmarker_strings)
		pygame.mouse.set_cursor(*pygame.cursors.broken_x)
		
		# background = pygame.image.load("ressources/"+background).convert_alpha()
		self.explosion = Explosion(self.game_display)
		position_souris = (0, 0)
		self.adversaire_visible = True
		self.show_hitbox = False
		while True:
			self.game_display.fill((5, 5, 5))
			# self.game_display.blit(background, (0, 0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.fin()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_i:
						self.robot_joueur.angle_canon += 0.1
					elif event.key == pygame.K_k:
						self.robot_joueur.angle_canon -= 0.1
					elif event.key == pygame.K_h:
						if self.show_hitbox:
							self.show_hitbox = False
						else:
							self.show_hitbox = True
					if event.key == pygame.K_ESCAPE:
						self.fin()
					elif event.key == pygame.K_SPACE:
						self.robot_joueur.tir()
						self.tir = True
					elif event.key == pygame.K_r:
						for r in self.liste_robots:
							r.ressuciter()
					else:
						#deplacement du joueur
						for r in self.liste_robots:
							r.changer_vitesse(event.key)					
					
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.robot_joueur.tir()
					self.tir = True
					
				if event.type == pygame.KEYUP:
					#deplacement robot joueur
					for r in self.liste_robots:
							r.arreter(event.key)
					
			#position de la souris
			x1, y1 = pygame.mouse.get_pos()
			x2, y2 = self.camera.get_position()
			position_souris = x1+x2, y1+y2
			
			if not "test" in mode:
				self.envoyer_informations_serveur()
			self.robot_joueur.orienter_canon(position_souris)	#en absolue	
			
			self.deplacer_robots()
			x, y = self.robot_joueur.position
			self.camera.set_position_centre(x, y) #repositionner la camera
			self.collision()
			# self.spot()
			# print(self.adversaire_visible)
			self.afficher_map()
			# self.afficher_fleche()
			# self.afficher_minimap()
			self.afficher_robots() # attention fps
			self.afficher_explosions()
			self.afficher_fps(100, 30)
			pygame.display.update((0, 0, 1600, 900))
			# pygame.display.update((200, 200, 1200, 500)) # update/flip
			
			self.clock.tick(self.fps)
	
	def deplacer_robots(self):
		for robot in self.liste_robots:
			robot.move()
				
	def afficher_fps(self, x, y):
		fps = int(self.clock.get_fps())
		# print(fps)
		message = "FPS : " + str(fps)
		font = pygame.font.SysFont("Verdana", 20)
		label = font.render(message, 1, (255,255,255))
		largeur, hauteur = font.size(message)
		self.game_display.blit(label, (x-largeur/2, y-hauteur/2))
			
	def get_informations(self):
		"retourne toutes les informations relatives au robot (joueur)"
		infos = self.robot_joueur.get_informations()
		if self.tir:
			self.tir = False
			infos += "*tir:True"
		else:
			infos += "*tir:False"
		return infos
	
	def envoyer_informations_serveur(self):
		message = self.get_informations()
		self.connexion_adversaire.send(message.encode('utf8'))
	
	def spot(self):
		"detecte si adversaire visible ou non"
		# print("test spot")
		p1 = self.robot_joueur.position
		p2 = self.robot_adversaire.position
		map_bloc = self.map.get_map_bloc()
		for point in self.map.get_bloc_ligne(p1, p2): #seulement bloc sur la ligne
			if map_bloc[point]: #test si le point est dans un bloc mur
				self.adversaire_visible = False
				return False
		self.adversaire_visible = True		
		return True
		
if __name__ == '__main__':
	Joueur(mode)
