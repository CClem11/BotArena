import cv2
# from threading import *
from time import sleep

class Portrait():
	def __init__(self):
		# Thread.__init__(self)
		self.video = cv2.VideoCapture(0)
		# self.start()
	
	def run(self):
		while True:
			self.actualiser()
			sleep(5)
		
	def actualiser(self):
		# print("nouvelle image !")
		ret, img = self.video.read()
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		# cv2.imwrite("ressources/img.png", img)
		# cv2.imshow('img', img)
		# img = cv2.bitwise_not(hsv)
		print(img[0, 0])
		return img
		
	# def actualiser(self):
		# print("nouvelle image !")
		# ret, img = self.video.read()
		# cv2.imwrite("ressources/img.png", img)
		
	def stop(self):
		cv2.destroyAllWindows()