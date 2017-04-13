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
		

#Ouverture de la fenêtre Pygame
dimension_fenetre = (1500, 850)
fenetre = pygame.display.set_mode(dimension_fenetre, pygame.FULLSCREEN)

#Chargement
fond = pygame.image.load("ressources/noir.png").convert_alpha()


scale = 1.0

dimension_icone = (320, 180)
dimension_icone_zoom = (480, 270)

#Chargement des classes
sniper = pygame.image.load("ressources/sniper.jpg").convert()
sniper2 = pygame.image.load("ressources/sniper2.jpg").convert()
commando1 = pygame.image.load("ressources/commando.jpg").convert()

classes = [commando1, sniper, sniper2, commando1]

hauteur_icone = 250
w,h = sniper.get_size()
sniper = pygame.transform.scale(sniper, (int(w*scale), int(h*scale)))
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

	pygame.display.flip()
	sleep(0.02)
	
