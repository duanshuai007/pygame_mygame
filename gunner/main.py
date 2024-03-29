import pygame
import random
from pygame.color import THECOLORS
import time
import sys

from hero import Hero
#from hero_8 import Hero
from enemy import Enemy
from background import BackGround
import misc
from misc import pause,gameover,game_success,select_gift
import weapon_ringoffire
import weapon_fireball
from experience import Experience

HERO_SPEED = 2
ENEMY_SPEED = 1
GUN_SPEED = 10
GUN_INTERVAL_TS = 1500

from operator import itemgetter

def animate():
    bg.update(hero.speed[0], hero.keepmove)
    enemy_group.update((hero.rect.centerx, hero.rect.centery))
    for enemy in enemy_group:
        if enemy.alive():
            pass
        else:
            if enemy.time_to_clean(100):
                hero.score += 1
                exp = Experience(screen, enemy.getCurrentPos(), 15)
                experience_group.add(exp)
                enemy_group.remove(enemy)
                enemy.kill()

    experience_group.update(hero.getCurrentPos(), hero.getClosedDistance())
    for exp in experience_group:
        if exp.beCaught():
            experience_group.remove(exp)
            exp.kill()
            hero.add_experience()

    experience_group.draw(screen)
    enemy_group.draw(screen)
    intersect_monster = pygame.sprite.spritecollide(hero, enemy_group, False)
    if intersect_monster:
        hero.hurt()
    hero.update()

    for enemy in enemy_group:
        enemy.show_hurt_message()

    #misc.life_display_update(hero.life)
    screen.blit(pygame.font.Font.render(fontgame, "Score:{}".format(hero.score), 1, THECOLORS['white']), (20,10))
    screen.blit(pygame.font.Font.render(fontgame, "Hero Shot IntervalMs:{} Enemy Speed:{}".format(GUN_INTERVAL_TS, ENEMY_SPEED), 1, THECOLORS['white']), (200,10))
    #pygame.draw.line(screen, THECOLORS['green'], (hero.rect.left, hero.rect.top), (gun_pos_x, gun_pos_y), 2)
    #pygame.display.flip() 
    pygame.display.update()

pygame.init()
#设置窗口大小、颜色、载入图片   
size = width,height = 1024,768
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Gunner")

hero_file = 'hero.png'
#hero_file = 'aaaaaaaaaaa.jpeg'
enemy_file = 'monster1.png'
flyknife_file = 'fireball.png'
#flyknife_file = 'enemy.png'
enemy_death_file = 'explosion1.gif'
#flyknife_file = 'shot.gif'
#flyknife_file = 'knife.png'
#创建Clock的实例
clock = pygame.time.Clock()

#创建小组
enemy_group = pygame.sprite.Group()
experience_group = pygame.sprite.Group()
hero = Hero(hero_file, "hero", HERO_SPEED, enemy_group)
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
if pygame.key.get_focused() is True:
    pygame.event.set_grab(True)

g_gun_last_interval_ts = 0
g_enemy_last_add_ts = 0
unlucky_value = 0

w = weapon_ringoffire.RingOfFire(screen)
hero.set_weapon(w)
f = weapon_fireball.FireBall(screen)
hero.set_weapon(f)

while mRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mRunning = False
            #检查帧速率
            frame_rate = clock.get_fps()
            print ('frame rate =',frame_rate )
        elif event.type == pygame.USEREVENT:
            if event.attr == misc.ATTR_GAME_OVER:
                if gameover() == True:
                    enemy_group.empty()
                    experience_group.empty()
                    hero.move_status_clear()
                    hero.reset()
                    game_restart = True
                else:
                    pygame.quit()
            elif event.attr == 1000:
                hero.set_paramters('role', 'speed_rate', 0.5)    #人物移动速度+50%
            elif event.attr == 1001:
                hero.set_paramters('buttle', 'attack_rate', 0.5) #子弹攻击力+50%
            elif event.attr == 1002:
                hero.set_paramters('buttle', 'interval_rate', -0.2)   #子弹攻击间隔-20%
            elif event.attr == 1003:
                hero.set_paramters('role', 'hitpoint_rate', 1)   #生命值+1
            elif event.attr == 1004:
                hero.set_paramters('ringoffire', 'maxradius_rate', 0.2)   #火环最大攻击半径+20%
            elif event.attr == 1005:
                hero.set_paramters('role', 'expcloseddistance_rate', 1.0)   #拾取经验半径+100%
            elif event.attr == misc.ATTR_ROLE_UPGRADE:
                select_gift()
                hero.move_status_clear()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                hero.set_move_right()
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                hero.set_move_left()
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                hero.set_move_up()
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                hero.set_move_down()
            if event.key == pygame.K_SPACE:
                pause()
                #select_gift()
                hero.move_status_clear()
            elif event.key == pygame.K_q:
                frame_rate = clock.get_fps()
                pygame.quit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                hero.set_move_right_left_stop()
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                hero.set_move_right_left_stop()
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                hero.set_move_up_down_stop()
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                hero.set_move_up_down_stop()
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos_x,mouse_pos_y = event.pos
            hero.set_mouse_target((mouse_pos_x, mouse_pos_y))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hero.set_mouse_move_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            hero.set_mouse_move_stop()

    if game_restart is True:
        game_restart = False

    curr_ts = pygame.time.get_ticks()
    if (len(enemy_group) < 1 and game_restart is False):
        if hero.score < 500:
            ENEMY_SPEED = 1
            GUN_INTERVAL_TS = 1500
        elif hero.score >= 500:
            if game_success() is True:
                enemy_group.empty()
                hero.reset()
                game_restart = True
            else:
                pygame.quit()
        if curr_ts - g_enemy_last_add_ts > 100:
            g_enemy_last_add_ts = curr_ts
            for i in range(10):
                enemy = Enemy(screen, enemy_file, enemy_death_file, "enemy", (hero.rect.centerx, hero.rect.centery), ENEMY_SPEED, 100)
                enemy_group.add(enemy)
    animate()
    #控制帧速率
    clock.tick(60)

pygame.quit()
