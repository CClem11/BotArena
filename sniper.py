from robot import *
from projectile import SniperProj

class Sniper(Robot):
	def __init__(self):
		Robot.__init__(self)
		self.temps_rechargement = 0.1
		self.type_projectile = SniperProj