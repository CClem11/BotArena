from __future__ import print_function
import pygame
from pygame.locals import *
pygame.init()
from time import sleep

def fin():
	pygame.quit()
	quit()
	
def afficher_texte(message, x, y,taille=34,couleur=(255,255,255)):
	font = pygame.font.SysFont("Arial Black", taille)
	texte = font.render(message, 1, couleur)
	largeur, hauteur = font.size(message)
	affichage.blit(texte, (x-largeur/2, y-hauteur/2))
	
def afficher_image_centre(img, x, y):
	w, h = pygame.Surface.get_size(img)
	affichage.blit(img, (x-w/2, y-h/2))
		

#Ouverture de la fenêtre Pygame
dimension_fenetre = (1600, 900)
affichage = pygame.display.set_mode(dimension_fenetre, pygame.FULLSCREEN)

#Chargement
fond = pygame.image.load("ressources/noir.png").convert_alpha()

nombre_image = 3

largeur_image = int(dimension_fenetre[0]/(2*nombre_image))
hauteur_image = int(largeur_image*3/4)

#Chargement des classes
sniper = pygame.transform.scale(pygame.image.load("ressources/sniper.jpg").convert(), (largeur_image, hauteur_image))
tank = pygame.transform.scale(pygame.image.load("ressources/tank.jpg").convert(), (largeur_image, hauteur_image))
commando1 = pygame.transform.scale(pygame.image.load("ressources/commando.jpg").convert(), (largeur_image, hauteur_image))

cochee = pygame.transform.scale(pygame.image.load("ressources/cocher.png").convert_alpha(), (500, 400))
non_cochee = pygame.transform.scale(pygame.image.load("ressources/non_cochee.png").convert(), (100, 100))

classes = [commando1, sniper, tank]
nom_classe = ["Commando", "Sniper", "Tank"]

selection_clic = -1 #0 correspond allah première classe !

while True:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			fin()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				fin()
		if event.type == pygame.MOUSEBUTTONDOWN:
			selection_clic = selection
			print("Nouvelle selection : ", selection_clic)
	souris = pygame.mouse.get_pos()
	selection = int(souris[0]*nombre_image/dimension_fenetre[0])
			
	affichage.blit(fond, (0,0)) #clear
	afficher_texte("CHOOSE YOUR CLASS", dimension_fenetre[0]/2, 50, 34)
	
	for numero_image, img in enumerate(classes):
		x = largeur_image/2+2*numero_image*largeur_image
		x_centre = x+largeur_image/2
		affichage.blit(img, (x, 200))
		afficher_texte(nom_classe[numero_image], x_centre, 180, 25,(0,255,255))
		
		# si la souris est sur la classe ou que cette dernière est selectionnée alors on dessine un rectangle
		if numero_image == selection or numero_image == selection_clic:
			#couleur du rectangle de selection
			if numero_image == selection_clic:
				couleur = (0,255,0)
			else:
				couleur = (255,255,255)
			x1 = x_centre - largeur_image + 5
			pygame.draw.rect(affichage, couleur, (x1,150,2*largeur_image-5*2, dimension_fenetre[1]-240),5)
		
		
		#pour la description de la classe
		if numero_image == selection:
			afficher_image_centre(cochee, x_centre, 600)
		else:
			afficher_image_centre(non_cochee, x_centre, 600)
	
	pygame.display.flip()
	sleep(0.02)
	
