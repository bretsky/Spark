import pygame
from pygame.locals import *
import sys
import random
pygame.init()
lazy_frog_animation = []
for i in range(32):
	lazy_frog = pygame.image.load('images/intro/lazy_frog/lazy_frog (%(number)i).gif' % {'number' : i+1})
	lazy_frog_animation.append(lazy_frog)
spark_animation = []
for i in range(96):
	spark = pygame.image.load('images/intro/spark/spark (%(number)i).gif' % {'number' : i+1})
	spark_animation.append(spark)

resolution_list = [(1280, 720), (1366, 768), (1600, 900), (1920, 1080)]
resolution = random.choice(resolution_list)
screen_x = resolution[0]
screen_y = resolution[1]
icon = pygame.image.load('images/spark_icon.gif')
pygame.display.set_icon(icon)
pygame.mixer.music.set_volume(1)
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Spark")
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)
VeraMono = pygame.font.Font('fonts/VeraMono.ttf', 32)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
framerate = pygame.time.Clock()
index = 0
volume = 1.000
sound_volume = 1.000

def splash():
	splash_go = True
	pygame.mixer.music.load('sounds/frog.mp3')
	pygame.mixer.music.play()
	pygame.mixer.music.set_volume(volume)
	for x in range(32):
		if splash_go == True:
			framerate.tick(6)
			screen.blit(background, (0,0))
			screen.blit(lazy_frog_animation[x], (center_screen(lazy_frog_animation[x].get_width(),'x'), center_screen (lazy_frog_animation[x].get_height(), 'y')))
			events = pygame.event.get()		
			pygame.display.update()
			splash_go = escape_check(events)
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
	pygame.mixer.music.set_volume(volume)
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
	if not pygame.mixer.music.get_busy():
		pygame.mixer.music.load('sounds/intro.mp3')
		pygame.mixer.music.play(-1)
		pygame.mixer.music.set_volume(volume)
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
	dropdown_menu_open = False
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
	back_button = pygame.image.load('images/back_button.gif')
	back_button = back_button.convert()
	back_button_pressed = pygame.image.load('images/back_button_pressed.gif')
	back_button_pressed = back_button_pressed.convert()
	back_button_rect = pygame.Rect(button_center_width, volume_button_rect.bottom + 6, 738, 58)
	menu_title = pygame.image.load('images/spark_text.gif')
	menu_title = menu_title.convert()
	while options_go == True:
		button_number = 0
		flag_list = []
		flag_list.append(screen.get_flags())
		flags = screen.get_flags()
		framerate.tick(60)
		screen.blit(background, (0,0))
		screen.blit(menu_title, (center_screen(menu_title.get_width(), 'x'), (screen.get_height())/4 - menu_title.get_height()/2-60))
		screen.blit(resolution_button, (resolution_button_rect.x, resolution_button_rect.y))
		if FULLSCREEN in flag_list:
			screen.blit(windowed_button, (windowed_button_rect.x, windowed_button_rect.y))
		else: 
			screen.blit(fullscreen_button, (fullscreen_button_rect.x, fullscreen_button_rect.y))
		screen.blit(volume_button, (volume_button_rect.x, volume_button_rect.y))
		screen.blit(back_button, (back_button_rect.x, back_button_rect.y))
		if dropdown_menu_open:	
			screen.blit(resolution_button_pressed, (resolution_button_rect.x, resolution_button_rect.y))
			for x in resolution_list:
				screen.blit(dropdown, (center_screen(dropdown.get_width(), 'x'), resolution_button_rect.bottom + button_number*dropdown.get_height()))
				text = pygame.font.Font.render(VeraMono, 'x'.join(map(str, resolution_list[button_number])), False, (255, 255, 255))
				print('x'.join(map(str, resolution_list[button_number])))
				button_number += 1
		else:
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
				if back_button_rect.collidepoint(position):
					screen.blit(back_button_pressed, (back_button_rect.x, back_button_rect.y))
		events = pygame.event.get()		
		for event in events:
			if event.type == MOUSEBUTTONUP and event.button == 1:
				position = pygame.mouse.get_pos()
				if resolution_button_rect.collidepoint(position):
					if not dropdown_menu_open:
						dropdown_menu_open = True
						button_number = 0
					elif dropdown_menu_open:
						dropdown_menu_open = False
				if not dropdown_menu_open:
					if fullscreen_button_rect.collidepoint(position):
						pygame.display.set_mode((screen_x,screen_y),flags^FULLSCREEN)
					if volume_button_rect.collidepoint(position):
						volume_options()
					if back_button_rect.collidepoint(position):
						menu()
		pygame.display.update()
		options_go = quit_check(events)
		
def volume_options():
	volume_options_go = True
	global sound_volume
	global volume
	click_music = False
	click_sound = False
	menu_title = pygame.image.load('images/spark_text.gif')
	menu_title = menu_title.convert()
	button_center_width = (screen.get_width()-738)/2
	button_center_height = (screen.get_height()-280)/2+15
	music_text = pygame.font.Font.render(VeraMono, 'Music:', False, (255, 255, 255))
	music_rect = pygame.Rect(center_screen(738, 'x'), button_center_height, music_text.get_width(), music_text.get_height())
	music_bar = pygame.image.load('images/volume_bar.gif')
	music_bar_rect = pygame.Rect(music_rect.left, music_rect.bottom + 6, music_bar.get_width(), music_bar.get_height())
	sound_text = pygame.font.Font.render(VeraMono, 'Sound:', False, (255, 255, 255))
	sound_rect = pygame.Rect(center_screen(738, 'x'), music_bar_rect.bottom + 6, sound_text.get_width(), sound_text.get_height())
	music_bar = music_bar.convert()
	slider_button = pygame.image.load('images/slider_button.gif')
	slider_button = slider_button.convert()
	slider_button_rect = pygame.Rect(music_bar_rect.left + round(pygame.mixer.music.get_volume()*715), music_rect.bottom + 6, 24, 40)
	slider_button_rect2 = pygame.Rect(music_bar_rect.left + round(sound_volume*715), sound_rect.bottom + 6, 24, 40)
	slider_button_pressed = pygame.image.load('images/slider_button_pressed.gif')
	slider_button_pressed = slider_button_pressed.convert()
	sound_bar = pygame.image.load('images/volume_bar.gif')
	sound_bar = sound_bar.convert()
	sound_bar_rect = pygame.Rect(sound_rect.left, sound_rect.bottom + 6, sound_bar.get_width(), sound_bar.get_height())
	back_button = pygame.image.load('images/back_button.gif')
	back_button = back_button.convert()
	back_button_rect = pygame.Rect(center_screen(738, 'x'), sound_bar_rect.bottom + 12, back_button.get_width(), back_button.get_height())
	back_button_pressed = pygame.image.load('images/back_button_pressed.gif')
	back_button_pressed = back_button_pressed.convert()
	while volume_options_go == True:
		framerate.tick(60)
		screen.blit(background, (0,0))		
		screen.blit(menu_title, (center_screen(menu_title.get_width(), 'x'), (screen.get_height())/4 - menu_title.get_height()/2-60))
		screen.blit(music_text, (center_screen(music_bar.get_width(), 'x' ), button_center_height))
		screen.blit(music_bar, (music_bar_rect.x, music_bar_rect.y))
		screen.blit(sound_text, (sound_rect.x, sound_rect.y))
		screen.blit(sound_bar, (sound_bar_rect.x, sound_bar_rect.y))
		screen.blit(back_button, (back_button_rect.x, back_button_rect.y))
		if pygame.mouse.get_pressed()[0]:
			position = pygame.mouse.get_pos()[0]-12
			if click_music == True:
				if position < 0 + music_bar_rect.x:
					position = 0
				elif position > 715 + music_bar_rect.x:
					position = 715
				else:
					position = position - music_bar_rect.x
				volume = position / 715.000
				screen.blit(slider_button_pressed, (position+music_bar_rect.x, slider_button_rect.y))
			else:
				screen.blit(slider_button, (music_bar_rect.x + volume*715, slider_button_rect.y))
		else:
			screen.blit(slider_button, (music_bar_rect.x + volume*715, slider_button_rect.y))
		if pygame.mouse.get_pressed()[0]:
			position = pygame.mouse.get_pos()[0]-12
			if click_sound == True:
				if position < 0 + sound_bar_rect.x:
					position = 0
				elif position > 715 + sound_bar_rect.x:
					position = 715
				else:
					position = position - sound_bar_rect.x
				sound_volume = position / 715.000
				screen.blit(slider_button_pressed, (position+sound_bar_rect.x, slider_button_rect2.y))
			else:
				screen.blit(slider_button, (sound_bar_rect.x + sound_volume*715, slider_button_rect2.y))
			if back_button_rect.collidepoint(pygame.mouse.get_pos()):
				screen.blit(back_button_pressed, (back_button_rect.x, back_button_rect.y))
		else:
			screen.blit(slider_button, (sound_bar_rect.x + sound_volume*715, slider_button_rect2.y))
		events = pygame.event.get()		
		for event in events:
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				position = pygame.mouse.get_pos()
				if music_bar_rect.collidepoint(position):
					click_music = True
				if sound_bar_rect.collidepoint(position):
					click_sound = True
			if event.type == MOUSEBUTTONUP and event.button == 1:
				if click_music:
					pygame.mixer.music.set_volume(volume)
					click_music = False
				if click_sound:
					click_sound = False
				if back_button_rect.collidepoint(pygame.mouse.get_pos()):
					options()
		pygame.display.update()
		menu_go = quit_check(events)
	
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