import pygame
import random
import math
from pygame.color import THECOLORS
import misc

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
#class RingOfFire(pygame.sprite.Sprite):
class RingOfFire():
    screen = None
    __weapon_type = 0
    __weapon_name = 'ringoffire'
    cx = 0
    cy = 0
    start_ts = 0
    radius = 15
    __hero_attack = 0
    __speed = 0
    __max_radius = 0
    __min_radius = 0
    __attack = 0
    __interval = 0

    def __init__(self, screen):
        #pygame.sprite.Sprite.__init__(self)
        self.screen = screen

    def update(self, hero_center_xy:tuple, paramters:dict):
        self.cx = hero_center_xy[0]
        self.cy = hero_center_xy[1]
        self.__speed = paramters['speed']
        self.__max_radius = paramters['maxradius']
        self.__min_radius = paramters['minradius']
        self.__interval = paramters['interval']
        self.__attack = paramters['attack']
        self.move()

    def move(self):
        curr_ts = pygame.time.get_ticks()
        if curr_ts > self.start_ts + self.__interval:
            self.start_ts = curr_ts
            self.radius += self.__speed
            if self.radius >= self.__max_radius:
                self.radius = self.__min_radius
            pygame.draw.circle(self.screen, THECOLORS['red'], (self.cx, self.cy), self.radius, 5)

    def attack(self, enemy_group):
        for e in enemy_group:
            r = misc.get_point_distance((self.cx, self.cy), (e.rect.centerx, e.rect.centery))
            if abs(self.radius - r) < 5:
                e.death(self.__attack)
    def getWeaponType(self):
        return self.__weapon_type
    def getWeaponName(self):
        return self.__weapon_name

    def draw(self):
        pass

def main():
    pass

if __name__ == '__main__':
    main()
