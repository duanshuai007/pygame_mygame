import pygame
import random 
from pygame.color import THECOLORS
import time

#定义小鸟类
class AngryBirdClass(pygame.sprite.Sprite):
	is_continue_collied = False
	continue_collied_count = 0
	name = ""
	def __init__(self, image_file, location, speed, name):
		pygame.sprite.Sprite.__init__(self) 
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
		self.speed = speed
		self.name = name
	#动画函数   
	def move(self):
		self.rect = self.rect.move(self. speed)
		if self.rect.left < 0 or self.rect.right > width:
			self.speed[0] = -self.speed[0]
		if self.rect.top < 0 or self.rect.bottom > height:
			self.speed[1] = -self.speed[1]
def animate(group):
	screen.fill(THECOLORS['green'])
	#先移动所有小鸟
	for bird in group:
		bird.move()
	#将小鸟从组中删除
	for bird in group:
		group.remove(bird)
		#检查碰撞
		intersect_sprite = pygame.sprite.spritecollide(bird, group, False)
		if intersect_sprite:
			#print(type(intersect_sprite))
			#rint(len(intersect_sprite))
			#print(intersect_sprite)
			for sprite in intersect_sprite:
				#print("sprite name:{}".format(sprite.name))
				if sprite.speed[0] == bird.speed[0] and sprite.speed[1] == bird.speed[1]:
					bird.speed[0] = random.choice([-3,3])
					bird.speed[1] = random.choice([-5,5])
			#print("{} {}".format(bird.name, bird.speed))
			if bird.is_continue_collied is True:
				#如果连续监测到碰撞，则可能是图片覆盖到另一个图片，此时不能调转方向，
				#否则会出现被覆盖的图片在原地不动(以极小-3，+3 -5，+5的xy速度抖动)的现象
				bird.continue_collied_count = bird.continue_collied_count + 1
				if bird.continue_collied_count > 20:
					#if bird.speed[0] > 0
					pass
			else:
				bird.speed[0] = -bird.speed[0]
				bird.speed[1] = -bird.speed[1]
				bird.is_continue_collied = True
		else:
			bird.is_continue_collied = False
			bird.continue_collied_count = 0
		#将小鸟添加回原组   
		group.add(bird)
		bird.move()
		screen.blit(bird.image, bird.rect)
	pygame.display.flip() 

#设置窗口大小、颜色、载入图片   
size = width,height = 800,600
screen = pygame.display.set_mode(size)
screen.fill(THECOLORS['black'])
img_file1 = 'redBird.png'
#img_file2 = 'blueBird.png'
img_file3 = 'blueBird.png'

#创建Clock的实例
clock = pygame.time.Clock()
#创建小组
group = pygame.sprite.Group()
for row in range(0,1):
	for column in range(0,2):
		print("a row={} col={}".format(row, column))
		location = [column*180+10, row*180+10]
		speed = [random.choice([-3,3]), random.choice([-5,5])]
		name = "bird{}{}".format(row, column)
		bird = AngryBirdClass(img_file1, location, speed, name)
		group.add(bird)
'''	
for row in range(0,1):
	for column in range(0,2):
		print("b row={} col={}".format(row, column))
		location = [column*180+100, row*180+100]
		speed = [random.choice([-5,5]), random.choice([-3,3])]
		bird = AngryBirdClass(img_file2, location, speed)
		group.add(bird)
'''
point = AngryBirdClass(img_file3, [180, 180], [0,0], "point")
group.add(point)

#主循环
mRunning = True
while mRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			mRunning = False
			#检查帧速率
			frame_rate = clock.get_fps()
			print ('frame rate =',frame_rate )
		elif event.type == pygame.MOUSEBUTTONDOWN:
			print("MOUSEBUTTONDOWN")
		elif event.type == pygame.MOUSEBUTTONUP:
			print("MOUSEBUTTONUP")
		elif event.type == pygame.MOUSEMOTION:
			#鼠标移动
			#print("MOUSEMOTION")
			mouse_pos = pygame.mouse.get_pos()
#print("mouse_pos 0:{} 1:{}".format(mouse_pos[0], mouse_pos[1]))
			#print("point pos x:{} y:{}".format(point.rect.left, point.rect.top))
#			point.speed[0] = mouse_pos[0] - point.rect.left
#			point.speed[1] = mouse_pos[1] - point.rect.top
			point.rect.left = mouse_pos[0]
			point.rect.top = mouse_pos[1]
#point.move()
#			screen.blit(point.image, point.rect)
#			pygame.display.flip() 
		elif event.type == pygame.MOUSEWHEEL:
			print("MOUSEWHEEL")
	animate(group)
#控制帧速率
	clock.tick(60)

pygame.quit()
