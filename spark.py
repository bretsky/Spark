import pygame
from pygame.locals import *
pygame.init()

spark_animation = []
for i in range(96):
	spark = pygame.image.load('intro\spark (%(number)i).gif' % {'number' : i+1})
	spark_animation.append(spark)
screen_x = 1280
screen_y = 720
icon = pygame.image.load('spark_icon.gif')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Spark")
SONG_END = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(SONG_END)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
framerate = pygame.time.Clock()
index = 0

def intro():
	intro_go = True
	pygame.mixer.music.load('sweep.mp3')
	pygame.mixer.music.play(-1)
	for x in range (96):
		if intro_go == True:
			framerate.tick(24)
			screen.blit(background, (0,0))
			screen.blit(spark_animation[x], (center(512,'x'), center (96, 'y')))
			pygame.display.update()
			intro_go = quit_check()
	pygame.mixer.music.stop()
		
def menu():
	menu_go = True
	pygame.mixer.music.load('intro.mp3')
	pygame.mixer.music.play(-1)
	menu_background = pygame.image.load('menu_background.gif')
	menu_background = menu_background.convert()
	menu_title = pygame.image.load('spark_text.gif')
	menu_title = menu_title.convert()
	newgame_button = pygame.image.load('newgame_button.gif')
	newgame_button = newgame_button.convert()
	continue_button = pygame.image.load('continue_button.gif')
	continue_button = continue_button.convert()
	options_button = pygame.image.load('options_button.gif')
	options_button = options_button.convert()
	exit_button = pygame.image.load('exit_button.gif')
	exit_button = exit_button.convert()
	while menu_go == True:
		framerate.tick(24)
		screen.blit(background, (0,0))
		screen.blit(menu_background, (center(menu_background.get_width(), 'x'), center(menu_background.get_height(), 'y')))
		screen.blit(menu_title, (center(menu_title.get_width(), 'x'), (screen.get_height() - 280)/4 - menu_title.get_height()/2))
		screen.blit(newgame_button, (center(newgame_button.get_width(),'x'), center(menu_background.get_height(), 'y')+15))
		screen.blit(continue_button, (center(continue_button.get_width(),'x'), center(menu_background.get_height(), 'y')+79))
		screen.blit(options_button, (center(options_button.get_width(),'x'), center(menu_background.get_height(), 'y')+143))
		screen.blit(exit_button, (center(exit_button.get_width(),'x'), center(menu_background.get_height(), 'y')+207))
		
		pygame.display.update()
		menu_go = quit_check()
	pygame.mixer.music.stop()

def center(x, dimension):
	center_x = 0
	if dimension == 'x':
		center_x = (screen.get_width() - x)/2
	if dimension == 'y':
		center_x = (screen.get_height() - x)/2
	return center_x


def quit_check():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return False
	else:
		return True


intro()
menu()