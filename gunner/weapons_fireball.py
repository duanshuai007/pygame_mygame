import pygame
import random
import math
from pygame.color import THECOLORS
import misc

class fireball(pygame.sprite.Sprite):
    screen = None
    group = None
    default_speed = 0
    every_frame_update_count = 0
    cx = 0
    cy = 0
    target_enemy = None

    def __init__(self, image_file, hero_location:tuple, tar_location:tuple, group):
        pygame.sprite.Sprite.__init__(self)
        self.origin_image = pygame.image.load(image_file).convert_alpha()
        self.origin_image = pygame.transform.scale(self.origin_image, (30,30))
        self.image = self.origin_image
        self.rect = self.image.get_rect()
        self.default_speed = 0
        self.cx = hero_location[0]
        self.cy = hero_location[1]
        self.speed = [0, 0]
        self.screen = pygame.display.get_surface()
        self.group = group
        
    def update(self):
        self.move()
        
    def move(self):
        if self.target_enemy is None:
            pass
        else:
            cur_pos_x = self.cx
            cur_pos_y = self.cy
            tar_pos_x = self.target_enemy.rect.centerx 
            tar_pos_y = self.target_enemy.rect.centery
            angled = misc.calc_angle(cur_pos_x, cur_pos_y, tar_pos_x, tar_pos_y)
            vel_x,vel_y = misc.calc_angle_speed(angled)
            self.speed[0] = vel_x * self.default_speed
            self.speed[1] = vel_y * self.default_speed
            self.image = pygame.transform.rotate(self.origin_image, -angled)
            self.image.set_colorkey((255,255,255))
            self.rect = self.image.get_rect(center = self.rect.center)
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
            
    #如果设置了目标敌人，则子弹会每帧计算运行轨迹追踪敌人
    #如果没有设置敌人，则子弹按照初始化时的鼠标方向直线运动
    def set_target(self, target:object):
        self.target_enemy = target

    def set_speed(self, speed):
        self.default_speed = speed

#def rotate(self):
#		self.image = pygame.transform.flip(self.image, True, False)
#		self.rect = self.image.get_rect(center = self.rect.center)


def main():
    pass

if __name__ == '__main__':
    main()

