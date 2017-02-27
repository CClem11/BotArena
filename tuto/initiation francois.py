import pygame
from time import sleep # comme le delay sur arduino mais le nombre en parametre est en seconde

fenetre = (500, 500) 		#equivalent a [500, 500]          
affichage = pygame.display.set_mode(fenetre)

#boucle principale (le "void loop" de pygame)
while True:
	#choisis ce que tu veux dessiner ici : https://www.pygame.org/docs/ref/draw.html
	#  moi je prends le cercle c'est celui qui demande le moins de parametres :)
	pygame.draw.circle(affichage, [255, 0, 255], (250, 250), 50) # au milieu de la fenetre un rond de r=50 pixels couleur=magenta (vive la chimie)
	
	# pour afficher quelque chose ensuite il faut update la fenetre d'affichage
	pygame.display.update()
	
	#rajoute du delais sinon on va "fumer" le pc 
	sleep(0.02) # soit 50 fps (1/50 de seconde)

#quand on sortira de la boucle il faut fermer pygame
pygame.quit()
