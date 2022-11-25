import pygame
import random
from pygame.color import THECOLORS
import time
import sys
import math
import misc
import queue

class Enemy(pygame.sprite.Sprite):
    name = ""
    default_speed = 0
    cx = 0
    cy = 0
    __rotate = 0
    __alive = True
    __death_ticks = 0
    __death_image_name = ""

    __DOT_fire_start_ts = 0  #怪物获得DOT的时间戳
    __DOT_fire_last_ts = 0   #怪物上一次被DOT伤害的时间戳
    __DOT_poison_start_ts = 0  #怪物获得DOT的时间戳
    __DOT_poison_last_ts = 0   #怪物上一次被DOT伤害的时间戳
    __HP = 0
    __screen = None
    __hurt_queue = None
    __hurt_show_start_ts = 0
    __hurt_point = 0
    __hurt_cx = 0
    __hurt_cy = 0

    #enemy 只生成在hero位置为圆心,3/8屏幕高度为半径的范围之外
    def __init__(self, main_screen, image_file, death_image_file, name, location:tuple, speed:int, HP:int):
        pygame.sprite.Sprite.__init__(self)
        self.__screen = main_screen
        font_type="times"
        font_size=20
        self.__layer = -1
        self.__hurt_queue = queue.Queue(3)
        self.__fontgame = pygame.font.SysFont(font_type, font_size)
        self.image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,20))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.__death_image_name = death_image_file
        self.default_speed = speed
        #self.screen = pygame.display.get_surface()
        x = random.randint(0, self.__screen.get_width());
        y = random.randint(0, self.__screen.get_height());
        while True:
            if math.sqrt((location[0] - x) * (location[0] - x) + (location[1] - y) * (location[1] - y)) > self.__screen.get_height() * 3 / 8:
                break
            else:
                if y >= self.__screen.get_height() // 2 and y < self.__screen.get_height():
                    y += 10
                elif y >= self.__screen.get_height():
                    y = 0
                elif y < self.__screen.get_height() // 2 and y > 0:
                    y -= 10
                elif y <= 0:
                    y = self.__screen.get_height()
        #self.rect.left, self.rect.top = [x, y]
        self.cx = x
        self.cy = y
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = [0, 0]
        self.name = name
        self.__HP = HP

    def update(self, target:tuple):
        if self.__alive is True:
            self.move(target)

    #动画函数
    def move(self, target:tuple):
        cur_pos_x = self.rect.left
        cur_pos_y = self.rect.top
        tar_pos_x = target[0]
        tar_pos_y = target[1]
        #如果不进行判断，每次都转动方向的话就形成了飞碟转动的效果
        '''
        if cur_pos_x < tar_pos_x:
            self.rotate(0)
        else:
            self.rotate(1)
        '''
        angle = misc.calc_angle(cur_pos_x, cur_pos_y, tar_pos_x, tar_pos_y)
        vel_x,vel_y = misc.calc_angle_speed(angle)
        self.rotate(0)
        self.cx += vel_x * self.default_speed
        self.cy += vel_y * self.default_speed
        self.rect.centerx = round(self.cx)
        self.rect.centery = round(self.cy)

    def show_hurt_message(self):
        if not self.__hurt_queue.empty():
            [self.__hurt_point, (self.__hurt_cx, self.__hurt_cy)] = self.__hurt_queue.get()
            self.__hurt_show_start_ts = pygame.time.get_ticks()

        if self.__hurt_show_start_ts + 200 >= pygame.time.get_ticks():
            self.__screen.blit(pygame.font.Font.render(self.__fontgame, "-{}".format(self.__hurt_point), 0, THECOLORS['white']), (self.__hurt_cx, self.__hurt_cy))

    def get_distance(self, location:tuple):
        '''
        a = abs(location[0] - self.rect.centerx)
        b = abs(location[1] - self.rect.centery)
        if a == 0:
            return [b, self]
        elif b == 0:
            return [a, self]
        else:
            c = math.sqrt(a*a + b*b)
            return [round(c, 1), self]
        '''
        return [round(misc.get_point_distance(location, (self.rect.centerx, self.rect.centery)), 1), self]

    def rotate(self, rotate:int):
        #self.image = pygame.transform.rotate(self.image, 180)
        '''
        if self.__rotate != rotate:
            self.__rotate = rotate
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(center = self.rect.center)
        '''
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = self.rect.center)

    def alive(self):
        return self.__alive

    def death(self, DP:int):
        self.__HP -= DP
        self.__hurt_queue.put([DP, (self.rect.centerx, self.rect.centery)])
        if self.__HP <= 0:
            self.__alive = False
            self.__death_ticks = pygame.time.get_ticks()
            self.image = pygame.image.load(self.__death_image_name).convert_alpha()
            self.image = pygame.transform.scale(self.image, (20,20))
            self.image.set_colorkey((255,255,255))
            self.rect = self.image.get_rect(center = self.rect.center)
            return True
        return False

    def time_to_clean(self, tick):
        if self.__alive is False:
            curr_tick = pygame.time.get_ticks()
            if curr_tick > self.__death_ticks + tick and self.__hurt_show_start_ts + 200 < curr_tick:
                return True
        return False

    def getCurrentPos(self):
        return (self.rect.centerx, self.rect.centery)

def main():
    pass

if __name__ == '__main__':
    main()
