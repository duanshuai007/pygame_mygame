import pygame
import random 
from pygame.color import THECOLORS

class fireball(pygame.sprite.Sprite):
    name = ""
    screen = None
    def __init__(self, image_file, name, screen):
        self._layer = 1
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0,0]
        self.speed = [0, 0]
        self.name = name
        self.screen = screen

    def fly(self, start_location, speed):
        self.rect.left = start_location[0]
        self.rect.top = start_location[1]
        self.speed[0] = speed
    
    def move(self):
        self.rect = self.rect.move(self.speed)
#        if self.rect.left > (self.screen.get_width() - self.rect.width):
#            fkgroup.remove(self)
#            #del self
#            self.kill()
#        elif self.rect.left < (0 - self.rect.width):
#            fkgroup.remove(self)
#            self.kill()
    def rotate(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = self.rect.center)
 

def main():
	pass

if __name__ == '__main__':
	main()
