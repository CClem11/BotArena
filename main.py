# -*- coding:utf8 -*-
import pygame
pygame.init()
from projectile import Explosion
from robot import *
from random import randrange
import socket, sys
from reception_client import *
from charger_map import *
from math_jeu import *
from collision import Point_AABB
from time import time
HOST, PORT = "", 35
mode = input("Choisir le mode (Tapez quelque chose -> Serveur; Entrée -> Client):")

background = ["bg2.jpg", "bg4.jpg", "bg5.jpg"]
#background = background[int(input("Quel image de background ? (entre 0 et {}):".format(len(background)-1)))]
background = background[randrange(len(background))]



class Joueur():	
	def __init__(self, mode=""):
		self.mode = mode
		if not "test" in mode:
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
					HOST = input("Adresse IP de l'hote :")
					print("Mode Client")
					self.mysocket.connect((HOST, PORT))
					self.connexion_adversaire = self.mysocket
					print("Connecte !")
			except Exception as e:
				print(e)
				sys.exit()
		
		self.fps = 60
		self.fenetre = (1600, 900)
				#Pygame initialisation
		self.clock = pygame.time.Clock()
		if "fenetre" in mode:
			self.fenetre = (1000, 550)
			self.game_display = pygame.display.set_mode(self.fenetre)
		else:
			self.game_display = pygame.display.set_mode(self.fenetre, pygame.FULLSCREEN)
		
		pygame.display.set_caption("Bot/Tank Arena") # title
		
		#Creation de la Map
		nombre_bloc = 32
		self.taille_mur = int(self.fenetre[0]/nombre_bloc) #pixels
		self.map = Map(self.game_display, self.fenetre, self.taille_mur)
		self.map_pixel = self.map.get_map()
		position_initiale1 = self.taille_mur, self.taille_mur
		position_initiale2 = self.fenetre[0]-self.taille_mur, self.fenetre[1]-self.taille_mur
		self.robot_joueur = Robot(self.game_display, self.map_pixel, position_initiale1, "Moi")
		self.tir = False
		self.robot_adversaire = Robot(self.game_display, self.map_pixel, position_initiale2, "Robbie")
		if "test" not in mode:
			ActualiserRobot(self.connexion_adversaire, self.robot_adversaire) # va mettre a jour la position de l'adversaire et autre parametres
		
		#lancement de la boucle principale
		self.main()
	
	def collision(self):
		"test si des objects sont en collision"
		#test entre projectile et robot
		liste_robot = [self.robot_joueur, self.robot_adversaire]
		for robot in liste_robot:
			projectiles = robot.get_projectiles()
			for projectile in projectiles:
				x_p, y_p = projectile.position
				for robot_cible in liste_robot:
					x, y = robot_cible.position
					if (x_p - x)**2 + (y_p - y)**2 < robot_cible.rayon**2: #distance du projectile au robot < rayon du robot ?
						robot_cible.toucher()
						self.explosion.nouvelle_explosion(projectile.position)
						projectiles.remove(projectile)
		#test entre projectile et obstacles
		self.collision_map()
	
	def collision_map(self):
		liste_robot = [self.robot_joueur, self.robot_adversaire]
		for robot in liste_robot:
			projectiles = robot.get_projectiles()
			for projectile in projectiles:
				x_p, y_p = projectile.position
				r_p = projectile.rayon
				for x, y, x1, y1 in self.map.get_map():
					if x < x_p < x1 and y < y_p < y1: #dans l'image mur
						self.explosion.nouvelle_explosion(projectile.position)
						projectiles.remove(projectile)
						
		
	def afficher_robots(self):
		self.robot_joueur.afficher(visible=True)
		self.robot_adversaire.afficher(visible=self.adversaire_visible)
	
	def afficher_map(self):
		self.map.afficher()
	
	def afficher_explosions(self):
		self.explosion.afficher()
	
	def fin(self):
		pygame.quit()
		quit()
		
	def main(self):
		global background
		background = pygame.image.load("ressources/"+background).convert_alpha()
		self.explosion = Explosion(self.game_display)
		position_souris = (0, 0)
		fps = 0
		self.adversaire_visible = True
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.fin()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.fin()
					if event.key == pygame.K_DOWN:
						self.robot_joueur.changer_vitesse('Down')
					elif event.key == pygame.K_UP:
						self.robot_joueur.changer_vitesse('Up')
					elif event.key == pygame.K_LEFT:
						self.robot_joueur.changer_vitesse('Left')
					elif event.key == pygame.K_RIGHT:
						self.robot_joueur.changer_vitesse('Right')
					elif event.key == pygame.K_SPACE:
						self.robot_joueur.tir()
						self.tir = True
					elif event.key == pygame.K_r:
						self.robot_joueur.ressuciter()
						self.robot_adversaire.ressuciter()
						
					
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.robot_joueur.tir()
					self.tir = True
					
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_DOWN:
						self.robot_joueur.arreter('Down')
					elif event.key == pygame.K_UP:
						self.robot_joueur.arreter('Up')
					elif event.key == pygame.K_LEFT:
						self.robot_joueur.arreter('Left')
					elif event.key == pygame.K_RIGHT:
						self.robot_joueur.arreter('Right')
				if event.type == pygame.MOUSEMOTION:
					position_souris = event.pos
			
			if not "test" in mode:
				self.envoyer_informations_serveur()
			self.robot_joueur.orienter_canon(position_souris)		
			
			#self.game_display.fill((0, 0, 0))
			self.game_display.blit(background, (0, 0))
			
			self.robot_joueur.move()
			self.collision()
			if fps%10 == 0:
				self.spot()
			self.afficher_map()
			self.afficher_robots()
			self.afficher_explosions()
			pygame.display.update()
			# pygame.display.flip()
			self.clock.tick(self.fps)
			fps += 1
			if fps > self.fps-1:
				fps = 0
			
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
		self.connexion_adversaire.send(message.encode('Utf8'))
	
	def spot(self):
		"detect si adversaire visible ou non"
		# print("test spot")
		x1, y1 = self.robot_joueur.position
		x2, y2 = self.robot_adversaire.position
		ligne = decoupage_deplacement((x1, y1), (x2, y2), int(distance(x1, y1, x2, y2)/30))
		for point in ligne:
			for rectangle in self.map_pixel:
				x1, y1, x2, y2 = rectangle
				if Point_AABB(point, (x1, y1, x2-x1, y2-y1)):
					self.adversaire_visible = False
					return False
		self.adversaire_visible = True
		return True
		
if __name__ == '__main__':
	Joueur(mode)
