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
	#enemy 只生成在hero位置为圆心,3/8屏幕高度为半径的范围之外
	def __init__(self, image_file, name, screen, location:tuple, speed:int):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image_file).convert_alpha()
		self.image = pygame.transform.scale(self.image, (30,30))
		self.image.set_colorkey((255,255,255))
		self.rect = self.image.get_rect()
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
		if location[0] < screen.get_width() / 2:
			self.rotate()
		self.name = name
		self.screen = screen

	def update(self, target:tuple):
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
		self.cx += self.speed[0]
		self.cy += self.speed[1]
		self.rect.centerx = round(self.cx)
		self.rect.centery = round(self.cy)
#        self.rect.left += self.speed[0]
#        self.rect.top += self.speed[1]
	#怪物转向
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

	def rotate(self):
		#self.image = pygame.transform.rotate(self.image, 180)
		self.image = pygame.transform.flip(self.image, True, False)
		self.rect = self.image.get_rect(center = self.rect.center)

def main():
    pass

if __name__ == '__main__':
    main()
