map1 = "ressources/map1.txt"
map2 = "ressources/map2.txt"

marqueur_vide = "-"
marqueur_plein = "#"

def ouvrir_map(chemin):
	with open(chemin, 'r') as fichier:
		map = {}
		for l, ligne in enumerate(fichier.readlines()):
			for c, caractere in enumerate(ligne):
				if caractere == marqueur_plein:
					map[c, l] = "v"
		#print(map)
		return map

if __name__ == '__main__':
	ouvrir_map(map2)