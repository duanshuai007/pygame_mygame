import pygame
import random
import math
from pygame.color import THECOLORS

def warp_angle(angle):
	return abs(angle % 360)

class fireball(pygame.sprite.Sprite):
	screen = None
	group = None
	default_speed = 0
	every_frame_update_count = 0
	cx = 0
	cy = 0
	target_enemy = None

	def __init__(self, image_file, hero_location:tuple, tar_location:tuple, group):
		pygame.sprite.Sprite.__init__(self)
		self.origin_image = pygame.image.load(image_file).convert_alpha()
		self.origin_image = pygame.transform.scale(self.origin_image, (30,10))
#self.origin_image.set_colorkey((255,255,255))
		self.image = self.origin_image
		self.rect = self.image.get_rect()
		self.default_speed = 0
		self.cx = hero_location[0]
		self.cy = hero_location[1]
		self.speed = [0, 0]
		self.screen = pygame.display.get_surface()
		self.group = group

		cur_pos_x = hero_location[0]
		cur_pos_y = hero_location[1]
		tar_pos_x = tar_location[0]
		tar_pos_y = tar_location[1]
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
			'''
			if tar_pos_x > cur_pos_x:
				fx = 1
			elif tar_pos_x < cur_pos_x:
				fx = -1
			else:
				fx = 0

			if tar_pos_y > cur_pos_y:
				fy = 1
			elif tar_pos_y < cur_pos_y:
				fy = -1
			else:
				fy = 0
			'''
			'''
			#A = math.degrees(math.acos((a*a - b*b - c*c) / (-2*b*c)))
			A = math.degrees(math.acos((b*b - a*a - c*c) / (-2*a*c)))
			#print(int(A))
			#angle = math.pi * A
			angle = A
			self.speed[0] = fx * math.cos(math.radians(angle)) * SPEED
			self.speed[1] = fy * math.sin(math.radians(angle)) * SPEED
			'''
#			self.speed[0] = round(self.default_speed * a / c, 1)
#			self.speed[1] = round(self.default_speed * b / c, 1)
			self.speed[0] = round(self.default_speed * a / c, 4)
			self.speed[1] = round(self.default_speed * b / c, 4)
			
	def update(self):
		self.move()

	def move(self):
		if self.target_enemy is None:
			pass	
		else:
			cur_pos_x = self.cx
			cur_pos_y = self.cy
			tar_pos_x = self.target_enemy.rect.centerx 
			tar_pos_y = self.target_enemy.rect.centery
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
				self.speed[0] = round(self.default_speed * a / c, 4)
				self.speed[1] = round(self.default_speed * b / c, 4)
			delta_x = tar_pos_x - cur_pos_x
			delta_y = tar_pos_y - cur_pos_y
			angle = math.atan2(delta_y, delta_x)
			angled = warp_angle(-math.degrees(angle))
			self.image = pygame.transform.rotate(self.origin_image, angled)
			self.image.set_colorkey((255,255,255))
			self.rect = self.image.get_rect(center = self.rect.center)

		self.cx += self.speed[0]
		self.cy += self.speed[1]
		self.rect.centerx = round(self.cx)
		self.rect.centery = round(self.cy)
		
		if self.rect.left < 0 or self.rect.left > self.screen.get_width() - self.rect.width:
			self.group.remove(self)
			self.kill()
		elif self.rect.top < 0 or self.rect.top > self.screen.get_height() - self.rect.height:
			self.group.remove(self)
			self.kill()
			#else:
			#    self.screen.blit(self.image, self.rect)

	#如果设置了目标敌人，则子弹会每帧计算运行轨迹追踪敌人
	#如果没有设置敌人，则子弹按照初始化时的鼠标方向直线运动
	def set_target(self, target:object):
		self.target_enemy = target

	def set_speed(self, speed):
		self.default_speed = speed

#def rotate(self):
#		self.image = pygame.transform.flip(self.image, True, False)
#		self.rect = self.image.get_rect(center = self.rect.center)


def main():
    pass

if __name__ == '__main__':
    main()

