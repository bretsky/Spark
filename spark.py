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
screen_x = 640
screen_y = 480
icon = pygame.image.load('images/spark_icon.gif')
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
 

def splash():
	splash_go = True
	pygame.mixer.music.load('sounds/frog.mp3')
	pygame.mixer.music.play()
	for x in range(32):
		if splash_go == True:
			framerate.tick(6)
			screen.blit(background, (0,0))
			screen.blit(lazy_frog_animation[x], (center_screen(lazy_frog_animation[x].get_width(),'x'), center_screen (lazy_frog_animation[x].get_height(), 'y')))
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
			screen.blit(presents, (center_screen(presents.get_width(), 'x'), center_screen(presents.get_height(), 'y')))
			events = pygame.event.get()		
			pygame.display.update()
			splash_go = escape_check(events)

	for x in range(32):
		if splash_go == True:
			framerate.tick(16)
			screen.blit(background, (0,0))
			presents = pygame.font.Font.render(VeraMono, 'Presents...',  False, (255-x*8, 255-x*8, 255-x*8))
			screen.blit(presents, (center_screen(presents.get_width(), 'x'), center_screen(presents.get_height(), 'y')))
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
			screen.blit(spark_animation[x], (center_screen(512,'x'), center_screen (96, 'y')))
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
	button_center_width = (screen.get_width()-738)/2
	button_center_height = (screen.get_height()-280)/2+15
	newgame_button_rect = pygame.Rect(button_center_width, button_center_height, 738, 58)
	continue_button_rect = pygame.Rect(button_center_width, newgame_button_rect.bottom+6, 738, 58)
	options_button_rect = pygame.Rect(button_center_width, continue_button_rect.bottom+6, 738, 58)
	exit_button_rect = pygame.Rect(button_center_width, options_button_rect.bottom+6, 738, 58)
	while menu_go == True:
		framerate.tick(60)
		screen.blit(background, (0,0))
		screen.blit(menu_background, (center_screen(menu_background.get_width(), 'x'), center_screen(menu_background.get_height(), 'y')))

		screen.blit(menu_title, (center_screen(menu_title.get_width(), 'x'), (screen.get_height())/4 - menu_title.get_height()/2-60))
		
		screen.blit(newgame_button,(button_center_width, button_center_height))
		
		screen.blit(continue_button,(button_center_width, newgame_button_rect.bottom+6) )
		
		screen.blit(options_button,(button_center_width, continue_button_rect.bottom+6) )
		
		screen.blit(exit_button,(button_center_width, options_button_rect.bottom+6) )
		events = pygame.event.get()		
		if pygame.mouse.get_pressed()[0]:
			position = pygame.mouse.get_pos()
			if newgame_button_rect.collidepoint(position):
				screen.blit(newgame_button_pressed, (newgame_button_rect.x, newgame_button_rect.y))
			if continue_button_rect.collidepoint(position):
				screen.blit(continue_button_pressed, (continue_button_rect.x, continue_button_rect.y))
			if options_button_rect.collidepoint(position):
				screen.blit(options_button_pressed, (options_button_rect.x, options_button_rect.y))
			if exit_button_rect.collidepoint(position):
				screen.blit(exit_button_pressed, (exit_button_rect.x, exit_button_rect.y))
		for event in events:
			if event.type == MOUSEBUTTONUP and event.button == 1:
				position = pygame.mouse.get_pos()
				if newgame_button_rect.collidepoint(position):
					pass
				if continue_button_rect.collidepoint(position):
					pass
				if options_button_rect.collidepoint(position):
					options()
				if exit_button_rect.collidepoint(position):
					sys.exit(0)

		pygame.display.update()
		menu_go = escape_check(events)
	pygame.mixer.music.stop()

def options():
	options_go = True
	button_center_width = (screen.get_width()-738)/2
	button_center_height = (screen.get_height()-280)/2+15
	dropdown = pygame.image.load('images/dropdown.gif')
	dropdown = dropdown.convert()
	resolution_button = pygame.image.load('images/resolution_button.gif')
	resolution_button = resolution_button.convert()
	resolution_button_pressed = pygame.image.load('images/resolution_button_pressed.gif')
	resolution_button_pressed = resolution_button_pressed.convert()
	resolution_button_rect = pygame.Rect(button_center_width, button_center_height, 738, 58)
	fullscreen_button = pygame.image.load('images/fullscreen_button.gif')
	fullscreen_button = fullscreen_button.convert()
	fullscreen_button_pressed = pygame.image.load('images/fullscreen_button_pressed.gif')
	fullscreen_button_pressed = fullscreen_button_pressed.convert()
	fullscreen_button_rect = pygame.Rect(button_center_width, resolution_button_rect.bottom + 6, 738, 58)

	windowed_button = pygame.image.load('images/windowed_button.gif')
	windowed_button = windowed_button.convert()
	windowed_button_pressed = pygame.image.load('images/windowed_button_pressed.gif')
	windowed_button_pressed = windowed_button_pressed.convert()
	windowed_button_rect = pygame.Rect(button_center_width, resolution_button_rect.bottom + 6, 738, 58)
	volume_button = pygame.image.load('images/volume_button.gif')
	volume_button = volume_button.convert()
	volume_button_pressed = pygame.image.load('images/volume_button_pressed.gif')
	volume_button_pressed = volume_button_pressed.convert()
	volume_button_rect = pygame.Rect(button_center_width, windowed_button_rect.bottom + 6, 738, 58)
	menu_title = pygame.image.load('images/spark_text.gif')
	menu_title = menu_title.convert()
	while options_go == True:
		flag_list = []
		flag_list.append(screen.get_flags())
		flags = screen.get_flags()
		framerate.tick(60)
		screen.blit(background, (0,0))
		screen.blit(menu_title, (center_screen(menu_title.get_width(), 'x'), (screen.get_height())/4 - menu_title.get_height()/2-60))
		screen.blit(resolution_button, (center_screen(resolution_button.get_width(), 'x'), button_center_height))
		if FULLSCREEN in flag_list:
			screen.blit(windowed_button, (center_screen(windowed_button.get_width(), 'x'), resolution_button_rect.bottom + 6))
		else: 
			screen.blit(fullscreen_button, (center_screen(fullscreen_button.get_width(), 'x'), resolution_button_rect.bottom + 6))
		screen.blit(volume_button, (center_screen(volume_button.get_width(), 'x'), fullscreen_button_rect.bottom + 6))
		events = pygame.event.get()		
		if pygame.mouse.get_pressed()[0]:
			position = pygame.mouse.get_pos()
			if resolution_button_rect.collidepoint(position):
				screen.blit(resolution_button_pressed, (resolution_button_rect.x, resolution_button_rect.y))
			if fullscreen_button_rect.collidepoint(position):
				if FULLSCREEN in flag_list:
					screen.blit(windowed_button_pressed, (fullscreen_button_rect.x, fullscreen_button_rect.y))
				else: 
					screen.blit(fullscreen_button_pressed, (fullscreen_button_rect.x, fullscreen_button_rect.y))	
			if volume_button_rect.collidepoint(position):
				screen.blit(volume_button_pressed, (volume_button_rect.x, volume_button_rect.y))

		for event in events:

			if event.type == MOUSEBUTTONUP and event.button == 1:
				position = pygame.mouse.get_pos()
				if resolution_button_rect.collidepoint(position):
					pass
				if fullscreen_button_rect.collidepoint(position):
					pygame.display.set_mode((screen_x,screen_y),flags^FULLSCREEN)


		pygame.display.update()
		options_go = quit_check(events)
		
	
	
def center_screen(x, dimension):
	center = 0
	if dimension == 'x':
		center = (screen.get_width() - x)/2
	if dimension == 'y':
		center = (screen.get_height() - x)/2
	return center

def center(small_dimension, large_dimension):
	return (large_dimension - small_dimension)/2


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

def game():
	splash()
	intro()
	menu()

game()