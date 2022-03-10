import pygame
import random
from pygame.color import THECOLORS
import time
import sys
import math

FONT_FILE = "simhei.ttf"
FONT_SIZE_LARGE		= 120
FONT_SIZE_MIDDLE	= 80
FONT_SIZE_SMALL		= 40

GAME_OVER			= 0
#GAME_RESET			= 1

def calc_angle(cur_x:int, cur_y:int, tar_x:int, tar_y:int)->float:
    delta_x = tar_x - cur_x
    delta_y = tar_y - cur_y
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def calc_angle_speed(angle):
    vel_x = math.cos(math.radians(angle))
    vel_y = math.sin(math.radians(angle))
    return [vel_x,vel_y]
    
def get_point_distance(a:tuple, b:tuple):
    x = abs(a[0] - b[0])
    y = abs(a[1] - b[1])
    return math.sqrt(x*x + y*y)
    
last_pause_ts = 0
def pause():
    global last_pause_ts
    curr_ts = time.time() * 1000
    if curr_ts - last_pause_ts > 200:
        last_pause_ts = curr_ts
        largeText = pygame.font.Font(FONT_FILE, FONT_SIZE_LARGE)
        TextSurf = largeText.render("Pause", True, (140,140,140))
        TextRect = TextSurf.get_rect()
        screen = pygame.display.get_surface()
        TextRect.center = ((screen.get_width() / 2), (screen.get_height() / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.flip()
        exit = False
        while exit is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        curr_ts = time.time() * 1000
                        if curr_ts - last_pause_ts > 200:
                            last_pause_ts = curr_ts
                            exit = True
                            break

            pygame.time.wait(30)
            pygame.display.update()
        
def game_success():
    largeText = pygame.font.Font(FONT_FILE, FONT_SIZE_LARGE)
    TextSurf = largeText.render("YOU WIN", True, THECOLORS['red'])
    tishi1 = pygame.font.Font(FONT_FILE, FONT_SIZE_SMALL)
    tishi1_surface = tishi1.render("Press [Enter] Start a new game", True, THECOLORS['white'])
    tishi2 = pygame.font.Font(FONT_FILE, FONT_SIZE_SMALL)
    tishi2_surface = tishi2.render("Press [Exc] exit game", True, THECOLORS['white'])
    screen = pygame.display.get_surface()
    TextRect = TextSurf.get_rect()
    TextRect.center = ((screen.get_width() / 2), (screen.get_height() / 2 - 80))
    screen.blit(TextSurf, TextRect)

    tishi1_rect = tishi1_surface.get_rect()
    tishi1_rect.center = ((screen.get_width() / 2), (screen.get_height() / 2 + 40))
    screen.blit(tishi1_surface, tishi1_rect)

    tishi2_rect = tishi2_surface.get_rect()
    tishi2_rect.center = ((screen.get_width() / 2), (screen.get_height() / 2 + 120))
    screen.blit(tishi2_surface, tishi2_rect)

    pygame.display.flip()

    exit = False
    is_continue_game = False
    while exit is False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    is_continue_game = True
                    exit = True
                    break
                elif event.key == pygame.K_ESCAPE:
                    is_continue_game = False
                    exit = True
                    break
            elif event.type == pygame.QUIT:
                pygame.quit()
        pygame.time.wait(30)
        pygame.display.update()
    return is_continue_game

gameover_exit_f = False
game_continue_f = False

def gameover():
    global gameover_exit_f
    global game_continue_f
    largeText = pygame.font.Font(FONT_FILE, FONT_SIZE_LARGE)
    TextSurf = largeText.render("你死了", True, THECOLORS['red'])
    TextRect = TextSurf.get_rect()
    screen = pygame.display.get_surface()
    TextRect.center = ((screen.get_width() / 2), (screen.get_height() / 2))
    screen.blit(TextSurf, TextRect)
    pygame.display.flip()

    button_width = 120
    button_height = 50
    w = screen.get_width() 
    h = screen.get_height()
    bl = w / 3 - (button_width / 2)
    br = w / 3 * 2 - (button_width / 2)
    btop = h * 0.7

    game_continue_f = False
    gameover_exit_f = False
    while gameover_exit_f is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameover_exit_f = True
                    break
        #clock.tick(30)
        pygame.time.wait(30)
        button(screen, "继续", bl, btop, button_width, button_height, THECOLORS['green'], THECOLORS['lightgreen'], game_reset)
        button(screen, "退出", br, btop, button_width, button_height, THECOLORS['red'], THECOLORS['indianred1'], game_quit)
        pygame.display.update()
    return game_continue_f

def button(screen, msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        click = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
            print(click)
    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
    smallText = pygame.font.Font(FONT_FILE, FONT_SIZE_SMALL)
    textSurf = smallText.render(msg, True, THECOLORS['black'])
    textRect = textSurf.get_rect()
    textRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)

def game_quit():
    global gameover_exit_f
    gameover_exit_f = True

def game_reset():
    global gameover_exit_f
    global game_continue_f
    gameover_exit_f = True
    game_continue_f = True

def post_event_gameover():
    e = pygame.event.Event(pygame.USEREVENT, attr=GAME_OVER)
    pygame.event.post(e)

def life_display_update(life_number):
    img = pygame.image.load("hero_life.png").convert()
    img = pygame.transform.scale(img, (30,30))
    img.set_colorkey((0,0,0))
    rect = img.get_rect()
    screen = pygame.display.get_surface()
    for i in range(0,life_number):
        screen.blit(img, (20 + (i * (rect.width + 5)), 60))



