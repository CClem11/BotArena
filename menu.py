from __future__ import print_function
import pygame
from pygame.locals import *
pygame.init()
from time import sleep

def fin():
	pygame.quit()
	quit()
def afficher_texte(message, x, y):
	font = pygame.font.SysFont("Arial Black", 34)
	texte = font.render(message, 1, (255,255,255))
	largeur, hauteur = font.size(message)
	fenetre.blit(texte, (x-largeur/2, y-hauteur/2))
def afficher_image_centre(img, x, y):
	w, h = pygame.Surface.get_size(img)
	fenetre.blit(img, (x-w/2, y-h/2))
	
def afficher_classes():
	partie_x = dimension_fenetre[0]/(2*len(classes))
	for i, classe in enumerate(classes):
		afficher_image_centre(classe, (2*i+1)*partie_x, hauteur_icone)
		
def souris_sur_image():
	x, y = pygame.mouse.get_pos()
	partie_x = dimension_fenetre[0]/(2*len(classes))
	liste_souris_sur_image = [False for i in range(len(classes))]
	for i in range(len(classes)):
		x1 = (2*i+1)*partie_x - dimension_icone[0]/2
		x2 = x1 + dimension_icone[0]
		y1 = hauteur_icone - dimension_icone[1]/2
		y2 = y1 + dimension_icone[1]
		# pygame.draw.rect(fenetre, (255, 0, 0), (x1, y1, dimension_icone[0], dimension_icone[1]), 1)
		if x1 <= x <= x2:
			if y1 <= y <= y2:
				liste_souris_sur_image[i] = True				
	return liste_souris_sur_image
	
def animation():
	liste = souris_sur_image()
	print(liste)
	for i, img in enumerate(liste):
		if img==True:
			classes[i] = pygame.transform.scale(classes[i], (dimension_icone_zoom))
		else:
			classes[i] = pygame.transform.scale(classes[i], (dimension_icone))
		
	
	
#Ouverture de la fenêtre Pygame
dimension_fenetre = (1500, 850)
fenetre = pygame.display.set_mode(dimension_fenetre, pygame.FULLSCREEN)

#Chargement
fond = pygame.image.load("ressources/noir.png").convert_alpha()

dimension_icone = (320, 180)
dimension_icone_zoom = (480, 270)

#Chargement des classes
sniper = pygame.image.load("ressources/sniper.jpg").convert()
sniper2 = pygame.image.load("ressources/sniper2.jpg").convert()
commando1 = pygame.image.load("ressources/commando.jpg").convert()

classes = [commando1, sniper, sniper2, commando1]

hauteur_icone = 250

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			fin()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				fin()
	fenetre.blit(fond, (0,0))
	afficher_texte("CHOOSE YOUR CLASS", dimension_fenetre[0]/2, 50)
	afficher_classes()
	animation()
	pygame.display.flip()
	sleep(0.02)
	
