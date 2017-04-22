# -*- coding:utf8 -*-

#Map creator en mieux

import pygame
pygame.init()
from os import getcwd
from tkinter.filedialog import asksaveasfilename, askopenfilename

class App():
	def __init__(self, nombre_colonne, nombre_ligne):
		self.fenetre = (1600, 900)
		if self.fenetre != (1600, 900):
			self.game_display = pygame.display.set_mode(self.fenetre)
		else:
			self.game_display = pygame.display.set_mode(self.fenetre, pygame.FULLSCREEN)
		self.clock = pygame.time.Clock()
		
		#chargement des images
		self.liste_image = ["ressources/mur.png", "ressources/ground.png", "ressources/grass.png"]
		#initialisation
		self.initialisation(nombre_colonne, nombre_ligne)
		self.nouvelle_map(1)
		self.ajouter_bordures(0)
		
		self.selection = -1
		#ajout de bordures
		self.ajouter_bordures(0)
		#lancement de la boucle principale
		self.main()
	
	def initialisation(self, nombre_colonne, nombre_ligne):
		self.colonne, self.ligne = nombre_colonne, nombre_ligne
		self.taille_bloc = int(min(self.fenetre[0]/(nombre_colonne+3), self.fenetre[1]/(nombre_ligne+3)))
		self.blocs = []
		#mettre à l'echelle les images en fonction de la taille des blocs
		for img in self.liste_image:
			self.blocs.append(pygame.transform.scale(pygame.image.load(img).convert(), (self.taille_bloc,self.taille_bloc)))
	
	def open(self):
		nom_fichier = askopenfilename(title="Ouvrir une map",filetypes = [("Fichier Texte","*.txt")])
		if nom_fichier != "":
			self.map = {}
			with open(nom_fichier, 'r') as fichier:
				max_x, max_y = 0, 0
				for y, ligne in enumerate(fichier.readlines()):
					# print("\"" + str(ligne) + "\"")
					if y > max_y:
						max_y = y
					for x, bloc in enumerate(ligne):
						if bloc not in "\n":
							if x > max_x:
								max_x = x
							self.map[(x, y)] = int(bloc)
							
			self.initialisation(max_x+1, max_y+1)
	
	def get_bloc(self, position_souris):
		"retourne le bloc sous la souris si il y en a un"
		w = self.taille_bloc
		#test de clique sur une case
		for x in range(self.colonne):
			for y in range(self.ligne):
				if 2*w + y*w <= position_souris[1] <= 2*w + (y+1)*w:
					if 2*w + x*w <= position_souris[0] <= 2*w + (x+1)*w:
						return self.map[(x, y)]
		return None
						
	
	def afficher_texte(self, message, x, y,taille=34,couleur=(255,255,255)):
		font = pygame.font.SysFont("Arial Black", taille)
		texte = font.render(message, 1, couleur)
		largeur, hauteur = font.size(message)
		self.game_display.blit(texte, (x-largeur/2, y-hauteur/2))
	
	def afficher_actions(self):
		message = '"s" : save, "o" : open, "n", nouvelle map, "b" : bordure, "g" : grille'
		self.afficher_texte(message, 1100, 15, 20)
		message = 'clic gauche : poser bloc,	clic droit : selectionner le bloc'
		self.afficher_texte(message, 1100, 40, 18, (200, 200, 200))
	
	def ajouter_bordures(self, num_bloc):
		"ajoute des bordures avec le bloc passé en argument"
		for y in range(self.ligne):
			for x in range(self.colonne):
				if y == 0 or y == self.ligne-1 or x == 0 or x == self.colonne-1:
					self.map[(x, y)] = num_bloc
	
	def nouvelle_map(self, bloc):
		self.map = {(x, y):bloc for x in range(self.colonne) for y in range(self.ligne)}
	
	def save(self):
		nom_fichier = asksaveasfilename(title="Enregistrer sous", initialdir=getcwd(), filetypes = [("Fichier Texte","*.txt")], defaultextension=".txt")
		if nom_fichier != "":
			print("Enregistrement de la map : ", nom_fichier)
			with open(nom_fichier, 'w') as fichier:
				for y in range(self.ligne):
					ligne = "".join([str(self.map[(x, y)]) for x in range(self.colonne)])
					fichier.write(ligne)
					fichier.write("\n")
	
	def fin(self):
		# self.save()
		pygame.quit()
		quit()
	
	def souris(self, position):
		w = self.taille_bloc
		#determiner si selection d'un bloc
		if 0 <= position[1] <= w:
			trouve_selection = False
			for i in range(len(self.blocs)):
				if 2*w + i*w < position[0] < 2*w + (i+1)*w:
					self.selection = i
					trouve_selection = True
			if not trouve_selection:
				self.selection = -1
		#test de clique sur une case
		for x in range(self.colonne):
			for y in range(self.ligne):
				if 2*w + y*w <= position[1] <= 2*w + (y+1)*w:
					if 2*w + x*w <= position[0] <= 2*w + (x+1)*w:
						self.map[(x, y)] = self.selection
						# print(x, y)
	
	def dessiner_choix_bloc(self):
		for i, img in enumerate(self.blocs):
			x = 2*self.taille_bloc + i*self.taille_bloc
			self.game_display.blit(img, (x, 0))
	
	def dessiner_selection(self):
		x = 2*self.taille_bloc + self.selection*self.taille_bloc
		pygame.draw.rect(self.game_display, (0, 255, 0), (x, 0, self.taille_bloc, self.taille_bloc), 2)
	
	def afficher_map(self):
		w = self.taille_bloc
		for x in range(self.colonne):
			for y in range(self.ligne):
				x1 = 2*w + x*w
				y1 = 2*w + y*w
				pygame.draw.rect(self.game_display, (150, 150, 150), (x1, y1, w, w), 1)
				img = self.map[(x, y)]
				if img != -1:
					self.game_display.blit(self.blocs[img], (x1, y1))
					
	def afficher_grille(self, afficher=True):
		if afficher:
			w = self.taille_bloc
			for x in range(self.colonne):
				for y in range(self.ligne):
					x1 = 2*w + x*w
					y1 = 2*w + y*w
					pygame.draw.rect(self.game_display, (150, 150, 150), (x1, y1, w, w), 1)
	
	def main(self):
		down = False
		grille = False
		while True:
			self.game_display.fill((0, 0, 0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.fin()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.fin()
					#autres action possible avec le clavier : 
					if event.key == pygame.K_o:	#open
						self.open()
					if event.key == pygame.K_s: #save
						self.save()
					if event.key == pygame.K_b:	#bordure avec le bloc en selection
						self.ajouter_bordures(self.selection)
					if event.key == pygame.K_n:	#remplace tout les bloc par le bloc en selection
						self.nouvelle_map(self.selection)
					if event.key == pygame.K_g:	#affiche la grille
						print(grille)
						if not grille:
							grille = True
						else:
							grille = False
					
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						down = True
						self.souris(event.pos)
					if event.button == 3: #selectionner le bloc sous la souris
						bloc = self.get_bloc(event.pos)
						if bloc != None:
							self.selection = bloc
				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						down = False
				if event.type == pygame.MOUSEMOTION:
					if down:
						self.souris(event.pos)
					
			self.afficher_actions()		
			self.dessiner_choix_bloc()
			self.dessiner_selection()
			self.afficher_map()
			self.afficher_grille(grille)
			if self.selection != -1: #afficher le bloc sous la souris
				x, y = pygame.mouse.get_pos()[0] - int(self.taille_bloc/2), pygame.mouse.get_pos()[1] - int(self.taille_bloc/2)
				self.game_display.blit(self.blocs[self.selection], (x, y))
			pygame.display.flip()
			self.clock.tick(60)

		
if __name__ == "__main__":
	# try:
		# colonne = int(input("Nombre de bloc en x : "))
		# ligne = int(input("Nombre de bloc en y : "))
	# except:
		# print("Erreur type int ?")
		# quit()
	colonne, ligne = int(16*1/2), int(9*1/2)
	App(colonne, ligne)