import pygame
from pygame.locals import *
import sys
pygame.init()
lazy_frog_animation = []
for i in range(32):
	lazy_frog = pygame.image.load('images/intro/lazy_frog/lazy_frog (%(number)i).gif' % {'number' : i+1})
	lazy_frog_animation.append(lazy_frog)
spark_animation = []
for i in range(96):
	spark = pygame.image.load('images/intro/spark/spark (%(number)i).gif' % {'number' : i+1})
	spark_animation.append(spark)
screen_x = 1920
screen_y = 1080
icon = pygame.image.load('images/spark_icon.gif')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((screen_x, screen_y), FULLSCREEN)
pygame.display.set_caption("Spark")
SONG_END = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(SONG_END)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
framerate = pygame.time.Clock()
index = 0
 

def splash():
	splash_go = True
	for x in range(32):
		if splash_go == True:
			framerate.tick(6)
			screen.blit(background, (0,0))
			screen.blit(lazy_frog_animation[x], (center(lazy_frog_animation[x].get_width(),'x'), center (lazy_frog_animation[x].get_height(), 'y')))
			events = pygame.event.get()		
			pygame.display.update()
			splash_go = escape_check(events)
	VeraMono = pygame.font.Font('fonts/VeraMono.ttf', 32)
	presents = pygame.font.Font.render(VeraMono, 'Presents',  False, (255, 255, 255))
	for x in range(32):
		if splash_go == True:
			framerate.tick(16)
			screen.blit(background, (0,0))
			presents = pygame.font.Font.render(VeraMono, 'Presents...',  False, (x*8, x*8, x*8))
			screen.blit(presents, (center(presents.get_width(), 'x'), center(presents.get_height(), 'y')))
			events = pygame.event.get()		
			pygame.display.update()
			splash_go = escape_check(events)



def intro():
	intro_go = True
	pygame.mixer.music.load('sounds/sweep.mp3')
	pygame.mixer.music.play(-1)
	for x in range (96):
		if intro_go == True:
			framerate.tick(24)
			screen.blit(background, (0,0))
			screen.blit(spark_animation[x], (center(512,'x'), center (96, 'y')))
			events = pygame.event.get()		
			pygame.display.update()
			intro_go = escape_check(events)
	pygame.mixer.music.stop()
		
def menu():
	menu_go = True
	pygame.mixer.music.load('sounds/intro.mp3')
	pygame.mixer.music.play(-1)
	menu_background = pygame.image.load('images/menu_background.gif')
	menu_background = menu_background.convert()
	menu_title = pygame.image.load('images/spark_text.gif')
	menu_title = menu_title.convert()
	newgame_button = pygame.image.load('images/newgame_button.gif')
	newgame_button = newgame_button.convert()
	newgame_button_pressed = pygame.image.load('images/newgame_button_pressed.gif')
	newgame_button_pressed = newgame_button_pressed.convert()
	continue_button = pygame.image.load('images/continue_button.gif')
	continue_button = continue_button.convert()
	continue_button_pressed = pygame.image.load('images/continue_button_pressed.gif')
	continue_button_pressed = continue_button_pressed.convert()
	options_button = pygame.image.load('images/options_button.gif')
	options_button = options_button.convert()
	options_button_pressed = pygame.image.load('images/options_button_pressed.gif')
	options_button_pressed = options_button_pressed.convert()
	exit_button = pygame.image.load('images/exit_button.gif')
	exit_button = exit_button.convert()
	exit_button_pressed = pygame.image.load('images/exit_button_pressed.gif')
	exit_button_pressed = exit_button_pressed.convert()
	while menu_go == True:
		framerate.tick(60)
		screen.blit(background, (0,0))
		button_center_width = center(newgame_button.get_width(), 'x')
		button_center_height = center(menu_background.get_height(), 'y')
		screen.blit(menu_background, (center(menu_background.get_width(), 'x'), center(menu_background.get_height(), 'y')))
		screen.blit(menu_title, (center(menu_title.get_width(), 'x'), (screen.get_height() - 280)/4 - menu_title.get_height()/2))
		newgame_button_rect = pygame.Rect(button_center_width, button_center_height+15, 738, 58)
		screen.blit(newgame_button,(button_center_width, button_center_height+15) )
		continue_button_rect = pygame.Rect(button_center_width, button_center_height+79, 738, 58)
		screen.blit(continue_button,(button_center_width, button_center_height+79) )
		options_button_rect = pygame.Rect(button_center_width, button_center_height+143, 738, 58)
		screen.blit(options_button,(button_center_width, button_center_height+143) )
		exit_button_rect = pygame.Rect(button_center_width, button_center_height+207, 738, 58)
		screen.blit(exit_button,(button_center_width, button_center_height+207) )
		events = pygame.event.get()		
		if pygame.mouse.get_pressed()[0]:
			position = pygame.mouse.get_pos()
			if newgame_button_rect.collidepoint(position):
				screen.blit(newgame_button_pressed, (button_center_width, button_center_height+15))
			if continue_button_rect.collidepoint(position):
				screen.blit(continue_button_pressed, (button_center_width, button_center_height+79))
			if options_button_rect.collidepoint(position):
				screen.blit(options_button_pressed, (button_center_width, button_center_height+143))
			if exit_button_rect.collidepoint(position):
				screen.blit(exit_button_pressed, (button_center_width, button_center_height+207))

		pygame.display.update()
		menu_go = escape_check(events)
	pygame.mixer.music.stop()

def center(x, dimension):
	center_x = 0
	if dimension == 'x':
		center_x = (screen.get_width() - x)/2
	if dimension == 'y':
		center_x = (screen.get_height() - x)/2
	return center_x


def quit_check(events):
	for event in events:
		if event.type == pygame.QUIT:
			sys.exit(0)
	else:
		return True

def escape_check(events):
	for event in events:
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			sys.exit(0)
		if event.type == pygame.QUIT:
			sys.exit(0)
	else:
		return True

splash()
intro()
menu()