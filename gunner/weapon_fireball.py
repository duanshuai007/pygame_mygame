import pygame
import random
import math
from pygame.color import THECOLORS
import misc
from operator import itemgetter

'''
子弹属性:
持续伤害(火，毒)
负面效果(减速，降低攻击，百分比掉血，无视防御）
子弹穿透
子弹弹射
多重弹药(霰弹枪)
眩晕麻痹(雷)
范围内持续快速掉血(献祭)
爆裂弹药(打中或到达最大记录爆炸)
回旋弹
'''
#子类，只在该文件中使用
class mfireball(pygame.sprite.Sprite):
    screen = None
    group = None
    default_speed = 0
    cx = 0
    cy = 0
    #target_enemy = None
    __disappear_point = None
    __image_file = 'fireball.png'
    def __init__(self, screen, hero_location:tuple, tar_location:tuple, group, distance, speed):
        pygame.sprite.Sprite.__init__(self)
        self.origin_image = pygame.image.load(self.__image_file).convert_alpha()
        self.origin_image = pygame.transform.scale(self.origin_image, (15,15))
        self.image = self.origin_image
        self.rect = self.image.get_rect()
        self.default_speed = speed
        self.cx = hero_location[0]
        self.cy = hero_location[1]
        self.ox = self.cx
        self.oy = self.cy
        self.speed = [0, 0]
        self.screen = screen
        self.group = group
        self.distance = distance

        angled = misc.calc_angle(self.cx, self.cy, tar_location.rect.centerx, tar_location.rect.centery)
        vel_x,vel_y = misc.calc_angle_speed(angled)
        self.speed[0] = vel_x * self.default_speed
        self.speed[1] = vel_y * self.default_speed
        self.image = pygame.transform.rotate(self.origin_image, -angled)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center = self.rect.center)
        self.__disappear_point = None

    def update(self):
        self.move()

    def move(self):
        #如果子弹移动超出了最大距离，则删除该子弹
        if misc.get_point_distance([self.cx, self.cy], [self.ox, self.oy]) > self.distance:
            self.group.remove(self)
            self.kill()
            return
        if self.__disappear_point:
            min_distance =  misc.get_point_distance((self.rect.centerx, self.rect.centery), self.__disappear_point)
            if min_distance <= 10:
                self.group.remove(self)
                self.kill()
                return

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

    def set_target(self, target:object):
        #self.target_enemy = target
        pass

    #invaild_bullet_group无效子弹组，不参与碰撞计算
    def set_disappear_point(self, invaild_fireball_group, disappear:tuple):
        self.__disappear_point = disappear
        self.group = invaild_fireball_group
        #print("disappear point={} {}".format(disappear[0], disappear[1]))

    def set_speed(self, speed):
        self.default_speed = speed

#主类，生成火球型武器，hero可以通过set_weapon进行装备。可以装备多种类型武器。
class FireBall():
    cx = 0
    cy = 0
    screen = None
    __last_shot_ts = 0
    __unlucky_value = 0
    fireball_group = None
    invaild_group = None
    __weapon_type = 1
    __weapon_name = 'buttle'

    __interval = 0
    __speed = 0
    __attack = 0
    __distance = 0

    def __init__(self, screen):
        self.screen = screen
        self.fireball_group = pygame.sprite.Group()
        self.invaild_group = pygame.sprite.Group()

    def update(self, hero_center_xy:tuple, paramters:dict):
        self.cx = hero_center_xy[0]
        self.cy = hero_center_xy[1]
        self.__interval = paramters['interval']
        self.__speed = paramters['speed']
        self.__attack = paramters['attack']
        self.__distance = paramters['distance']
        self.move()

    def move(self):
        self.fireball_group.update()
        self.invaild_group.update()

    def draw(self):
        self.fireball_group.draw(self.screen)
        self.invaild_group.draw(self.screen)

    def getWeaponType(self):
        return self.__weapon_type
    def getWeaponName(self):
        return self.__weapon_name

    def attack(self, enemy_group):
        curr = pygame.time.get_ticks()
        #周期射出子弹
        if curr - self.__last_shot_ts > self.__interval:
            self.__last_shot_ts = curr
            distance_list = []
            for enemy in enemy_group:
                if enemy.alive():
                    distance_list.append(enemy.get_distance((self.cx, self.cy)))
            if len(distance_list):
                distance_list.sort(reverse=False, key=itemgetter(0))
                r = random.randint(1, 10)
                buttle_count = 0
                if r == 10:
                    #连续发送6颗子弹
                    buttle_count = 1
                else:
                    self.__unlucky_value += 1

                if self.__unlucky_value >= 10:
                    buttle_count = 1
                    self.__unlucky_value = 0

                if buttle_count == 0:
                    fk = mfireball(self.screen, (self.cx, self.cy), distance_list[0][1], self.fireball_group, self.__distance, self.__speed)
                    self.fireball_group.add(fk)
                else:
                    fk = mfireball(self.screen, (self.cx - 20, self.cy), distance_list[0][1], self.fireball_group, self.__distance, self.__speed)
                    self.fireball_group.add(fk)
                    fk = mfireball(self.screen, (self.cx + 20, self.cy), distance_list[0][1], self.fireball_group, self.__distance, self.__speed)
                    self.fireball_group.add(fk)
                    fk = mfireball(self.screen, (self.cx, self.cy - 20), distance_list[0][1], self.fireball_group, self.__distance, self.__speed)
                    self.fireball_group.add(fk)
                    fk = mfireball(self.screen, (self.cx, self.cy + 20), distance_list[0][1], self.fireball_group, self.__distance, self.__speed)
                    self.fireball_group.add(fk)
        else:
            for enemy in enemy_group:
                if enemy.alive():
                    intersect_sprite = pygame.sprite.spritecollide(enemy, self.fireball_group, False)
                    if intersect_sprite:
                        for fb in self.fireball_group:
                            enemy.death(self.__attack)
                            self.fireball_group.remove(fb)
                            fb.set_disappear_point(self.invaild_group, enemy.getCurrentPos())
                            break
        pass



