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
from misc import pause,gameover,game_success

JUMP_HEIGHT	= 3
JUMP_SPEED = -10
HERO_X_SPEED = 6
HERO_Y_SPEED = 6
ENEMY_SPEED = 1.5
global_counter = 0

from operator import itemgetter

def animate():
	global global_counter
	bg.update(hero.speed[0], hero.keepmove)

	fkgroup.update()
	hero.update()

	global_counter += 1
	if global_counter % 2 == 0:
		enemygroup.update((hero.rect.centerx, hero.rect.centery))
		for enemy in enemygroup:
			#enemy.move((hero.rect.centerx, hero.rect.centery))
			intersect_sprite = pygame.sprite.spritecollide(enemy, fkgroup, False)
			if intersect_sprite:
				for bullet in fkgroup:
					if bullet.target_enemy == enemy:
						fkgroup.remove(bullet)
						bullet.kill()
				enemy.kill()
				enemygroup.remove(enemy)
				hero.score+=1
				for bullet in intersect_sprite:
					fkgroup.remove(bullet)
					bullet.kill()

	enemygroup.draw(screen)
	intersect_monster = pygame.sprite.spritecollide(hero, enemygroup, False)
	if intersect_monster:
		hero.hurt()
	screen.blit(hero.image, hero.rect)
	misc.life_display_update(screen, hero.life)
	screen.blit(pygame.font.Font.render(fontgame, "Score:{}".format(hero.score), 1,(150,150,150)), (20,10))
	fkgroup.draw(screen)
	#pygame.draw.line(screen, THECOLORS['green'], (hero.rect.left, hero.rect.top), (gun_pos_x, gun_pos_y), 2)
#pygame.display.flip() 
	pygame.display.update()

pygame.init()
#设置窗口大小、颜色、载入图片   
size = width,height = 1024,768
screen = pygame.display.set_mode(size)
#screen.fill(THECOLORS['black'])
pygame.display.set_caption("Gunner")

hero_file = 'hero.png'
enemy_file = 'monter1.png'
flyknife_file = 'fireball.png'
#flyknife_file = 'knife.png'
#创建Clock的实例
clock = pygame.time.Clock()

#创建小组
fkgroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
hero = Hero(hero_file, "hero", screen)
bg = BackGround(None, "bg", screen)

font_type="times"
font_size=30
text = str("Score:{}".format(10))
fontgame = pygame.font.SysFont(font_type, font_size)

#主循环
mRunning = True
game_restart = False
gun_pos_x = 0
gun_pos_y = 0

pygame.event.set_allowed(pygame.USEREVENT)
pygame.key.set_repeat(40)
GUN_SPEED = 16
GUN_INTERVAL_TS = 1000

g_gun_last_interval_ts = 0

while mRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			mRunning = False
			#检查帧速率
			frame_rate = clock.get_fps()
			print ('frame rate =',frame_rate )
		elif event.type == pygame.USEREVENT:
			if event.attr == misc.GAME_OVER:
				if gameover(screen, clock) == True:
					enemygroup.empty()
					fkgroup.empty()
					hero.reset()
					game_restart = True
				else:
					pygame.quit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				hero.speed[0] = HERO_X_SPEED
				hero.towardright = True
#	hero.rotate(0)
				hero.keepmove = True
			elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
				hero.speed[0] = -HERO_X_SPEED
				hero.towardright = False
#w				hero.rotate(1)
				hero.keepmove = True
			elif event.key == pygame.K_UP or event.key == pygame.K_w:
				hero.speed[1] = -HERO_Y_SPEED
				hero.keepmove = True
			elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
				hero.speed[1] = HERO_Y_SPEED
				hero.keepmove = True
			elif event.key == pygame.K_SPACE:
				pause(screen, clock)
				#清除hero的移动速度等标志，清除按键记录信息
				#防止退出暂停后出现移动异常的问题
				hero.speed = [0,0]
				hero.keepmove = False
			elif event.key == pygame.K_q:
				frame_rate = clock.get_fps()
				print ('frame rate =',frame_rate )
				pygame.quit()
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_LEFT or event.key == pygame.K_a:
				hero.speed[0] = 0
				if hero.speed[1] == 0:
					hero.keepmove = False
			elif event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_DOWN or event.key == pygame.K_s:
				hero.speed[1] = 0
				if hero.speed[0] == 0:
					hero.keepmove = False
		elif event.type == pygame.MOUSEMOTION:
			gun_pos_x,gun_pos_y = event.pos
			#move_x,move_y = e.rel

	if game_restart is True:
		game_restart = False
	else:
		curr_ts = time.time() * 1000
		
#if curr_ts - g_gun_last_interval_ts > GUN_INTERVAL_TS:
		if curr_ts - g_gun_last_interval_ts > 100:
			g_gun_last_interval_ts = curr_ts
			distance_list = []
			for enemy in enemygroup:
				distance_list.append(enemy.get_distance((hero.rect.centerx, hero.rect.centery)))
			if len(distance_list):
				fk = fireball(flyknife_file, screen, (hero.rect.left, hero.rect.top), (gun_pos_x, gun_pos_y), fkgroup)
				fk.set_speed(GUN_SPEED)
				distance_list.sort(reverse=False, key=itemgetter(0))
				fk.set_target(distance_list[0][1])
				fkgroup.add(fk)
			
	if (len(enemygroup) < 16 and game_restart is False):
		if hero.score <= 25:
			ENEMY_SPEED = 4
			GUN_INTERVAL_TS = 1000
		elif hero.score > 25 and hero.score <= 50:
			ENEMY_SPEED = 5
			GUN_INTERVAL_TS = 900
		elif hero.score > 50 and hero.score <= 75:
			ENEMY_SPEED = 6
			GUN_INTERVAL_TS = 800
		elif hero.score > 75 and hero.score <= 100:
			ENEMY_SPEED = 7
			GUN_INTERVAL_TS = 700
		elif hero.score > 100 and hero.score <= 150:
			ENEMY_SPEED = 8
			GUN_INTERVAL_TS = 600
		elif hero.score > 150 and hero.score <= 200:
			ENEMY_SPEED = 8.5
			GUN_INTERVAL_TS = 400
		elif hero.score > 250 and hero.score <= 300:
			ENEMY_SPEED = 9
			GUN_INTERVAL_TS = 350
		elif hero.score > 300 and hero.score <= 400:
			ENEMY_SPEED = 9.5
			GUN_INTERVAL_TS = 300
		elif hero.score > 400 and hero.score < 500:
			ENEMY_SPEED = 10
			GUN_INTERVAL_TS = 250
		elif hero.score >= 500:
			if game_success(screen, clock) is True:
				enemygroup.empty()
				fkgroup.empty()
				hero.reset()
				game_restart = True
			else:
				pygame.quit()
		enemy = Enemy(enemy_file, "enemy", screen, (hero.rect.centerx, hero.rect.centery), ENEMY_SPEED)
		enemygroup.add(enemy)
		
	animate()
#控制帧速率
	clock.tick(30)

pygame.quit()
