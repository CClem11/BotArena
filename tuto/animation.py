import pygame
from time import sleep

def fin():
	#quand on sortira de la boucle il faut fermer pygame
	pygame.quit()
	quit()
	
def zoom_effect(zoom):
	"0 < zoom < 1 -----> 0 < f(zoom) < 1"
	if 0 < zoom <= 2:
		return 1 - (zoom-1)**4
	else:
		return 1

def afficher_centre_image(image, x, y, zoom):
	"affiche une image centree et tournee en x, y"
	w1 = int(w*zoom)
	h1 = int(h*zoom)
	image_tournee = pygame.transform.scale(image_originale, (w1, h1))
	largeur, hauteur = pygame.Surface.get_size(image_tournee)
	x -= largeur/2
	y -= hauteur/2
	affichage.blit(image_tournee, (x, y))

def animation():
	print("animation")
	z = 0.01
	while zoom_effect(z) < zoom:
		affichage.fill((0, 0, 0))
		afficher_centre_image(image_originale, 250, 250, zoom_effect(z))
		pygame.display.update()
		sleep(0.015)
		z += 0.01
		
fenetre = (500, 500) 		#equivalent a [500, 500]          
affichage = pygame.display.set_mode(fenetre)

image_originale = pygame.image.load("mur1.png") #on charge l'image
w, h = pygame.Surface.get_size(image_originale)
zoom = 1 # fois 1

while True:
	#Boucle for des evenements
	for event in pygame.event.get():		#	https://www.pygame.org/docs/ref/event.html
		if event.type == pygame.QUIT:
			fin()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a: # sur qwerty donc il faut appuyer sur 'q'
				animation()
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			#print(event.button)
			if event.button == 4:
				zoom += 0.05
			if event.button == 5 and zoom > 0.05:
				zoom -= 0.05
	
	#En dehors de la boucle des evenements
	affichage.fill((0, 0, 0))
	afficher_centre_image(image_originale, 250, 250, zoom)
	pygame.display.update()
	sleep(0.02)
	