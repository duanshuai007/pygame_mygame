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

HERO_X_SPEED = 3
HERO_Y_SPEED = 3
ENEMY_SPEED = 4
GUN_SPEED = 16
GUN_INTERVAL_TS = 1000
#每4帧怪物移动一次
global_counter = 0

from operator import itemgetter

def animate():
	global global_counter
	bg.update(hero.speed[0], hero.keepmove)

	bullte_group.update()
	hero.update()

	global_counter += 1
	if global_counter % 4 == 0:
		enemy_group.update((hero.rect.centerx, hero.rect.centery))
		for enemy in enemy_group:
			#enemy.move((hero.rect.centerx, hero.rect.centery))
			#对每个enemy都与子弹组进行碰撞检测
			if enemy.alive():
				intersect_sprite = pygame.sprite.spritecollide(enemy, bullte_group, False)
				if intersect_sprite:
					#设置enemy死亡状态
					enemy.death()
					#这里预估是将第一个触碰到enemy的子弹移除
					for bullet in intersect_sprite:
						bullte_group.remove(bullet)
						bullet.kill()
						break

					#寻找距离该被消灭的enemy附近距离最近的enemy
					distance_list = []
					for e in enemy_group:
						if e.alive():
							distance_list.append(e.get_distance((enemy.rect.centerx, enemy.rect.centery)))
					if len(distance_list):
						distance_list.sort(reverse=False, key=itemgetter(0))
					#有碰撞,对子弹组中的子弹进行判断，
					#因为该enemy即将删除，所以需要将目标是该enemy的子弹进行处理
					#其他子弹的target设置为此刻距离该enemy最近的enemy
					for bullet in bullte_group:
						if bullet.target_enemy == enemy:
							if len(distance_list):
								bullet.set_target(distance_list[0][1])
							else:
								bullet.set_target(None)
							#bullte_group.remove(bullet)
							#bullet.kill()
					#得分+1
					hero.score+=1
			else:
				#时间到清除该enemy
				if enemy.time_to_clean(200):
					enemy_group.remove(enemy)
					enemy.kill()

	enemy_group.draw(screen)
	intersect_monster = pygame.sprite.spritecollide(hero, enemy_group, False)
	if intersect_monster:
		hero.hurt()
	screen.blit(hero.image, hero.rect)
	misc.life_display_update(hero.life)
	screen.blit(pygame.font.Font.render(fontgame, "Score:{}".format(hero.score), 1, THECOLORS['white']), (20,10))
	screen.blit(pygame.font.Font.render(fontgame, "Hero Shot IntervalMs:{} Enemy Speed:{}".format(GUN_INTERVAL_TS, ENEMY_SPEED), 1, THECOLORS['white']), (200,10))
	bullte_group.draw(screen)
	#pygame.draw.line(screen, THECOLORS['green'], (hero.rect.left, hero.rect.top), (gun_pos_x, gun_pos_y), 2)
#pygame.display.flip() 
	pygame.display.update()

pygame.init()
#设置窗口大小、颜色、载入图片   
size = width,height = 1024,768
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Gunner")

hero_file = 'hero.png'
enemy_file = 'monster1.png'
flyknife_file = 'fireball.png'
enemy_death_file = 'explosion1.gif'
#flyknife_file = 'shot.gif'
#flyknife_file = 'knife.png'
#创建Clock的实例
clock = pygame.time.Clock()

#创建小组
bullte_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
hero = Hero(hero_file, "hero")
bg = BackGround(None, "bg")

font_type="times"
font_size=30
text = str("Score:{}".format(10))
fontgame = pygame.font.SysFont(font_type, font_size)

#主循环
mRunning = True
game_restart = False

pygame.event.set_allowed(pygame.USEREVENT)
pygame.key.set_repeat(40)

g_gun_last_interval_ts = 0

unlucky_value = 0

while mRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			mRunning = False
			#检查帧速率
			frame_rate = clock.get_fps()
			print ('frame rate =',frame_rate )
		elif event.type == pygame.USEREVENT:
			if event.attr == misc.GAME_OVER:
				if gameover() == True:
					enemy_group.empty()
					bullte_group.empty()
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
				pause()
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
		#elif event.type == pygame.MOUSEMOTION:
		#	gun_pos_x,gun_pos_y = event.pos
		#	move_x,move_y = e.rel

	if game_restart is True:
		game_restart = False
	else:
		curr_ts = pygame.time.get_ticks()
		if curr_ts - g_gun_last_interval_ts > GUN_INTERVAL_TS:
#if curr_ts - g_gun_last_interval_ts > 100:
			g_gun_last_interval_ts = curr_ts
			distance_list = []
			for enemy in enemy_group:
				if enemy.alive():
					distance_list.append(enemy.get_distance((hero.rect.centerx, hero.rect.centery)))
			if len(distance_list):
				distance_list.sort(reverse=False, key=itemgetter(0))
				r = random.randint(1, 10)
				#发射一颗子弹
				buttle_count = 0
				if r == 10:
					#连续发送6颗子弹
					buttle_count = 1
				else:
					unlucky_value += 1

				if unlucky_value >= 10:
					buttle_count = 1
					unlucky_value = 0

				if buttle_count == 0:
					fk = fireball(flyknife_file, (hero.rect.centerx, hero.rect.centery), (0, 0), bullte_group)
					fk.set_speed(GUN_SPEED)
					fk.set_target(distance_list[0][1])
					bullte_group.add(fk)
				else:
					fk = fireball(flyknife_file, (hero.rect.left, hero.rect.top), (0, 0), bullte_group)
					fk.set_speed(GUN_SPEED)
					fk.set_target(distance_list[0][1])
					bullte_group.add(fk)

					fk = fireball(flyknife_file, (hero.rect.left, hero.rect.top + hero.rect.height//2), (0, 0), bullte_group)
					fk.set_speed(GUN_SPEED)
					fk.set_target(distance_list[0][1])
					bullte_group.add(fk)

					fk = fireball(flyknife_file, (hero.rect.left, hero.rect.top + hero.rect.height), (0, 0), bullte_group)
					fk.set_speed(GUN_SPEED)
					fk.set_target(distance_list[0][1])
					bullte_group.add(fk)

					fk = fireball(flyknife_file, (hero.rect.left + hero.rect.width, hero.rect.top), (0, 0), bullte_group)
					fk.set_speed(GUN_SPEED)
					fk.set_target(distance_list[0][1])
					bullte_group.add(fk)

					fk = fireball(flyknife_file, (hero.rect.left + hero.rect.width, hero.rect.top + hero.rect.height//2), (0, 0), bullte_group)
					fk.set_speed(GUN_SPEED)
					fk.set_target(distance_list[0][1])
					bullte_group.add(fk)

					fk = fireball(flyknife_file, (hero.rect.left + hero.rect.width, hero.rect.top + hero.rect.height), (0, 0), bullte_group)
					fk.set_speed(GUN_SPEED)
					fk.set_target(distance_list[0][1])
					bullte_group.add(fk)
			
	if (len(enemy_group) < 16 and game_restart is False):
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
			if game_success() is True:
				enemy_group.empty()
				bullte_group.empty()
				hero.reset()
				game_restart = True
			else:
				pygame.quit()
		enemy = Enemy(enemy_file, enemy_death_file, "enemy", (hero.rect.centerx, hero.rect.centery), ENEMY_SPEED)
		enemy_group.add(enemy)
		
	animate()
#控制帧速率
	clock.tick(60)

pygame.quit()
