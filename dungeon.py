import random
import pygame
from pygame.locals import *
import sys
import time

geo_file = open(r'data\dungeon\geographical_features.txt')
dungeon_attr_file = open(r'data\dungeon\dungeon_attributes.txt')
dungeon_adj_file = open(r'data\dungeon\dungeon_adjectives.txt')
dungeon_word_file = open(r'data\dungeon\dungeon_words.txt')
geo_list = geo_file.read().splitlines()
dungeon_attr_list = dungeon_attr_file.read().splitlines()
dungeon_adj_list = dungeon_adj_file.read().splitlines()
dungeon_word_list = dungeon_word_file.read().splitlines()

def random_dungeon_name():
	num = random.randrange(0,5)
	if num == 0:
		dungeon_name = ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_word_list).split()) + ' ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(geo_list).split())
	elif num == 1:
		dungeon_name = 'The ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_adj_list).split()) + ' ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(geo_list).split())
	elif num == 2:
		dungeon_name = 'The ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(geo_list).split()) + ' of ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_attr_list).split())
	elif num == 3:
		dungeon_name = 'The ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_adj_list).split()) + ' ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(geo_list).split()) + ' of ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_attr_list).split())
	elif num == 4:
		dungeon_name = 'The ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(geo_list).split()) + ' of ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_adj_list).split()) + ' ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_attr_list).split())
	return dungeon_name

sys.setrecursionlimit(5000)

class Tile:
	def __init__(self, tile_type, water):
		self.type = tile_type
		self.water = water
		# self.light = 255
		self.light = 0
		self.visible = False
	def set_light(self, value):
		if value > self.light:
			self.light = value
	def set_visible(self, visible):
		self.visible = visible

character_pos = [0, 0]
map_list = [[Tile(0, False) for y in range(128)] for x in range(128)]
pygame.init()
screen_x = 896
screen_y = 896
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption(random_dungeon_name())
screen_bg = pygame.Surface((896, 896)).convert()
screen_bg.fill((0, 0, 0))
floor_tile = pygame.Surface((7, 7)).convert()
floor_tile.fill((30, 16, 3))
wall_tile = pygame.Surface((7, 7)).convert()
wall_tile.fill((63, 63, 63))
bg_tile = pygame.Surface((7, 7)).convert()
bg_tile.fill((70, 45, 10))
water_tile = pygame.Surface((7, 7)).convert()
water_tile.fill((16, 16, 160))
hall_tile = pygame.Surface((7, 7)).convert()
hall_tile.fill((148, 120, 78))
character_tile = pygame.Surface((7, 7)).convert()
character_tile.fill((255, 255, 255))
destination_tile = pygame.Surface((7, 7)).convert()
destination_tile.fill((255, 0, 0))
enemy_tile = pygame.Surface((7,7)).convert()
enemy_tile.fill((255, 255, 0))
start_tile = pygame.Surface((7, 7)).convert()
start_tile.fill((0, 255, 0))
dead_tile = pygame.Surface((7, 7)).convert()
dead_tile.fill((255, 128, 0))
health_pixel = pygame.Surface((1,3)).convert()
health_pixel.fill((255,0,0))
rooms = []
framerate = pygame.time.Clock()
dead_enemies = []
dead_enemy_locations = []
def print_map():
	print_go = True
	w_count = 0
	a_count = 0
	s_count = 0
	d_count = 0
	while print_go == True:	
		framerate.tick(60)
		counter = 0
		for y in map_list:
			x_counter = 0
			for x in y:
				if x.type == 0:
					screen.blit(bg_tile, (x_counter*7, counter*7))
				if x.type == 1 and x.water == False:
					screen.blit(floor_tile, (x_counter*7, counter*7))
				if x.type == 2:
					screen.blit(wall_tile, (x_counter*7, counter*7))
				if x.type == 3 and x.water  == False:
					screen.blit(hall_tile, (x_counter*7, counter*7))
				if x.water == True:
					screen.blit(water_tile, (x_counter*7, counter*7))
				x_counter+=1
			counter += 1
		screen.blit(character_tile, (character_pos[0]*7, character_pos[1]*7))
		pygame.display.update()
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					return
	return

def print_map_dots(fill_start, destination):
	print_go = True
	while print_go == True:
		framerate.tick(55)
		counter = 0	
		screen.blit(screen_bg, (0,0))
		for y in map_list:
			x_counter = 0
			for x in y:
				if x.type == 0:
					screen.blit(bg_tile, (x_counter*7, counter*7))
				if x.type == 1 and x.water == False:
					screen.blit(floor_tile, (x_counter*7, counter*7))
				if x.type == 2:
					screen.blit(wall_tile, (x_counter*7, counter*7))
				if x.type == 3 and x.water  == False:
					screen.blit(hall_tile, (x_counter*7, counter*7))
				if x.water == True:
					screen.blit(water_tile, (x_counter*7, counter*7))
				x_counter+=1
			counter += 1
		screen.blit(destination_tile, (destination[0]*7, destination[1]*7))
		screen.blit(start_tile, (fill_start[0]*7, fill_start[1]*7))
		pygame.display.update()
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					return
	return

def print_map_game(destination):
	print_go = True
	jumped_this_turn = False
	jump_wait_counter = 0
	enemy_wait = False
	character_health = 10
	max_character_health = 10
	regen_rate = 15
	regen_counter = 0
	# time.clock()
	# frame_counter = 0
	# seconds = 1
	while print_go == True:
		framerate.tick(30)
		# print(character_health)
		# print(framerate.get_fps())
		for y in map_list:
			for x in y:
				x.set_visible(False)
		# frame_counter += 1
		# if time.clock() >= seconds:
		# 	print(frame_counter)
		# 	frame_counter = 0
		# 	seconds += 1
		moved_this_turn = False
		if jumped_this_turn == True:
			jump_wait_counter += 1
			enemy_wait = True
			if jump_wait_counter == 7:
				enemy_wait = False
				print('Enemy moves')
			if jump_wait_counter >= 15:
				jumped_this_turn = False
				jump_wait_counter = 0
				print('Recovery Done')
			moved_this_turn = True
		else:
			enemy_wait = False
		counter = 0
		for room in rooms:
			if room.in_this_room(character_pos[0], character_pos[1]):
				if not room.discovered:
					room.discover()
					for room_y in range(room.height+3):
						for room_x in range(room.width+3):
							for y in range(11):
								for x in range(11):
									light_pos = [room_x-5+x+room.wall_left, room_y-5+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128: 
										map_list[light_pos[1]][light_pos[0]].set_light(15)
							for y in range(9):
								for x in range(9):
									light_pos = [room_x-4+x+room.wall_left, room_y-4+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128: 
										map_list[light_pos[1]][light_pos[0]].set_light(31)
							for y in range(7):
								for x in range(7):
									light_pos = [room_x-3+x+room.wall_left, room_y-3+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128: 
										map_list[light_pos[1]][light_pos[0]].set_light(63)
							for y in range(5):
								for x in range(5):
									light_pos = [room_x-2+x+room.wall_left, room_y-2+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128: 
										map_list[light_pos[1]][light_pos[0]].set_light(127)
							for y in range(3):
								for x in range(3):
									light_pos = [room_x-1+x+room.wall_left, room_y-1+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128: 
										map_list[light_pos[1]][light_pos[0]].set_light(255)						
							map_list[room_y+room.wall_top][room_x+room.wall_left].set_light(255)
		for y in range(13):
			for x in range(13):
				light_pos = [character_pos[0]-6+x, character_pos[1]-6+y]
				if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1: 
					map_list[light_pos[1]][light_pos[0]].set_light(15)
					map_list[light_pos[1]][light_pos[0]].set_visible(True)
		for y in range(11):
			for x in range(11):
				light_pos = [character_pos[0]-5+x, character_pos[1]-5+y]
				if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1:
					map_list[light_pos[1]][light_pos[0]].set_light(31)
		for y in range(9):
			for x in range(9):
				light_pos = [character_pos[0]-4+x, character_pos[1]-4+y]
				if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1:
					map_list[light_pos[1]][light_pos[0]].set_light(63)
		for y in range(7):
			for x in range(7):
				light_pos = [character_pos[0]-3+x, character_pos[1]-3+y]
				if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1:
					map_list[light_pos[1]][light_pos[0]].set_light(127)
		for y in range(5):
			for x in range(5):
				light_pos = [character_pos[0]-2+x, character_pos[1]-2+y]
				if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1:
					map_list[light_pos[1]][light_pos[0]].set_light(255)
		for y in range(3):
			for x in range(3):
				light_pos = [character_pos[0]-1+x, character_pos[1]-1+y]
				if light_pos[0] < 128 and light_pos[1] < 128: 
					map_list[light_pos[1]][light_pos[0]].set_light(255)		
		screen.blit(screen_bg, (0,0))
		for y in map_list:
			x_counter = 0
			for x in y:

				if x.type == 0:
					x_tile = bg_tile
					if x.visible:
						x_tile.set_alpha(x.light)
					else:
						x_tile.set_alpha(x.light/2)
					screen.blit(x_tile, (x_counter*7, counter*7))
				if x.type == 1 and x.water == False:
					x_tile = floor_tile
					if x.visible:
						x_tile.set_alpha(x.light)
					else:
						x_tile.set_alpha(x.light/2)
					screen.blit(x_tile, (x_counter*7, counter*7))
				if x.type == 2:
					x_tile = wall_tile
					if x.visible:
						x_tile.set_alpha(x.light)
					else:
						x_tile.set_alpha(x.light/2)
					screen.blit(x_tile, (x_counter*7, counter*7))
				if x.type == 3 and x.water  == False:
					x_tile = hall_tile
					if x.visible:
						x_tile.set_alpha(x.light)
					else:
						x_tile.set_alpha(x.light/2)
					screen.blit(x_tile, (x_counter*7, counter*7))
				x_counter+=1
			counter += 1
		x_tile = destination_tile
		if map_list[destination[1]][destination[0]].visible:
			x_tile.set_alpha(map_list[destination[1]][destination[0]].light)
		else:
			x_tile.set_alpha(map_list[destination[1]][destination[0]].light/2)
		screen.blit(x_tile, (destination[0]*7, destination[1]*7))
		screen.blit(character_tile, (character_pos[0]*7, character_pos[1]*7))
		for enemy in dead_enemy_locations:
			x_tile = dead_tile
			x_tile.set_alpha(min(map_list[enemy[1]][enemy[0]].light,255.0-(255.0*(dead_enemies[dead_enemy_locations.index(enemy)].turns_dead)/45.0)))
			if map_list[enemy[1]][enemy[0]].visible:
				screen.blit(x_tile, (enemy[0]*7, enemy[1]*7))
		for enemy in enemy_locations:				
			x_tile = enemy_tile
			x_tile.set_alpha(map_list[enemy[1]][enemy[0]].light)
			if map_list[enemy[1]][enemy[0]].visible:
				screen.blit(x_tile, (enemy[0]*7, enemy[1]*7))
		for pixel in range(round(screen_x*character_health/max_character_health)):
			screen.blit(health_pixel, (pixel, 0))
		pygame.display.update()
		if character_health <= 0:
			print('You Lose')
			return
		if character_pos == destination:
			print('You Win!')
			return
		for enemy in enemies:
			if not enemy.alive:
				dead_enemies.append(enemy)
				dead_enemy_locations.append(enemy_locations[enemies.index(enemy)])
				del enemy_locations[enemies.index(enemy)]
				del enemies[enemies.index(enemy)]
		for enemy in dead_enemies:
			enemy.turns_dead += 1
			if enemy.turns_dead >= 45:
				del dead_enemy_locations[dead_enemies.index(enemy)]
				del dead_enemies[dead_enemies.index(enemy)]
		events = pygame.event.get()
		key = pygame.key.get_pressed()
		move_speed = 1
		mods = pygame.key.get_mods()
		if mods & KMOD_SHIFT:
			move_speed = 2
		if not moved_this_turn:
			if key[pygame.K_w] or key[pygame.K_UP]:
				w_count += move_speed
				if w_count >= 10:
					w_count = 0
					if map_list[character_pos[1]-1][character_pos[0]].type != 2:
						if not [character_pos[0],character_pos[1]-1] in enemy_locations:
							w_count += 8
							character_pos[1] -= 1
							print('Moved')
							moved_this_turn = True
			else:
				w_count = 0
		if not moved_this_turn:
			if key[pygame.K_s] or key[pygame.K_DOWN]:
				s_count += move_speed
				if s_count >= 10:
					s_count = 0
					if map_list[character_pos[1]+1][character_pos[0]].type != 2:
						if not [character_pos[0],character_pos[1]+1] in enemy_locations:
							s_count += 8
							character_pos[1] += 1
							print('Moved')
							moved_this_turn = True
			else:
				s_count = 0
		if not moved_this_turn:
			if key[pygame.K_a] or key[pygame.K_LEFT]:
				a_count += move_speed
				if a_count >= 10:
					a_count = 0
					if map_list[character_pos[1]][character_pos[0]-1].type != 2:
						if not [character_pos[0]-1,character_pos[1]] in enemy_locations:
							a_count += 8
							character_pos[0] -= 1
							print('Moved')
							moved_this_turn = True
			else:
				a_count = 0
		if not moved_this_turn:
			if key[pygame.K_d] or key[pygame.K_RIGHT]:
				d_count += move_speed
				if d_count >= 10:
					d_count = 0
					if map_list[character_pos[1]][character_pos[0]+1].type != 2:
						if not [character_pos[0]+1,character_pos[1]] in enemy_locations:
							d_count += 8
							character_pos[0] += 1
							print('Moved')
							moved_this_turn = True
			else:
				d_count = 0
		for event in events:
			if event.type == pygame.QUIT:
				return
			if not moved_this_turn:
				if event.type == MOUSEBUTTONUP and event.button == 1:
					position = pygame.mouse.get_pos()
					position = [int(x/7) for x in position]
					print(position)
					if position in enemy_locations:
						if position[0] > character_pos[0]-2 and position[0] < character_pos[0]+2:
							if position[1] > character_pos[1]-2 and position[1] < character_pos[1]+2:
								enemies[enemy_locations.index(position)].damage(1)
								print('Attack successful')
								moved_this_turn = True

			if event.type == pygame.KEYDOWN:
				if not moved_this_turn:
					if event.key == pygame.K_w or event.key == pygame.K_UP:
						if map_list[character_pos[1]-move_speed][character_pos[0]].type != 2 and map_list[character_pos[1]-1][character_pos[0]].type != 2:
							if not [character_pos[0],character_pos[1]-move_speed] in enemy_locations:
								character_pos[1] -= move_speed
								print('Moved')
								moved_this_turn = True
								if move_speed == 2:
									jumped_this_turn = True
									print('You jumped')
				if not moved_this_turn:
					if event.key == pygame.K_s or event.key == pygame.K_DOWN:
						if map_list[character_pos[1]+move_speed][character_pos[0]].type != 2 and map_list[character_pos[1]+1][character_pos[0]].type != 2:
							if not [character_pos[0],character_pos[1]+move_speed] in enemy_locations:
								character_pos[1] += move_speed
								print('Moved')
								moved_this_turn = True
								if move_speed == 2:
									jumped_this_turn = True
									print('You jumped')
				if not moved_this_turn:
					if event.key == pygame.K_a or event.key == pygame.K_LEFT:
						if map_list[character_pos[1]][character_pos[0]-move_speed].type != 2 and map_list[character_pos[1]][character_pos[0]-1].type != 2:
							if not [character_pos[0]-move_speed,character_pos[1]] in enemy_locations:
								character_pos[0] -= move_speed
								print('Moved')
								moved_this_turn = True
								if move_speed == 2:
									jumped_this_turn = True
									print('You jumped')
				if not moved_this_turn:			
					if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
						if map_list[character_pos[1]][character_pos[0]+move_speed].type != 2 and map_list[character_pos[1]][character_pos[0]+1].type != 2:
							if not [character_pos[0]+move_speed,character_pos[1]] in enemy_locations:
								character_pos[0] += move_speed
								print('Moved')
								moved_this_turn = True
								if move_speed == 2:
									jumped_this_turn = True
									print('You jumped')
				if event.key == pygame.K_SPACE:
					return
		if moved_this_turn:

			print('Moved this turn')

			if not enemy_wait:
				regen_counter += 1
				if regen_counter >= regen_rate:
					if character_health >= max_character_health:
						regen_counter = int(regen_rate/2.0)
					else: 
						character_health += int(regen_counter/regen_rate)
						regen_counter = 0
					
				for enemy in enemy_locations:
					if enemies[enemy_locations.index(enemy)].alive:
						if enemy[0] > character_pos[0]-2 and enemy[0] < character_pos[0]+2 and enemy[1] > character_pos[1]-2 and enemy[1] < character_pos[1]+2:
							print('Imma attack you!')
							character_health -= 1
						elif not random.randrange(0,8) == 0:
							if map_list[enemy[1]][enemy[0]].visible:
								print('Enemy is visible')
								move_horizontal = random.choice([True, False])
								if move_horizontal:
									print('Horizontal movement has priority')
									if enemy[0] < character_pos[0] and map_list[enemy[1]][enemy[0]+1].type != 2 and not [enemy[0]+1, enemy[1]] in enemy_locations:
										print('You are to my right')
										enemy[0] += 1
									elif enemy[1] < character_pos[1] and map_list[enemy[1]+1][enemy[0]].type != 2 and not [enemy[0], enemy[1]+1] in enemy_locations:
										print('You are below me')
										enemy[1] += 1
									elif enemy[1] > character_pos[1] and map_list[enemy[1]-1][enemy[0]].type != 2 and not [enemy[0], enemy[1]-1] in enemy_locations:
										print('You are above me')
										enemy[1] -= 1
									elif enemy[0] > character_pos[0] and map_list[enemy[1]][enemy[0]-1].type != 2 and not [enemy[0]-1, enemy[1]] in enemy_locations:
										print('You are to my left')
										enemy[0] -= 1
									else:
										print('No possible movement')
								if not move_horizontal:
									print('Vertical movement has priority')
									if enemy[1] < character_pos[1] and map_list[enemy[1]+1][enemy[0]].type != 2 and not [enemy[0], enemy[1]+1] in enemy_locations:
										print('You are below me')
										enemy[1] += 1
									elif enemy[0] < character_pos[0] and map_list[enemy[1]][enemy[0]+1].type != 2 and not [enemy[0]+1, enemy[1]] in enemy_locations:
										print('You are to my right')
										enemy[0] += 1
									elif enemy[0] > character_pos[0] and map_list[enemy[1]][enemy[0]-1].type != 2 and not [enemy[0]-1, enemy[1]] in enemy_locations:
										print('You are to my left')
										enemy[0] -= 1
									elif enemy[1] > character_pos[1] and map_list[enemy[1]-1][enemy[0]].type != 2 and not [enemy[0], enemy[1]-1] in enemy_locations:
										print('You are above me')
										enemy[1] -= 1
									else:
										print('No possible movement')
							else:
								print("I'm moving randomly!")
								direction = random.randrange(0,4)
								if direction == 0 and map_list[enemy[1]][enemy[0]+1].type != 2 and not [enemy[0]+1, enemy[1]] in enemy_locations:
									enemy[0] += 1
								if direction == 1 and map_list[enemy[1]+1][enemy[0]].type != 2 and not [enemy[0], enemy[1]+1] in enemy_locations:
									enemy[1] += 1
								if direction == 2 and map_list[enemy[1]-1][enemy[0]].type != 2 and not [enemy[0], enemy[1]-1] in enemy_locations:
									enemy[1] -= 1
								if direction == 3 and map_list[enemy[1]][enemy[0]-1].type != 2 and not [enemy[0]-1, enemy[1]] in enemy_locations:
									enemy[0] -= 1
						else:
							print("Hurr durr, I'm just gonna sit here")
	return

class Room:
	def __init__(self, x1, x2, y1, y2):	
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.wall_top = y1 -1
		self.wall_bottom = y2 + 1
		self.wall_left = x1 - 1
		self.wall_right = x2 + 1
		self.height = y2 - y1
		self.width = x2 - x1
		self.discovered = False

	def intercepts(self, other_room):
		if self.wall_left <= other_room.wall_right and self.wall_right >= other_room.wall_left:
			if self.wall_top <= other_room.wall_bottom and self.wall_bottom >= other_room.wall_top:
				return True
		else: 
			return False

	def in_this_room(self, x, y):
		if x >= self.x1 and x <= self.x2:
			if y >= self.y1 and y <= self.y2:
				return True
		else:
			return False

	def is_wall(self, x, y):
		if not self.in_this_room(x, y):
			if x >= self.wall_left and x <= self.wall_right:
				if y >= self.wall_top and y <= self.wall_bottom:
					return True
		else:
			return False

	def tile_map(self, level_map):
		for y in range(self.wall_top, self.wall_bottom+1):
			for x in range(self.wall_left, self.wall_right+1):
				level_map[y][x] = Tile(2, False)
		for y in range(self.y1, self.y2+1):
			for x in range(self.x1, self.x2+1):
				level_map[y][x] = Tile(1, False)

	def discover(self):
		self.discovered = True

def carve_map(x, y, level_map):
	for row in range(y-1, y+2):
		for column in range(x-1, x+2):
			if level_map[row][column].type == 0:
				level_map[row][column] = Tile(2, False)
	else:
		level_map[y][x] = Tile(3, False)

def tile_rooms():
	for x in range(128):
		for y in range(128):
			for room in rooms:
				if room.in_this_room(x, y):
					map_list[y][x] = Tile(1, False)

def fill(x, y):
	if map_list[y][x].type == 1 or map_list[y][x].type == 3:
		if map_list[y][x].water == False:
			map_list[y][x].water = True
			screen.blit(water_tile, (x, y))
			# time.sleep(0.01)
			fill(x-1, y)
			fill(x+1, y)
			fill(x, y-1)
			fill(x, y+1)
	else:
		return

def unfill():
	for x in range(128):
		for y in range(128):
			map_list[y][x].water = False

corridors_made = 0

def make_corridors():
	global rooms
	global corridors_made
	global map_list
	unfill()
	fill_start = random.choice(rooms)
	fill(fill_start.x1, fill_start.y1)
	start_room = fill_start
	destination = random.choice(rooms)
	fill_start_pos = [fill_start.x1, fill_start.y1]
	destination_pos = [destination.x1, destination.y1]
	# print_map_dots(fill_start_pos, destination_pos)
	if not map_list[destination.y1][destination.x1].water:
		if not destination.intercepts(start_room):
			seed = random.randrange(2)
			corridors_made += 1
			if seed == 1:
				y_choices = [start_room.wall_top, start_room.wall_bottom]
				x = random.randrange(start_room.x1, start_room.x2+1)
				y = random.randrange(start_room.y1, start_room.y2+1)
				destination_y = random.randrange(destination.height) + destination.y1
				while y < destination_y:
					carve_map(x, y, map_list)
					y += 1
				while y > destination_y:
					carve_map(x, y, map_list)
					y += -1
				while x < destination.x1:
					carve_map(x, y, map_list)
					x += 1
				while x > destination.x2:
					carve_map(x, y, map_list)
					x += -1
			if seed == 0:
				x_choices = [start_room.wall_left, start_room.wall_right]
				x = random.randrange(start_room.x1, start_room.x2+1)
				y = random.randrange(start_room.y1, start_room.y2+1)
				destination_x = random.randrange(destination.width) + destination.x1
				while x < destination_x:
					carve_map(x, y, map_list)
					x += 1
				while x > destination_x:
					carve_map(x, y, map_list)
					x += -1
				while y < destination.y1:
					carve_map(x, y, map_list)
					y += 1
				while y > destination.y2:
					carve_map(x, y, map_list)
					y += -1
			print('Successfully created corridor %(corridor)i' % {'corridor' : corridors_made})
		else:
			print('Start and destination were the same, regenerating')
			return make_corridors()
	else:
		print('Invalid room pair, regenerating')
		return make_corridors()
	unfill()
	fill_start = random.choice(rooms)
	fill(fill_start.x1, fill_start.y1)
	# print_map()
	if corridors_made > 12:
		map_list = [[Tile(0, False) for y in range(128)] for x in range(128)]
		rooms = make_rooms()
		tile_rooms()
		print('Dungeon was too complex, regenerating')
		corridors_made = 0
		return make_corridors()
	for y in map_list:
		for x in y:
			if x.type == 1 and x.water == False:
				return make_corridors()

def random_room(rooms):
	x = random.randrange(1, 127)
	y = random.randrange(1, 127)
	w = random.randrange(1, 15)
	h = random.randrange(1, 15)
	x2 = x + w
	y2 = y + h
	room = Room(x, x2, y, y2)
	if x2 >= 127 or y2 >= 127:
		return random_room(rooms)
	for x in rooms:
		if room.intercepts(x):
			print('Room conflicted with existing room, regenerating')
			return random_room(rooms)
	else:
		print('Made room dimensions')
		return room

def make_rooms():
	rooms = []
	for x in range(random.randrange(4, 15)):
		room = random_room(rooms)
		print('Made room %(counter)i' % {'counter' : x + 1})
		room.tile_map(map_list)
		# print_map()
		rooms.append(room)
	tile_rooms()
	return rooms

class Enemy():
	def __init__(self, monster_type, hp):
		self.type = monster_type
		self.hp = hp
		self.alive = True
		self.turns_dead = 0
	def damage(self, value):
		self.hp -= value
		if self.hp <= 0:
			self.alive = False

		

def make_enemy():
	enemy_room = random.choice(rooms)
	enemy_pos = [enemy_room.x1 + random.randrange(0, enemy_room.width), enemy_room.y1 + random.randrange(0, enemy_room.height)]
	if enemy_pos != character_pos:
		if not enemy_pos in enemy_locations:
			return [enemy_pos,Enemy('monster', 5)]
	return make_enemy()

rooms = make_rooms()
make_corridors()
unfill()
tile_rooms()
char_room = rooms[0]
character_pos = [char_room.x1 + random.randrange(0, char_room.width), char_room.y1 + random.randrange(0, char_room.height)]
end_room = rooms[random.randrange(1, len(rooms))]
end_pos = [end_room.x1 + random.randrange(0, end_room.width), end_room.y1 + random.randrange(0, end_room.height)]
enemy_locations = []
enemies = []
for enemy in range(random.randrange(2,len(rooms))):
	enemy_info = make_enemy()
	enemy_locations.append(enemy_info[0])
	enemies.append(enemy_info[1])
print(enemy_locations)
print(enemies)
print_map_game(end_pos)