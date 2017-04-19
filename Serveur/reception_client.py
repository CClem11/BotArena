
from threading import Thread
from time import time, sleep
import socket

class ReceptionClient(Thread):
	def __init__(self, joueur):
		Thread.__init__(self)
		self.joueur = joueur
		self.start()
	
	def traiter_donnees_serveur(self, donnees):
		print(self.getName(), ":", donnees)
		consigne = donnees.split('/')
		print(consigne)
		type_consigne = consigne[0]
		if type_consigne == "initialisation":
			print(consigne[1])
			self.joueur.initialisation(consigne[1])
		elif type_consigne == "ajouter_robot":
			infos = consigne[1].split('-')
			for info in infos:
				key, value = info.split(':')
				if key == "pos":
					pos = [int(valeur) for valeur in value[1:-1].split(',')]
				if key == "id_robot":
					id_robot = int(value)
			self.joueur.robots.append(Robot, self.joueur.game_display, pos, id_robot, "Robbie")
			
		elif type_consigne == "actualiser_informations":
			infos = consigne[1].split('-')
			for info in infos:
				key, value = info.split(':')
				if key == "id_robot":
					id_robot = int(value)
					robot = [robot for robot in self.joueur.robots if robot.id_joueur == id_robot][0]
				elif key == "pos":
					pos = [int(valeur) for valeur in value[1:-1].split(',')]
				elif key == "angle":
					angle = int(value)
			robot.position = pos 
			robot.angle_canon = angle
	
	def run(self):
		#initialisation
		msg = self.joueur.mysocket.recv(1024).decode('utf8')
		self.traiter_donnees_serveur(msg)
		while True:
			print("socket joueur :", self.joueur.mysocket)
			#msg = self.joueur.mysocket.recv(1024).decode('utf8')
			#self.traiter_donnees_serveur(msg)
			sleep(1)
	
	
	