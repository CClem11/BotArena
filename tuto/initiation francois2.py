import pygame
from time import sleep

def fin():
	#quand on sortira de la boucle il faut fermer pygame
	pygame.quit()
	quit()
	
fenetre = (1920, 1080) 		#equivalent a [500, 500]          
affichage = pygame.display.set_mode(fenetre,pygame.FULLSCREEN)
x = 250
y = 250

#boucle principale (le "void loop" de pygame)
while True:
	#Boucle for des evenements
	for event in pygame.event.get():		#	https://www.pygame.org/docs/ref/event.html
		#print(event)
		if event.type == pygame.QUIT:
			fin()
		
		if event.type == pygame.KEYDOWN:
			print(event.key)
			if event.key == pygame.K_LEFT:
				x = x - 20
			if event.key == pygame.K_RIGHT:
				x = x + 20
			if event.key == pygame.K_UP:
				y -= 20
			if event.key == pygame.K_DOWN:
				y += 20	
	
	#En dehors de la boucle des evenements
	affichage.fill((0, 0, 0))
	pygame.draw.circle(affichage, [255, 0, 255], (x, y), 50) # au milieu de la fenetre un rond de r=50 pixels couleur=magenta (vive la chimie)
	pygame.display.update()
	sleep(0.02)
	