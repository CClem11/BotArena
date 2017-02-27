# -*- coding:Utf-8 -*-
from robot import *
from random import randrange
import socket, sys
from reception_client import *
from charger_map import *

HOST, PORT = '192.168.1.11', 35
HOST = input("Adresse IP de l'hote :")
mode = input("Choisir le mode (Tapez quelque chose -> Serveur; Entree -> Client):")
background = ["bg.jpg", "bg2.jpg", "bg3.jpg", "bg4.jpg", "bg5.jpg"]
background = background[int(input("Quel image de background ? (entre 0 et {}):".format(len(background)-1)))]

class Joueur():
	def __init__(self, mode=""):
		self.mode = mode
		if mode != "test":
			self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				if len(mode) > 0:
					print("Mode Serveur")
					self.mysocket.bind((HOST, PORT))
					self.mysocket.listen(1)
					print("Attente de connexion...")
					self.connexion_adversaire, adresse = self.mysocket.accept()
				else:
					print("Mode Client")
					self.mysocket.connect((HOST, PORT))
					self.connexion_adversaire = self.mysocket
					print("Connecte !")
			except Exception as e:
				print(e)
				sys.exit()

		self.fps = 70
		self.fenetre = (700, 800)
		
		self.clock = pygame.time.Clock()
		#self.game_display = pygame.display.set_mode(self.fenetre)
		self.game_display = pygame.display.set_mode((1600, 900), pygame.FULLSCREEN)
		pygame.display.set_caption("Arene") # title
		
		self.robot_joueur = Robot(self.game_display, (150, 150), "Moi")
		self.tir = False
		self.robot_adversaire = Robot(self.game_display, (1450, 750), "Robbie")
		if mode != "test":
			ActualiserRobot(self.connexion_adversaire, self.robot_adversaire) # va mettre a jour la position de l'adversaire et autre parametres
		#chargement de la map
		self.map = ouvrir_map(map2)
		self.img_obstacle = pygame.image.load("ressources/mur.png").convert_alpha()
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
						projectiles.remove(projectile)
		#test entre projectile et obstacles
		for robot in liste_robot:
			projectiles = robot.get_projectiles()
			for projectile in projectiles:
				x_p, y_p = projectile.position
				r_p = projectile.rayon
				for x, y in self.map.keys():
					cote = 100 # pixel de l'image mur
					x, y = x*100, y*100
					if x < x_p < x + cote and y < y_p < y + cote: #dans l'image mur
						projectiles.remove(projectile)
		
	def afficher_robots(self):
		self.robot_joueur.afficher()
		self.robot_adversaire.afficher()
	
	def afficher_map(self):
		for position in self.map.keys():
			x, y = position
			x *= 100
			y *= 100
			self.game_display.blit(self.img_obstacle, (x, y))
	
	def fin(self):
		pygame.quit()
		quit()
		
	def main(self):
		global background
		background = pygame.image.load("ressources/"+background).convert_alpha()

		position_souris = (0, 0)
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.fin()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.fin()
					if event.key == pygame.K_DOWN:
						self.robot_joueur.changer_vitesse('S')
					elif event.key == pygame.K_UP:
						self.robot_joueur.changer_vitesse('N')
					elif event.key == pygame.K_LEFT:
						self.robot_joueur.changer_vitesse('W')
					elif event.key == pygame.K_RIGHT:
						self.robot_joueur.changer_vitesse('E')
					elif event.key == pygame.K_SPACE:
						self.robot_joueur.tir()
						self.tir = True
					elif event.key == pygame.K_r:
						self.robot_adversaire.ressuciter()
					
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.robot_joueur.tir()
					self.tir = True
					
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_DOWN:
						self.robot_joueur.arreter('S')
					elif event.key == pygame.K_UP:
						self.robot_joueur.arreter('N')
					elif event.key == pygame.K_LEFT:
						self.robot_joueur.arreter('W')
					elif event.key == pygame.K_RIGHT:
						self.robot_joueur.arreter('E')
				if event.type == pygame.MOUSEMOTION:
					position_souris = event.pos
			
			if self.mode != "test":
				self.envoyer_informations_serveur()
			self.robot_joueur.orienter_canon(position_souris)		
			self.robot_joueur.move()
			self.collision()
			#self.game_display.fill((0, 0, 0))
			self.game_display.blit(background, (0, 0))
			self.afficher_map()
			self.afficher_robots()
			pygame.display.update()
			self.clock.tick(self.fps)
	
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
		
if __name__ == '__main__':
	Joueur(mode)
