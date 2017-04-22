#communication
import socket, sys
from threading import Thread
from time import sleep
HOST = '192.168.1.13'
PORT = 23
		

class Serveur():
	def __init__(self):
		#Thread.__init__(self)
		self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.mysocket.bind((HOST, PORT))
			self.initialiser()
		except socket.error as e:
			print("Erreur")
			sys.exit()
   
	def initialiser(self):
		print("Attente de connexion...")
		self.mysocket.listen(1)
		self.connexion, adresse = self.mysocket.accept()
		print("Connexion de {} sur le port {}".format(adresse[0], adresse[1]))
		self.envoyer("Serveur OK")
		self.reception = Reception(HOST, PORT, self.connexion)
	
	def envoyer(self, message):
		msg = "S "+message #S pour serveur
		self.connexion.send(msg.encode("utf8"))
		
class Client():
	def __init__(self):
		self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.mysocket.connect((HOST, PORT))
		except:
			print("Erreur dans Client (de connexion a serveur)")
			sys.exit()
		self.reception = Reception(HOST, PORT, self.mysocket)


class Reception(Thread):
	def __init__(self, HOST, PORT, connexion):
		Thread.__init__(self)
		self.connexion = connexion
		self.start()
  
	def run(self):
		print("Lancement de l'ecoute : \n")
		while True:
			msg = self.connexion.recv(1024).decode("utf8")
			print(msg)
			sleep(0.1)
		    