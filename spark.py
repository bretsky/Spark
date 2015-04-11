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

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
framerate = pygame.time.Clock()
index = 0

def intro():
	intro_go = True
	for x in range (96):
		if intro_go == True:
			framerate.tick(24)
			screen.blit(background, (0,0))
			screen.blit(spark_animation[x], (center(512, 96)))
			pygame.display.update()
			intro_go = quit_check()
		
def menu():
	menu_go = True
	menu_background = pygame.image.load('menu_background.gif')
	menu_background = menu_background.convert()
	menu_title = pygame.image.load('spark_text.gif')
	menu_title = menu_title.convert()
	while menu_go == True:
		framerate.tick(24)
		screen.blit(background, (0,0))
		screen.blit(menu_background, (center(menu_background.get_width(), menu_background.get_height())))
		title_position = int((screen.get_width()-menu_title.get_width())/2)
		screen.blit(menu_title, (title_position, 150))
		pygame.display.update()
		menu_go = quit_check()


def center(x, y):
	center_x = (screen.get_width() - x)/2
	center_y = (screen.get_height() - y)/2
	return (center_x, center_y)


def quit_check():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return False
	else:
		return True


intro()
menu()