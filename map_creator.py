# -*- coding:utf8 -*-

#Map creator en mieux

import pygame
pygame.init()

class App():
	def __init__(self, nombre_colonne, nombre_ligne):
		self.colonne, self.ligne = nombre_colonne, nombre_ligne
		self.fenetre = (1600, 900)
		if self.fenetre != (1600, 900):
			self.game_display = pygame.display.set_mode(self.fenetre)
		else:
			self.game_display = pygame.display.set_mode(self.fenetre, pygame.FULLSCREEN)
			
		self.taille_bloc = int(min(self.fenetre[0]/(nombre_colonne+3), self.fenetre[1]/(nombre_ligne+3)))
		self.map = {(x, y):1 for x in range(nombre_colonne) for y in range(nombre_ligne)}
		# print(self.map)
		self.clock = pygame.time.Clock()
		
				
		#chargement des images
		liste_image = ["ressources/mur.png", "ressources/grass.png"]
		self.blocs = []
		for img in liste_image:
			self.blocs.append(pygame.transform.scale(pygame.image.load(img).convert(), (self.taille_bloc,self.taille_bloc)))
		
		self.selection = -1
		
		#lancement de la boucle principale
		self.main()
	
	def fin(self):
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
						print(x, y)
	
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
	
	def main(self):
		down = False
		while True:
			self.game_display.fill((0, 0, 0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.fin()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.fin()
					print(event)
				if event.type == pygame.MOUSEBUTTONDOWN:
					down = True
					self.souris(event.pos)
				if event.type == pygame.MOUSEBUTTONUP:
					down = False
				if event.type == pygame.MOUSEMOTION:
					if down:
						self.souris(event.pos)
			if self.selection != -1:
				x, y = pygame.mouse.get_pos()[0] - int(self.taille_bloc/2), pygame.mouse.get_pos()[1] - int(self.taille_bloc/2)
				self.game_display.blit(self.blocs[self.selection], (x, y))
					
						
			self.dessiner_choix_bloc()
			self.dessiner_selection()
			self.afficher_map()
			pygame.display.flip()
			self.clock.tick(60)

		
if __name__ == "__main__":
	# try:
		# colonne = int(input("Nombre de bloc en x : "))
		# ligne = int(input("Nombre de bloc en y : "))
	# except:
		# print("Erreur type int ?")
		# quit()
	colonne, ligne = 16*3, 9*3
	App(colonne, ligne)