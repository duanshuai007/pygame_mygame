import pygame
import random
from pygame.color import THECOLORS
import time
import sys

FONT_FILE = "simhei.ttf"
FONT_SIZE_LARGE		= 120
FONT_SIZE_MIDDLE	= 80
FONT_SIZE_SMALL		= 40

GAME_OVER			= 0
#GAME_RESET			= 1

def pause(screen, clock):
    largeText = pygame.font.Font(FONT_FILE, FONT_SIZE_LARGE)
    TextSurf = largeText.render("Pause", True, (140,140,140))
    TextRect = TextSurf.get_rect()
    TextRect.center = ((screen.get_width() / 2), (screen.get_height() / 2))
    screen.blit(TextSurf, TextRect)
    pygame.display.flip()

    exit = False
    while exit is False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                exit = True
                break

        clock.tick(30)
##  gameDisplay.fill(white)
#button("Continue", 150, 450, 100, 50, green, bright_green,game_loop)
#       button("Quit",550, 450, 100, 50, red, bright_red,quitgame)
        pygame.display.update()
		#if exit is True:
		#    break

gameover_exit_f = False
game_continue_f = False

def gameover(screen, clock):
	global gameover_exit_f
	global game_continue_f
	largeText = pygame.font.Font(FONT_FILE, FONT_SIZE_LARGE)
	TextSurf = largeText.render("你死了", True, THECOLORS['red'])
	TextRect = TextSurf.get_rect()
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
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				gameover_exit_f = True
				break

		clock.tick(30)
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



def life_display_update(screen, life_number):
	img = pygame.image.load("hero_life.png").convert()
	img = pygame.transform.scale(img, (30,30))
	img.set_colorkey((0,0,0))
	rect = img.get_rect()
	for i in range(0,life_number):
		screen.blit(img, (20 + (i * (rect.width + 5)), 60))



