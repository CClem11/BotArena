#Serveur
import socket, sys
from threading import Thread

HOST, PORT = '37.187.127.237', 100

class Serveur():
	id_joueur = 1
	"Serveur de connexion pour les joueurs"
	def __init__(self, HOST, PORT):
		self.joueurs = {} # dictionnaire pour joueur : cle=id_joueur, connexion, robot, pos, angle, fire
		self.port, self.host = HOST, PORT
		self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		port_trouve = False
		while not port_trouve:
			try:
				self.serveur.bind((HOST, PORT))
				port_trouve = True
			except:
				print("Parametres ({}, {}) non valide !".format(HOST, PORT))
				PORT += 1
		
		print("Attente de connexion...sur ({}, {})".format(HOST, PORT))
		nombre_joueur = 2
		self.serveur.listen(nombre_joueur) #2 joueurs
		while len(self.joueurs) < nombre_joueur:
			connexion, adresse = self.serveur.accept()
			print("Connexion de {} sur le port {}".format(adresse[0], adresse[1]))
			self.joueurs[str(Serveur.id_joueur)] = [connexion]
			self.initialisation_connexion(connexion)
		print("Les {} joueurs sont connectes".format(nombre_joueur))
		
		# while False:
			# for value in self.joueurs.values():
				# connexion = value[0]
				# print(connexion.recv(1024).decode('utf8'))
	
	def initialisation_connexion(self, connexion):
		"envoie les informations d'initialisation pour un joueur"
		id_joueur = Serveur.id_joueur
		Serveur.id_joueur += 1
		ServeurEcoute(self, connexion, id_joueur)
		parametres = {}
		parametres['fps']= 60
		parametres['fenetre'] = (500, 500)
		parametres['id_robot'] = id_joueur
		message = self.formater_message("initialisation", parametres)
		self.envoyer(connexion, message)
		#avertir les autres joueurs qu'il y a un nouveau robot
		# self.relayer_informations(id_joueur, "ajouter_robot/id_robot:"+str(id_joueur)+"-pos:(200, 200)")
		
	
	def envoyer(self, connexion, message):
		# print("Envoi de donnees vers adversaire")
		try:
			connexion.send(message.encode("utf8"))
		except socket.error as e:
			print(e)
			self.arreter()

	def formater_message(self, type_consigne, parametres):
		message = type_consigne +"/"
		for parametre, valeur in parametres.items():
			message += str(parametre) + ':' + str(valeur) + '-'
		message = message[:-1] # enleve le dernier '-' (separateur de parametre)
		return message
	
	def relayer_informations(self, id_expediteur, donnees):
		"numero du thread puis msg en format str"
		consigne = donnees.split('/')
		type_consigne = consigne[0]
		if True:#type_consigne == "actualiser_informations":
			for id_joueur, attribut in self.joueurs.items():
				if id_joueur != str(id_expediteur):
					connexion_destinataire = attribut[0]
					#print(connexion_destinataire)
					self.envoyer(connexion_destinataire, donnees)
	
	def arreter(self):
		"Pour fermer correctement la co du serveur"
		self.serveur.close()


####################	Pour chaque joueur - ecoute client	###########
class ServeurEcoute(Thread):
	def __init__(self, serveur, connexion, id_joueur):
		Thread.__init__(self)
		self.serveur, self.connexion, self.id_joueur = serveur, connexion, id_joueur
		self.start()
	
	def run(self):
		#print("Ecoute de {} par {}".format("joueur", self.getName()))
		while True:
			try:
				msg = self.connexion.recv(1024).decode('utf8')
			except Exception as e: #plus de co ?
				print(e)
				self.stop()
			
			if msg != "":
				# print("id :", self.id_joueur, "->", msg)
				self.serveur.relayer_informations(self.id_joueur, msg)
				if msg == "stop":
					#Un des joueurs a ferme le jeu
					#fermeture des threads et des connexion
					self.serveur.arreter()
					self.arreter()
					
	
	def arreter(self):
		print("Fermeture de connexion et arret de ", self.getName())
		self.connexion.close()
		self.join()
	

if __name__ == '__main__':
	Serveur(HOST, PORT)