import pygame
import random
from pygame.color import THECOLORS
import time
import sys
import math
import misc
import queue

class Experience(pygame.sprite.Sprite):
    screen = None
    default_speed = 0
    cx = 0
    cy = 0
    __be_caught = False #捕获
    __is_closed = False #接近
    __caught_distance = 10
    def __init__(self, main_screen, location:tuple, speed:int):
        pygame.sprite.Sprite.__init__(self)
        self.__screen = main_screen
        self.__layer = -1
        self.image = pygame.image.load('hero_life.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (10,10))
        self.image.set_colorkey((255,0,0))
        self.rect = self.image.get_rect()
        self.default_speed = speed
        self.cx = location[0]
        self.cy = location[1]
        self.rect.centerx = self.cx
        self.rect.centery = self.cy

    def update(self, target:tuple, closed_distance:float):
        if self.__is_closed is False:
            if misc.get_point_distance( (self.rect.centerx, self.rect.centery), target) > closed_distance:
                return
            self.__is_closed = True
        else:
            self.move(target)

    #动画函数
    def move(self, target:tuple):
        angle = misc.calc_angle(self.cx, self.cy, target[0], target[1])
        vel_x,vel_y = misc.calc_angle_speed(angle)
        self.cx += vel_x * self.default_speed
        self.cy += vel_y * self.default_speed
        self.rect.centerx = round(self.cx)
        self.rect.centery = round(self.cy)
        if misc.get_point_distance( (self.rect.centerx, self.rect.centery), target) < self.__caught_distance:
            self.__be_caught = True

    #def getCurrentPos(self):
    #    return (self.rect.centerx, self.rect.centery)

    def beCaught(self):
        return self.__be_caught

def main():
    pass

if __name__ == '__main__':
    main()
