# -*- coding:utf8 -*-

from threading import Thread
from time import time, sleep
import socket

class ActualiserRobot(Thread):
	def __init__(self, connexion, robot):
		Thread.__init__(self)
		self.robot = robot
		self.connexion = connexion
		self.start()
	
	def traiter_donnees_serveur(self, donnees):
		# if donnees != "":
			# print("reception de donnees! :", donnees)
		#print(self.getName(), ":", donnees)
		try:
			consigne = donnees.split('/')
			type_consigne = consigne[0]
			if type_consigne == "actualiser_informations":
				infos = consigne[1].split('*')
				#print("parametres :", infos)
				for info in infos:
					key, value = info.split(':')
					if key == "position":
						pos = [int(valeur) for valeur in value[1:-1].split(',')]
						self.robot.position = pos
					elif key == "angle":
						self.robot.angle_canon = float(value)
					elif key == 'vie':
						self.robot.vie = int(value)
					elif key == 'tir' and value == "True":
						self.robot.tir()
		except:
			self.close()
	
	def run(self):
		while True:
			msg = self.connexion.recv(1024).decode('utf8')
			self.traiter_donnees_serveur(msg)