import pygame
import random
from pygame.color import THECOLORS
import time
import sys

class BackGround(pygame.sprite.Sprite):
	name = ""
	screen = None
#back_ground_index = 0
#step = 0
	def __init__(self, image_file, name, screen):
		#self._layer = -1
		pygame.sprite.Sprite.__init__(self)
		'''
		self.image = pygame.image.load(image_file).convert()
		self.image = pygame.transform.scale(self.image, (screen.get_width(), screen.get_height()))
		self.lrect = self.image.get_rect()
		self.rrect = self.image.get_rect()
		'''
		self.name = name
		self.screen = screen
		'''
		self.step = 1.4
		self.direct = 0
		'''

	def update(self, hero_speed_0:int, keep_move:bool):
		'''
		if hero_speed_0 != 0 or keep_move is False:
			self.direct = hero_speed_0
		if self.direct < 0:
			if self.back_ground_index > self.step:
				self.back_ground_index = self.back_ground_index - self.step
			else:
				self.back_ground_index = self.screen.get_width();
			#print("1 self.back_ground_index={}".format(self.back_ground_index))
		elif self.direct > 0:
			if self.back_ground_index + self.step < self.screen.get_width():
				self.back_ground_index = self.back_ground_index + self.step
			else:
				self.back_ground_index = 0
			#print("2 self.back_ground_index={}".format(self.back_ground_index))
		else:
			pass
		#刷新左侧的图形，将右侧移出到屏幕外侧的部分显示在左边
		#以达到连续背景的效果
		self.lrect.left = self.back_ground_index
		self.lrect.top = 0
		self.lrect.width = self.screen.get_width() - self.back_ground_index
		self.lrect.height = self.screen.get_height()
		self.rrect.left = 0
		self.rrect.top = 0
		self.rrect.width = self.back_ground_index
		self.rrect.height = self.screen.get_height()
		self.screen.blit(self.image, (0, 0, self.lrect.width, self.lrect.height), self.lrect)
		self.screen.blit(self.image, (self.screen.get_width() - self.back_ground_index, 0, self.rrect.width, self.rrect.height), self.rrect)
		'''
		#self.screen.blit(self.image, (0,0))
		self.screen.fill(THECOLORS['black'])

def main():
	pass

if __name__ == '__main__':
	main()
