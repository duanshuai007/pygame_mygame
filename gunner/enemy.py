import pygame
import random 
from pygame.color import THECOLORS
import time
import sys 
import math

class Enemy(pygame.sprite.Sprite):
	name = ""
	screen = None
	default_speed = 0
	cx = 0
	cy = 0
	__rotate = 0
	__alive = True
	__death_ticks = 0
	__death_image_name = ""
	#enemy 只生成在hero位置为圆心,3/8屏幕高度为半径的范围之外
	def __init__(self, image_file, death_image_file, name, screen, location:tuple, speed:int):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image_file).convert_alpha()
		self.image = pygame.transform.scale(self.image, (40,40))
		self.image.set_colorkey((255,255,255))
		self.rect = self.image.get_rect()
		self.__death_image_name = death_image_file
		self.default_speed = speed
		x = random.randint(0, screen.get_width());
		y = random.randint(0, screen.get_height());
		while True:
			if math.sqrt((location[0] - x) * (location[0] - x) + (location[1] - y) * (location[1] - y)) > screen.get_height() * 3 / 8:
				break
			else:
				if y >= screen.get_height() // 2 and y < screen.get_height():
					y += 10
				elif y >= screen.get_height():
					y = 0
				elif y < screen.get_height() // 2 and y > 0:
					y -= 10
				elif y <= 0:
					y = screen.get_height()
		#self.rect.left, self.rect.top = [x, y]
		self.cx = x
		self.cy = y
		self.rect.centerx = x
		self.rect.centery = y
		self.speed = [0, 0]
		self.name = name
		self.screen = screen

	def update(self, target:tuple):
		if self.__alive is True:
			self.move(target)

    #动画函数
	def move(self, target:tuple):
		cur_pos_x = self.rect.left
		cur_pos_y = self.rect.top
		tar_pos_x = target[0]
		tar_pos_y = target[1]
		'''
		#min_end_x = math.cos(math.radians(wrap_angle((t.minute * (360 / 60) + (t.second / 12)) - 90))) * (radius - 60)
		#min_end_y = math.sin(math.radians(wrap_angle((t.minute * (360 / 60) + (t.second / 12)) - 90))) * (radius - 60)
		a = abs(tar_pos_x - cur_pos_x)
		b = abs(tar_pos_y - cur_pos_y)
		c = math.sqrt(a*a + b*b)
		if a > 0 and b > 0 and c > 0:
			A = math.degrees(math.acos((a*a - b*b - c*c) / (-2*b*c)))
			#A = math.degrees(math.acos((b*b - a*a - c*c) / (-2*a*c)))
			#print(A)
			if tar_pos_x > cur_pos_x:
				fx = -1
			elif tar_pos_x < cur_pos_x:
				fx = 1
			else:
				fx = 0

			if tar_pos_y > cur_pos_y:
				fy = -1
			elif tar_pos_y < cur_pos_y:
				fy = 1
			else:
				fy = 0

			angle = -1 * math.pi * A
			#angle = -1 * A
			self.rect.left += fx * self.default_speed * math.cos(math.radians(angle))
			self.rect.top += fy * self.default_speed * math.sin(math.radians(angle))
			#self.screen.blit(self.image, self.rect)
		else:
			return
		'''
		if cur_pos_x == tar_pos_x:
			if tar_pos_y > cur_pos_y:
				self.speed[0] = 0
				self.speed[1] = self.default_speed
			elif tar_pos_y < cur_pos_y:
				self.speed[0] = 0
				self.speed[1] = -self.default_speed
		elif cur_pos_y == tar_pos_y:
			if tar_pos_x > cur_pos_x:
				self.speed[0] = self.default_speed
				self.speed[1] = 0
			elif tar_pos_x < cur_pos_x:
				self.speed[0] = -self.default_speed
				self.speed[1] = 0
		else:
			a = tar_pos_x - cur_pos_x
			b = tar_pos_y - cur_pos_y
			c = math.sqrt(a*a + b*b)
			self.speed[0] = self.default_speed * a / c
			self.speed[1] = self.default_speed * b / c

		#如果不进行判断，每次都转动方向的话就形成了飞碟转动的效果
		'''
		if cur_pos_x < tar_pos_x:
			self.rotate(0)
		else:
			self.rotate(1)
		'''
		self.rotate(0)
		self.cx += self.speed[0]
		self.cy += self.speed[1]
		self.rect.centerx = round(self.cx)
		self.rect.centery = round(self.cy)

	def get_distance(self, location:tuple):
		a = abs(location[0] - self.rect.centerx)
		b = abs(location[1] - self.rect.centery)
		if a == 0:
			return [b, self]
		elif b == 0:
			return [a, self]
		else:
			c = math.sqrt(a*a + b*b)
			return [round(c, 1), self]

	def rotate(self, rotate:int):
		#self.image = pygame.transform.rotate(self.image, 180)
		'''
		if self.__rotate != rotate:
			self.__rotate = rotate
			self.image = pygame.transform.flip(self.image, True, False)
			self.rect = self.image.get_rect(center = self.rect.center)
		'''
		self.image = pygame.transform.flip(self.image, True, False)
		self.rect = self.image.get_rect(center = self.rect.center)

	def alive(self):
		return self.__alive

	def death(self):
		self.__alive = False
		self.__death_ticks = pygame.time.get_ticks()
		self.image = pygame.image.load(self.__death_image_name).convert_alpha()
		self.image = pygame.transform.scale(self.image, (40,40))
		self.image.set_colorkey((255,255,255))
		self.rect = self.image.get_rect(center = self.rect.center)

	def time_to_clean(self, tick):
		if self.__alive is False:
			curr_tick = pygame.time.get_ticks()
			if curr_tick > self.__death_ticks + tick:
				return True
		return False

def main():
    pass

if __name__ == '__main__':
    main()
