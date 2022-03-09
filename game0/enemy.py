import pygame
import random 
from pygame.color import THECOLORS
import time
import sys 


class Enemy(pygame.sprite.Sprite):
    name = ""
    screen = None
    default_speed = 0
    def __init__(self, image_file, name, screen, born_in_right:bool, speed:int, locationY:int):
        self._layer = 1
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.default_speed = speed
        if born_in_right is True:
            #self.rect.left, self.rect.top = [ screen.get_width() - self.rect.width, screen.get_height() - self.rect.height]
            self.rect.left, self.rect.top = [ screen.get_width() - self.rect.width, locationY - self.rect.height]
            self.speed = [-speed, 0]
        else:
            #self.rect.left, self.rect.top = [ 0, screen.get_height() - self.rect.height]
            self.rect.left, self.rect.top = [ 0, locationY - self.rect.height]
            self.speed = [speed, 0]
            self.rotate()
        self.name = name
        self.screen = screen
    #动画函数
    def move(self):
        if self.rect.left > (self.screen.get_width() - self.rect.width):
            self.speed[0] = -self.speed[0]
            self.rotate()
        elif self.rect.left < 0:
            self.speed[0] = -self.speed[0]
            self.rotate()
        self.rect = self.rect.move(self.speed)
        #如果怪物与主角相向运动，则加速
        #如果
        '''
        if hero.speed[0] != 0:
            if hero.towardright is True and hero.keepmove and self.speed[0] < 0:
                self.speed[0] = -2 * self.default_speed
            elif hero.towardright is False and hero.keepmove and self.speed[0] > 0:
                self.speed[0] = 2 * self.default_speed
            else:
                self.speed[0] = (self.speed[0] / abs(self.speed[0])) * self.default_speed
        else:
            self.speed[0] = (self.speed[0] / abs(self.speed[0])) * self.default_speed
        '''
    #怪物转向
    def rotate(self):
        #self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = self.rect.center)

def main():
	pass

if __name__ == '__main__':
	main()
