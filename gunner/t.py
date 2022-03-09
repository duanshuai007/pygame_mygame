import pygame
import random
from pygame.color import THECOLORS
import math


pygame.init()
#设置窗口大小、颜色、载入图片
size = width,height = 1024,768
screen = pygame.display.set_mode(size)
#screen.fill(THECOLORS['black'])
pygame.display.set_caption("Gunner")

op_x = screen.get_width() // 2
op_y = screen.get_height() // 2
 
x = 0
y = 0

angle = 0
radius = 200

origin_image = pygame.image.load("knife.png").convert_alpha()
rect = origin_image.get_rect()
clock = pygame.time.Clock()

font = pygame.font.Font(None, 30)

def warp_angle(angle):
	return abs(angle%360)

def print_text(screen, font, x, y, msg, color):
	f = font.render(msg, True, color)
	rect = f.get_rect()
	rect.x = x
	rect.y = y
	screen.blit(f, rect)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			mRunning = False
			#检查帧速率
			#frame_rate = clock.get_fps()
			#print ('frame rate =', frame_rate )
			pygame.quit()
	screen.fill(THECOLORS['black'])
	angle += 1
	if angle > 360:
		angle = 0

	op_x = x
	op_y = y

	x = math.cos(math.radians(angle)) * radius
	y = math.sin(math.radians(angle)) * radius

	delta_x = x - op_x
	delta_y = y - op_y

	mangle = math.atan2(delta_y, delta_x)
	mangled = math.degrees(warp_angle(mangle))
	mangled2 = warp_angle(-math.degrees(mangle))
	image = pygame.transform.rotate(origin_image, mangled2)
	#pygame.draw.circle(screen, THECOLORS['red'], (x, y), 10, 2)
	rect = image.get_rect()

	screen.blit(image, (screen.get_width() // 2 + x - image.get_width() // 2, screen.get_height() // 2 + y - image.get_height() // 2))

	print_text(screen, font, 0, 0, "mangle={:.2f}".format(mangle), THECOLORS['red'])
	print_text(screen, font, 0, 30, "mangled={:.2f}".format(mangled), THECOLORS['red'])
	print_text(screen, font, 0, 60, "mangled2={:.2f}".format(mangled2), THECOLORS['red'])
	pygame.display.update()
	clock.tick(60)
