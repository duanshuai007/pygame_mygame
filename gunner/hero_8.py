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
	toward_upleft = 4
	toward_upright = 5
	toward_downleft = 6
	toward_downright = 7

	cx = 0
	cy = 0
	default_speed = 0

	def __init__(self, image_file, name, speed):
		self._layer = 1
		pygame.sprite.Sprite.__init__(self)
		self.master_image = pygame.image.load(image_file).convert_alpha()
#self.master_image.set_colorkey((255,255,255))
		self.master_image_col_number = 6
		self.master_image_row_number = 8
		self.master_image_w = self.master_image.get_width() // self.master_image_col_number
		self.master_image_h = self.master_image.get_height() // self.master_image_row_number

		self.master_image_index = 0
		self.screen = pygame.display.get_surface()
		rect = (0, 0, self.master_image_w, self.master_image_h)
		self.image = self.master_image.subsurface(rect)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = [self.screen.get_width() / 2 - self.rect.width / 2, self.screen.get_height() * 0.7 - self.rect.height]

		self.speed = [0, 0]
		self.name = name
		
		self.cx = self.rect.centerx
		self.cy = self.rect.centery
		self.default_speed = speed
		self.life = 5
		self.is_hurt = False
		self.hurt_display_count = 0
		self.hurt_display_ts = 0
		#self.fontgame = pygame.font.Font(None, 50)
		
	def update(self, target:tuple):
		self.move(target)

#动画函数
	def move(self, target:tuple):
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
				self.rect = self.rect.move(self.speed)
				return
		if target[0] > self.rect.left and target[0] < self.rect.left + self.rect.width and target[1] > self.rect.top and target[1] < self.rect.top + self.rect.height:
			self.change_image(self.toward_down)
			self.screen.blit(self.image, self.rect)
			return
		angled = misc.calc_angle(self.cx, self.cy, target[0], target[1])
		vel_x,vel_y = misc.calc_angle_speed(angled)
		self.speed[0] = vel_x * self.default_speed
		self.speed[1] = vel_y * self.default_speed
		self.cx += self.speed[0]
		self.cy += self.speed[1]
		self.rect.centerx = round(self.cx)
		self.rect.centery = round(self.cy)
		#self.screen.blit(pygame.font.Font.render(self.fontgame, "angle:{:.2f}".format(angled), 1, THECOLORS['white']), (100,500))
		#self.rect = self.rect.move(self.speed)
		#人物最多超出屏幕半个身位
		if (angled >= -22) and (angled < 22):
			self.change_image(self.toward_right)
		elif (angled >= 22) and (angled < 68):
			self.change_image(self.toward_downright)
		elif (angled >= 68) and (angled < 112):
			self.change_image(self.toward_down)
		elif (angled >= 112) and (angled < 157):
			self.change_image(self.toward_downleft)
		elif (angled >= 157) or (angled < -157):
			self.change_image(self.toward_left)
		elif (angled >= -157) and (angled < -112):
			self.change_image(self.toward_upleft)
		elif (angled >= -112) and (angled < -68):
			self.change_image(self.toward_up)
		elif (angled >= -68) and (angled < -22):
			self.change_image(self.toward_upright)
		'''
		if (angled >= -90) and (angled <= 90):
			self.change_image(self.toward_right)
		else:
			self.change_image(self.toward_left)
		'''
		'''
		if self.keepmove is True:
			if self.towardright is True:
				self.change_image(self.toward_right)
			else:
				self.change_image(self.toward_left)
		else:
			self.change_image(self.toward_down)
		'''
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

	def change_image(self, toward:int):
		curr_ts = pygame.time.get_ticks()
		if curr_ts - self.action_update_ts > 80:
			self.action_update_ts = curr_ts
			self.master_image_index += 1
			if self.master_image_index >= 6:
				self.master_image_index = 0
			curr_row = 0
			if toward == self.toward_up:
				curr_row = 0
			elif toward == self.toward_down:
				curr_row = 4
			elif toward == self.toward_left:
				curr_row = 6
			elif toward == self.toward_right:
				curr_row = 2
			elif toward == self.toward_upleft:
				curr_row = 7
			elif toward == self.toward_upright:
				curr_row = 1
			elif toward == self.toward_downleft:
				curr_row = 5
			elif toward == self.toward_downright:
				curr_row = 3
			rect = (self.master_image_index * self.master_image_w, curr_row * self.master_image_h, self.master_image_w, self.master_image_h)
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
