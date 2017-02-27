import pygame
from time import sleep

def fin():
	#quand on sortira de la boucle il faut fermer pygame
	pygame.quit()
	quit()

def afficher_image(x, y, inclinaison):
	"Fonction qui tourne l'image puis l'affiche en (x, y)"
	image = pygame.transform.rotate(image_originale, inclinaison)
	affichage.blit(image, (x, y))

def afficher_centre_image(image, x, y, inclinaison):
	"affiche une image centree et tournee en x, y"
	image_tournee = pygame.transform.rotate(image, inclinaison)
	largeur, hauteur = pygame.Surface.get_size(image_tournee)
	x -= largeur/2
	y -= hauteur/2
	affichage.blit(image_tournee, (x, y))

fenetre = (500, 500) 		#equivalent a [500, 500]          
affichage = pygame.display.set_mode(fenetre)

image_originale = pygame.image.load("mur.png") #on charge l'image
inclinaison = 0 #en degrees

while True:
	#Boucle for des evenements
	for event in pygame.event.get():		#	https://www.pygame.org/docs/ref/event.html
		if event.type == pygame.QUIT:
			fin()
		
		if event.type == pygame.KEYDOWN:
			#print(event.key)
			if event.key == pygame.K_UP:
				inclinaison += 5
			if event.key == pygame.K_DOWN:
				inclinaison -= 5
			print(inclinaison)
	
	#En dehors de la boucle des evenements
	affichage.fill((0, 0, 0))
	#afficher_image(250, 250, inclinaison)
	afficher_centre_image(image_originale, 250, 250, inclinaison)
	pygame.display.update()
	sleep(0.02)
	