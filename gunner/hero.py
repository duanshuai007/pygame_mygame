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
	score = 0
	life = 0
	life_protect_ts = 0
	is_hurt = False
	hurt_display_count = 0
	hurt_display_ts = 0
	action_update_ts = 0
	keepmove = False
	images = []
	
	toward_up = 0
	toward_down = 1
	toward_left = 2
	toward_right = 3
	
	def __init__(self, image_file, name):
		self._layer = 1
		pygame.sprite.Sprite.__init__(self)
		self.master_image = pygame.image.load(image_file).convert_alpha()
		self.master_image.set_colorkey((255,255,255))
		self.master_image_number = 16
		self.master_image_w = self.master_image.get_width() // self.master_image_number
		self.master_image_h = self.master_image.get_height()
		self.master_image_index = 0
		self.screen = pygame.display.get_surface()
		rect = (0, 0, self.master_image_w, self.master_image_h)
		self.image = self.master_image.subsurface(rect)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = [self.screen.get_width() / 2 - self.rect.width / 2, self.screen.get_height() * 0.7 - self.rect.height]

		self.speed = [0, 0]
		self.name = name
		
		self.life = 5
		self.is_hurt = False
		self.hurt_display_count = 0
		self.hurt_display_ts = 0

	def update(self):
		self.move()

	#动画函数
	def move(self):
		#添加人物受伤时的闪烁效果
		if self.is_hurt is True:
			curr_ts = pygame.time.get_ticks()
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
				self.change_image(self.toward_right)
			else:
				self.change_image(self.toward_left)
		else:
			self.change_image(self.toward_down)
			pass
		if self.rect.left < 0:
			self.speed[0] = 0
			self.rect.left = 0
		elif self.rect.left > (self.screen.get_width() * 1.0) - self.rect.width:
			self.speed[0] = 0
			self.rect.left = (self.screen.get_width() * 1.0) - self.rect.width
		if self.rect.top < 0:
			self.speed[1] = 0
			self.rect.top = 0
		elif self.rect.top > self.screen.get_height() - self.rect.height:
			self.speed[1] = 0
			self.rect.top = self.screen.get_height() - self.rect.height

		#self.screen.blit(self.image, self.rect)
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

	def change_image(self, toward:int):
		curr_ts = pygame.time.get_ticks()
		if curr_ts - self.action_update_ts > 80:
			self.action_update_ts = curr_ts
			self.master_image_index += 1
			if toward == self.toward_up:
				if self.master_image_index < 12 or self.master_image_index > 15:
					self.master_image_index = 12
			elif toward == self.toward_down:
				if self.master_image_index > 3:
					self.master_image_index = 0
			elif toward == self.toward_left:
				if self.master_image_index < 4 or self.master_image_index > 7:
					self.master_image_index = 4
			elif toward == self.toward_right:
				if self.master_image_index < 8 or self.master_image_index > 11:
					self.master_image_index = 8
			rect = (self.master_image_index * self.master_image_w, 0, self.master_image_w, self.master_image_h)
			self.image = self.master_image.subsurface(rect)
			self.rect = self.image.get_rect(center=self.rect.center)

	def hurt(self):
		curr_ts = pygame.time.get_ticks()
		if curr_ts - self.life_protect_ts > 1000:
			self.life_protect_ts = curr_ts
			self.life -= 1
			self.is_hurt = True
			self.hurt_display_count = 0
			if self.life == 0:
				misc.post_event_gameover()

	def reset(self):
		self.index = 0
		self.image = self.master_image.subsurface((0,0,self.master_image_w,self.master_image_h))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = [self.screen.get_width() / 2 - self.rect.width / 2, self.screen.get_height() * 0.7 - self.rect.height]

		self.speed = [0, 0]
		self.towardright = True
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
