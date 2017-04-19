# -*- coding:utf8 -*-

class Camera():
	def __init__(self, taille_fenetre_x, taille_fenetre_y):
		self.x = 0
		self.y = 0
		self.width = taille_fenetre_x
		self.height = taille_fenetre_y
	
	def set_position_centre(self, x, y):
		self.x = x - int(self.width/2)
		self.y = y - int(self.height/2)
		
	def get_position(self):
		return (self.x, self.y)