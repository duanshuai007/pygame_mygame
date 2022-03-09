import pygame
import random 
from pygame.color import THECOLORS
import time
import sys

from hero import Hero
from enemy import Enemy
from weapons_fireball import fireball
from background import BackGround
import misc
from misc import pause,gameover

JUMP_HEIGHT	= 3
JUMP_SPEED = -10
HERO_X_SPEED = 3
HERO_Y_SPEED = 2
ENEMY_SPEED = 1.5

def animate(group):
	bg.update(hero.speed[0], hero.keepmove)
	for knife in group:
		knife.move()
	
	for enemy in enemygroup:
		enemy.move()
		intersect_sprite = pygame.sprite.spritecollide(enemy, group, False)
		if intersect_sprite:
			enemy.kill()
			enemygroup.remove(enemy)
			hero.score+=1
			for sprite in intersect_sprite:
				fkgroup.remove(sprite)
				sprite.kill()
		else:
			screen.blit(enemy.image, enemy.rect)

	hero.move()
	intersect_monster = pygame.sprite.spritecollide(hero, enemygroup, False)
	if intersect_monster:
		hero.hurt()

	misc.life_display_update(screen, hero.life)
	screen.blit(pygame.font.Font.render(fontgame, "Score:{}".format(hero.score), 1,(150,150,150)), (20,10))
	for sprite in group:
		screen.blit(sprite.image, sprite.rect)
	pygame.display.flip() 

pygame.init()
#设置窗口大小、颜色、载入图片   
size = width,height = 1024,768
screen = pygame.display.set_mode(size)
#screen.fill(THECOLORS['black'])
pygame.display.set_caption("myGame")

#hero_file = 'redBird.png'
hero_file = 'hero1.png'
enemy_file = 'monter1.png'
flyknife_file = 'fireball.png'
background_file = 'background.jpg'
#创建Clock的实例
clock = pygame.time.Clock()

#创建小组
fkgroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
hero = Hero(hero_file, "hero", screen)
enemy = Enemy(enemy_file, "enemy", screen, True, ENEMY_SPEED, random.randint(int(screen.get_height() * 0.6), screen.get_height()))
enemygroup.add(enemy)

bg = BackGround(background_file, "bg", screen)

font_type="times"
font_size=30
text = str("Score:{}".format(10))
fontgame = pygame.font.SysFont(font_type, font_size)

#主循环
mRunning = True
game_restart = False
KeyLRPressCount = 0
KeyUDPressCount = 0

pygame.event.set_allowed(pygame.USEREVENT)

while mRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			mRunning = False
			#检查帧速率
			frame_rate = clock.get_fps()
			print ('frame rate =',frame_rate )
		elif event.type == pygame.USEREVENT:
			print("user event:{}".format(event))
			if event.attr == misc.GAME_OVER:
				if gameover(screen, clock) == True:
					enemygroup.empty()
					fkgroup.empty()
					hero.reset()
					KeyUDPressCount = 0
					KeyLRPressCount = 0
					game_restart = True
				else:
					pygame.quit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				hero.speed[0] = HERO_X_SPEED
				hero.towardright = True
				KeyLRPressCount += 1
				hero.rotate(0)
				hero.keepmove = True
			elif event.key == pygame.K_LEFT:
				hero.speed[0] = -HERO_X_SPEED
				hero.towardright = False
				KeyLRPressCount += 1
				hero.rotate(1)
				hero.keepmove = True
			elif event.key == pygame.K_UP:
				hero.speed[1] = -HERO_Y_SPEED
				KeyUDPressCount += 1
				hero.keepmove = True
				pass
			elif event.key == pygame.K_DOWN:
				hero.speed[1] = HERO_Y_SPEED
				KeyUDPressCount += 1
				hero.keepmove = True
				pass
			elif event.key == pygame.K_SPACE:
				pause(screen, clock)
				#gameover(screen, clock)
				#e = pygame.event.Event(pygame.USEREVENT, attr=misc.GAME_OVER)
				#pygame.event.post(e)
				#清除hero的移动速度等标志，清除按键记录信息
				#防止退出暂停后出现移动异常的问题
				hero.speed = [0,0]
				hero.keepmove = False
				KeyUDPressCount = 0
				KeyLRPressCount = 0
				pass
				'''
				elif event.key == pygame.K_z:
					#jump
					if hero.is_in_air is False:
					hero.speed[1] = JUMP_SPEED
					hero.is_jump = True
					hero.is_in_air = True
				'''
			elif event.key == pygame.K_x:
				#short
				left = hero.rect.left
				top = hero.rect.top
				name = "kf_{}_{}".format(left, top)
				fk = fireball(flyknife_file, name, screen)
				loca = [0, top + (hero.rect.height * 0.3)]
				speed = 20
				if hero.towardright is True:
					loca[0] = left + (hero.rect.width / 3)
				else:
					loca[0] = left - (fk.rect.width / 3)
					speed = -speed
					fk.rotate()
				fk.fly(loca, speed )
				fkgroup.add(fk)
			elif event.key == pygame.K_q:
				print("game exit")
				pygame.quit()
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
				KeyLRPressCount -= 1
				if KeyLRPressCount == 0:
					hero.speed[0] = 0
					if hero.speed[1] == 0:
						hero.keepmove = False
			elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				KeyUDPressCount -= 1
				if KeyUDPressCount == 0:
					hero.speed[1] = 0
					if hero.speed[0] == 0:
						hero.keepmove = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			#rint("MOUSEBUTTONDOWN")
			pass
		elif event.type == pygame.MOUSEBUTTONUP:
			#rint("MOUSEBUTTONUP")
			pass
		elif event.type == pygame.MOUSEMOTION:
			#鼠标移动
			#print("MOUSEMOTION")
			mouse_pos = pygame.mouse.get_pos()
#			point.rect.left = mouse_pos[0]
#			point.rect.top = mouse_pos[1]
#point.move()
#			screen.blit(point.image, point.rect)
#			pygame.display.flip() 
		elif event.type == pygame.MOUSEWHEEL:
			print("MOUSEWHEEL")
	if game_restart is True:
		game_restart = False
		enemy = Enemy(enemy_file, "enemy", screen, True, ENEMY_SPEED, random.randint(int(screen.get_height() * 0.6), screen.get_height()))
		enemygroup.add(enemy)
	if (len(enemygroup) < 3 and len(enemygroup) > 0):
		r = random.randint(1,100)
		#print("random={}".format(r))
		exit = False
		while True:
			ry = random.randint(int(screen.get_height() * 0.6), screen.get_height())
			for e in enemygroup:
				if ry < e.rect.top + 40 and ry > e.rect.top - 40:
					ry = random.randint(int(screen.get_height() * 0.6), screen.get_height())
				else:
					exit = True
					break
			if exit is True:
				break
		if r % 2 == 0:
			enemy = Enemy(enemy_file, "enemy", screen, True, ENEMY_SPEED, ry)
			enemygroup.add(enemy)
		else:
			enemy = Enemy(enemy_file, "enemy", screen, False, ENEMY_SPEED, ry)
			enemygroup.add(enemy)
		
	animate(fkgroup)
#控制帧速率
	clock.tick(60)

pygame.quit()
