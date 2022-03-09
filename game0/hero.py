import pygame
import random
from pygame.color import THECOLORS
import time
import sys

import misc

#定义小鸟类
class Hero(pygame.sprite.Sprite):
	name = ""
	#挑起动作状态标志 True:上跳状态 False:下落状态
	#   is_jump = False
	#跳跃落地标志位，防止在空中重复跳跃
	#   is_in_air = False
	screen = None
	towardright = True
	toward = 0
	index = 0
	score = 0
	life = 0
	life_protect_ts = 0
	is_hurt = False
	hurt_display_count = 0
	hurt_display_ts = 0
	action_update_ts = 0
	keepmove = False
	images = []
	def __init__(self, image_file, name, screen):
		self._layer = 1
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load(image_file).convert()
		self.original_width = img.get_width() // 16
		self.original_height = img.get_height()
		x = 0
		print("w={} h={} w={} h={}".format(img.get_width(), img.get_height(), self.original_width, self.original_height))
		for frame_no in range(0,15):
			frame_surface = pygame.Surface([self.original_width, self.original_height])
			frame_surface.blit(img, [x, 0])
			frame_surface.set_colorkey((255,255,255))
			self.images.append(frame_surface)
			x -= self.original_width
			print("x={}".format(x))
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		#self.rect.left, self.rect.top = [20, screen.get_height() - self.rect.height]
		self.rect.left, self.rect.top = [screen.get_width() / 2 - self.rect.width / 2, screen.get_height() * 0.7 - self.rect.height]

		self.current_index = 0
		self.speed = [0, 0]
		self.name = name
		self.screen = screen
		self.life = 5
		self.is_hurt = False
		self.hurt_display_count = 0
		self.hurt_display_ts = 0
	#动画函数
	def move(self):
		#添加人物受伤时的闪烁效果
		if self.is_hurt is True:
			curr_ts = time.time() * 1000
			if curr_ts - self.hurt_display_ts > 60:
				self.hurt_display_ts = curr_ts
				self.hurt_display_count += 1
				if self.hurt_display_count > 6:
					#stop hurt action
					self.is_hurt = False
					self.hurt_display_count = 0
			else:
				return
			pass
		self.rect = self.rect.move(self.speed)
		#人物最多超出屏幕半个身位
		if self.keepmove is True:
			if self.towardright is True:
				self.change_image("right")
			else:
				self.change_image("left")
		else:
			self.change_image("down")
			pass
		#if self.rect.left < (0 - (self.rect.width / 2)):
		if self.rect.left < 0:
			self.speed[0] = 0
			#self.rect.left = (0 - (self.rect.width / 2))
			self.rect.left = 0
		#elif self.rect.left > (self.screen.get_width() - (self.rect.width / 2)):
		elif self.rect.left > (self.screen.get_width() * 1.0) - self.rect.width:
			self.speed[0] = 0
			#self.rect.left = (self.screen.get_width() - (self.rect.width / 2))
			self.rect.left = (self.screen.get_width() * 1.0) - self.rect.width
		elif self.rect.top < self.screen.get_height() * 0.5:
			self.speed[1] = 0
			self.rect.top = self.screen.get_height() * 0.5
		elif self.rect.top > self.screen.get_height() - self.rect.height:
			self.speed[1] = 0
			self.rect.top = self.screen.get_height() - self.rect.height

		self.screen.blit(self.image, self.rect)
		'''
		#人物跳起落下的动作
		if self.is_jump is True:
			if self.rect.top < self.screen.get_height() - (JUMP_HEIGHT * self.rect.height):
				self.speed[1] = -self.speed[1]
				self.is_jump = False
		else:
			if self.rect.top > self.screen.get_height() - self.rect.height:
				self.speed[1] = 0
				self.rect.top = self.screen.get_height() - self.rect.height
				self.is_in_air = False
		'''
	def rotate(self, toward:int):
		if self.toward != toward:
			#self.image = pygame.transform.rotate(self.image, 180)
			self.image = pygame.transform.flip(self.image, True, False)
			self.rect = self.image.get_rect(center = self.rect.center)
			self.toward = toward

	def change_image(self, toward:str):
		curr_ts = time.time() * 1000
		if curr_ts - self.action_update_ts > 80:
			self.action_update_ts = curr_ts
			self.index = self.index + 1
			if toward == "up":
				if self.index < 12 or self.index > 15:
					self.index = 12
			elif toward == "down":
				if self.index > 3:
					self.index = 0
			elif toward == "left":
				if self.index < 4 or self.index > 7:
					self.index = 4
			elif toward == "right":
				if self.index < 8 or self.index > 11:
					self.index = 8
			self.image = self.images[self.index]
			center = self.rect.center
			self.rect = self.image.get_rect()
			self.rect.center = center

	def hurt(self):
		curr_ts = time.time() * 1000
		if curr_ts - self.life_protect_ts > 1000:
			self.life_protect_ts = curr_ts
			self.life -= 1
			self.is_hurt = True
			self.hurt_display_count = 0
			if self.life == 0:
				misc.post_event_gameover()

	def reset(self):
		self.index = 0
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = [self.screen.get_width() / 2 - self.rect.width / 2, self.screen.get_height() * 0.7 - self.rect.height]

		self.current_index = 0
		self.speed = [0, 0]
		self.towardright = True
		self.toward = 0
		self.score = 0
		self.action_update_ts = 0
		self.keepmove = False
		self.life_protect_ts = 0
		self.life = 5
		self.is_hurt = False
		self.hurt_display_count = 0

def main():
	pass

if __name__ == '__main__':
	main()
