import pygame
import random
from pygame.color import THECOLORS
import time
import sys

import misc

#定义小鸟类
class Hero(pygame.sprite.Sprite):
    name = ""
    #挑起动作状态标志 True:上跳状态 False:下落状态
    #   is_jump = False
    #跳跃落地标志位，防止在空中重复跳跃
    #   is_in_air = False
    screen = None
    towardright = True
    score = 0
    life_protect_ts = 0
    is_hurt = False
    hurt_display_count = 0
    hurt_display_ts = 0
    action_update_ts = 0
    keepmove = False
    images = []

    toward_up = 0
    toward_down = 1
    toward_left = 2
    toward_right = 3
    cx = 0
    cy = 0
    __move_to_x = 0
    __move_to_y = 0
    __mouse_move = False
    __keyboard_move = False
    __mouse_target = ()

    weapon = []
    enemy_group = None

    is_unbeatable = False   #无敌

    __paramters = {
        'role' : {
            'speed' : 2,
            'hitpoint' : 8,
            'expcloseddistance' : 90,
        },
        'buttle' : {
            'speed' : 10,
            'interval' : 1500,
            'attack' : 20,
            'distance' : 300,
            'ejection' : 0,                 #是否弹射
            'withFire' : 0,
            'withIce' : 0,
            'withLightning' : 0,
            'poison' : 0,
            'split' : 0,    #分裂
        },
        'ringoffire' : {
            'speed' : 3,
            'maxradius' : 120,
            'interval' : 10,
            'minradius' : 15,
            'attack' : 8,
        },
    }
    __paramters_base = {
        'role' : {
            'hitpoint_base' : 8,
            'hitpoint_rate'  : 0,
            'speed_base': 2,
            'speed_rate': 1.0,
            'expcloseddistance_base' : 90,
            'expcloseddistance_rate' : 1.0,
        },
        'buttle' : {
            'speed_base' : 10,
            'speed_rate' : 1.0,
            'interval_base' : 1500,
            'interval_rate' : 1.0,
            'attack_base' : 20,
            'attack_rate' : 1.0,
            'distance_base' : 300,
            'distance_rate' : 1.0,
        },
        'ringoffire' : {
            'speed_base' : 3,
            'speed_rate' : 1.0,
            'maxradius_base' : 120,
            'maxradius_rate' : 1.0,
            'interval_base' : 10,
            'interval_rate' : 1.0,
            'minradius_base' : 15,
            'minradius_rate' : 1.0,
            'attack_base' : 8,
            'attack_rate' : 1.0,
        },
    }

    __experience = 0
    __level = 1

    def __init__(self, image_file, name, speed, enemy_group):
        self._layer = 0
        pygame.sprite.Sprite.__init__(self)
        self.master_image = pygame.image.load(image_file).convert_alpha()
        self.master_image.set_colorkey((255,255,255))
        self.master_image_number = 16
        self.master_image_w = self.master_image.get_width() // self.master_image_number
        self.master_image_h = self.master_image.get_height()
        self.master_image_index = 0
        self.screen = pygame.display.get_surface()
        rect = (0, 0, self.master_image_w, self.master_image_h)
        self.image = self.master_image.subsurface(rect)
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [self.screen.get_width() / 2 - self.rect.width / 2, self.screen.get_height() * 0.7 - self.rect.height]

        self.speed = [0, 0]
        self.name = name

        self.cx = self.rect.centerx
        self.cy = self.rect.centery
        self.is_hurt = False
        self.hurt_display_count = 0
        self.hurt_display_ts = 0
        self.keepmove = False
        self.enemy_group = enemy_group
        #self.fontgame = pygame.font.Font(None, 50)

    def update(self):
        #update role hitpoint display
        misc.life_display_update(self.__paramters['role']['hitpoint'])
        if self.__mouse_move is True:
            self.mouse_move(self.__mouse_target)
        elif self.__keyboard_move is True:
            self.keyboard_move()
        self.__keepflash()

    def set_weapon(self, weapon):
        self.weapon.append(weapon)

    def set_paramters(self, mkey:str, ckey:str, value:float):
        print("mkey={} ckey={} value={}".format(mkey, ckey, value))
        if mkey in self.__paramters_base.keys():
            if ckey in self.__paramters_base[mkey].keys():
                self.__paramters_base[mkey][ckey] += value
                if self.__paramters_base[mkey][ckey] <= 0:
                    self.__paramters_base[mkey][ckey] = 0.1
            cword = ckey.split('_')[0]
            c_base = "{}_base".format(cword)
            c_rate = "{}_rate".format(cword)
            if cword == "hitpoint":
                self.__paramters[mkey][cword] = self.__paramters_base[mkey][c_base] + self.__paramters_base[mkey][c_rate]
            else:
                self.__paramters[mkey][cword] = self.__paramters_base[mkey][c_base] * self.__paramters_base[mkey][c_rate]
        else:
            print("set_paramters can't find key:{}".format(key))

    def __keepflash(self):
        #子弹或武器动画的移动更新和攻击行为判定
        for w in self.weapon:
            w.update((self.rect.centerx, self.rect.centery), self.__paramters[w.getWeaponName()])
            w.attack(self.enemy_group)
        #添加人物受伤时的闪烁效果
        if self.is_hurt is True:
            curr_ts = pygame.time.get_ticks()
            if curr_ts - self.hurt_display_ts > 60:
                self.hurt_display_ts = curr_ts
                self.hurt_display_count += 1
                if self.hurt_display_count > 6:
                    #stop hurt action
                    self.is_hurt = False
                    self.hurt_display_count = 0
            else:
                self.rect = self.rect.move(self.speed)
                return
        self.rect.centerx = round(self.cx)
        self.rect.centery = round(self.cy)

        if self.rect.left < 0:
            self.speed[0] = 0
            self.rect.left = 0
        elif self.rect.left > (self.screen.get_width() * 1.0) - self.rect.width:
            self.speed[0] = 0
            self.rect.left = (self.screen.get_width() * 1.0) - self.rect.width
        if self.rect.top < 0:
            self.speed[1] = 0
            self.rect.top = 0
        elif self.rect.top > self.screen.get_height() - self.rect.height:
            self.speed[1] = 0
            self.rect.top = self.screen.get_height() - self.rect.height

        self.screen.blit(self.image, self.rect)
        #in keyboard mode, when player press direction key, cx or cy will continue add or sub, even it alread less than 0 or bigger ther 
        #screen max size, so we need make it keep in vaild range. 
        self.cx = self.rect.centerx
        self.cy = self.rect.centery

        #绘制武器
        for w in self.weapon:
            w.draw()

    def keyboard_move(self):
        angled = misc.calc_angle(0, 0, self.__move_to_x, self.__move_to_y)
        vel_x,vel_y = misc.calc_angle_speed(angled)
        self.speed[0] = vel_x * self.__paramters['role']['speed']
        self.speed[1] = vel_y * self.__paramters['role']['speed']
        self.cx += self.speed[0]
        self.cy += self.speed[1]
        if (angled >= -90) and (angled <= 90):
            self.change_image(self.toward_right)
        else:
            self.change_image(self.toward_left)

    def mouse_move(self, target:tuple):
        '''
        if target[0] > self.rect.left and target[0] < self.rect.left + self.rect.width and target[1] > self.rect.top and target[1] < self.rect.top + self.rect.height:
            self.change_image(self.toward_down)
            self.screen.blit(self.image, self.rect)
            return
        '''
        angled = misc.calc_angle(self.cx, self.cy, target[0], target[1])
        vel_x,vel_y = misc.calc_angle_speed(angled)
        self.speed[0] = vel_x * self.__paramters['role']['speed']
        self.speed[1] = vel_y * self.__paramters['role']['speed']
        #print("mouse speed={}".format(self.speed[0]*self.speed[0] + self.speed[1]*self.speed[1]))
        self.cx += self.speed[0]
        self.cy += self.speed[1]
        if (angled >= -90) and (angled <= 90):
            self.change_image(self.toward_right)
        else:
            self.change_image(self.toward_left)

        #self.screen.blit(pygame.font.Font.render(self.fontgame, "angle:{:.2f}".format(angled), 1, THECOLORS['white']), (100,500))
        #self.rect = self.rect.move(self.speed)
        #人物最多超出屏幕半个身位
        '''
        if self.keepmove is True:
            if self.towardright is True:
                self.change_image(self.toward_right)
            else:
                self.change_image(self.toward_left)
        else:
            self.change_image(self.toward_down)
        #人物跳起落下的动作
        if self.is_jump is True:
            if self.rect.top < self.screen.get_height() - (JUMP_HEIGHT * self.rect.height):
                self.speed[1] = -self.speed[1]
                self.is_jump = False
        else:
            if self.rect.top > self.screen.get_height() - self.rect.height:
                self.speed[1] = 0
                self.rect.top = self.screen.get_height() - self.rect.height
                self.is_in_air = False
        '''

    def change_image(self, toward:int):
        curr_ts = pygame.time.get_ticks()
        if curr_ts - self.action_update_ts > 80:
            self.action_update_ts = curr_ts
            self.master_image_index += 1
            if toward == self.toward_up:
                if self.master_image_index < 12 or self.master_image_index > 15:
                    self.master_image_index = 12
            elif toward == self.toward_down:
                if self.master_image_index > 3:
                    self.master_image_index = 0
            elif toward == self.toward_left:
                if self.master_image_index < 4 or self.master_image_index > 7:
                    self.master_image_index = 4
            elif toward == self.toward_right:
                if self.master_image_index < 8 or self.master_image_index > 11:
                    self.master_image_index = 8
            rect = (self.master_image_index * self.master_image_w, 0, self.master_image_w, self.master_image_h)
            self.image = self.master_image.subsurface(rect)
            self.image = pygame.transform.scale(self.image, (30,30))
            self.rect = self.image.get_rect(center=self.rect.center)

    def hurt(self):
        if self.is_unbeatable is True:
            return
        curr_ts = pygame.time.get_ticks()
        if curr_ts - self.life_protect_ts > 3000:
            self.life_protect_ts = curr_ts
            self.__paramters['role']['hitpoint'] -= 1
            self.is_hurt = True
            self.hurt_display_count = 0
            if self.__paramters['role']['hitpoint'] == 0:
                misc.post_event_gameover()

    def reset(self):
        self.index = 0
        self.image = self.master_image.subsurface((0,0,self.master_image_w,self.master_image_h))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [self.screen.get_width() / 2 - self.rect.width / 2, self.screen.get_height() * 0.7 - self.rect.height]

        self.__paramters['role']['hitpoint'] = 6
        self.__paramters['role']['speed'] = 2
        self.speed = [0, 0]
        self.towardright = True
        self.score = 0
        self.action_update_ts = 0
        self.keepmove = False
        self.life_protect_ts = 0
        self.is_hurt = False
        self.hurt_display_count = 0

    def getCurrentPos(self):
        return [self.cx, self.cy]

    def set_move_right(self):
        self.__move_to_x = 1
        self.__keyboard_move = True
    def set_move_left(self):
        self.__move_to_x = -1
        self.__keyboard_move = True
    def set_move_right_left_stop(self):
        self.__move_to_x = 0
        if self.__move_to_y == 0:
            self.__keyboard_move = False
    def set_move_up(self):
        self.__move_to_y = -1
        self.__keyboard_move = True
    def set_move_down(self):
        self.__move_to_y = 1
        self.__keyboard_move = True
    def set_move_up_down_stop(self):
        self.__move_to_y = 0
        if self.__move_to_x == 0:
            self.__keyboard_move = False

    def set_mouse_target(self, target:tuple):
        self.__mouse_target = target
    def set_mouse_move_start(self):
        self.__mouse_move = True
    def set_mouse_move_stop(self):
        self.__mouse_move = False

    def move_status_clear(self):
        self.__mouse_move = False
        self.__move_to_x = 0
        self.__move_to_y = 0
        self.__keyboard_move = False

    def add_experience(self):
        self.__experience += 1
        if self.__experience <= 10:
            pass
        elif self.__experience <= 30:
            if self.__level == 1:
                self.__level = 2
                misc.post_event_role_upgrade()
        elif self.__experience <= 70:
            if self.__level == 2:
                self.__level = 3
                misc.post_event_role_upgrade()
        elif self.__experience <= 130:
            if self.__level == 3:
                self.__level = 4
                misc.post_event_role_upgrade()
        elif self.__experience <= 210:
            if self.__level == 4:
                self.__level = 5
                misc.post_event_role_upgrade()
    def get_level(self):
        return self.__level
    def getClosedDistance(self):
        return self.__paramters['role']['expcloseddistance']

def main():
    pass

if __name__ == '__main__':
    main()
