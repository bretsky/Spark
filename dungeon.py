import random
import pygame
from pygame.locals import *
import sys
import time
import dungeon_name_generator

sys.setrecursionlimit(5000)

class Tile:
	def __init__(self, tile_type, water):
		self.type = tile_type
		self.water = water
		self.light = 0
	def set_light(self, value):
		if value > self.light:
			self.light = value

character_pos = [0, 0]
map_list = [[Tile(0, False) for y in range(128)] for x in range(128)]
pygame.init()
screen_x = 1024
screen_y = 1024
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption(dungeon_name_generator.random_dungeon_name())
screen_bg = pygame.Surface((1024, 1024)).convert()
screen_bg.fill((0, 0, 0))
floor_tile = pygame.Surface((8, 8)).convert()
floor_tile.fill((30, 16, 3))
wall_tile = pygame.Surface((8, 8)).convert()
wall_tile.fill((63, 63, 63))
bg_tile = pygame.Surface((8, 8)).convert()
bg_tile.fill((70, 45, 10))
water_tile = pygame.Surface((8, 8)).convert()
water_tile.fill((16, 16, 160))
hall_tile = pygame.Surface((8, 8)).convert()
hall_tile.fill((148, 120, 78))
character_tile = pygame.Surface((8, 8)).convert()
character_tile.fill((255, 255, 255))
destination_tile = pygame.Surface((8, 8)).convert()
destination_tile.fill((255, 0, 0))
start_tile = pygame.Surface((8, 8)).convert()
start_tile.fill((0, 255, 0))
rooms = []
framerate = pygame.time.Clock()

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
					screen.blit(bg_tile, (x_counter*8, counter*8))
				if x.type == 1 and x.water == False:
					screen.blit(floor_tile, (x_counter*8, counter*8))
				if x.type == 2:
					screen.blit(wall_tile, (x_counter*8, counter*8))
				if x.type == 3 and x.water  == False:
					screen.blit(hall_tile, (x_counter*8, counter*8))
				if x.water == True:
					screen.blit(water_tile, (x_counter*8, counter*8))
				x_counter+=1
			counter += 1
		screen.blit(character_tile, (character_pos[0]*8, character_pos[1]*8))
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
					screen.blit(bg_tile, (x_counter*8, counter*8))
				if x.type == 1 and x.water == False:
					screen.blit(floor_tile, (x_counter*8, counter*8))
				if x.type == 2:
					screen.blit(wall_tile, (x_counter*8, counter*8))
				if x.type == 3 and x.water  == False:
					screen.blit(hall_tile, (x_counter*8, counter*8))
				if x.water == True:
					screen.blit(water_tile, (x_counter*8, counter*8))
				x_counter+=1
			counter += 1
		screen.blit(destination_tile, (destination[0]*8, destination[1]*8))
		screen.blit(start_tile, (fill_start[0]*8, fill_start[1]*8))
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
	# time.clock()
	# frame_counter = 0
	# seconds = 1
	while print_go == True:
		framerate.tick(60)
		# frame_counter += 1
		# if time.clock() >= seconds:
		# 	print(frame_counter)
		# 	frame_counter = 0
		# 	seconds += 1
		moved_this_turn = False
		counter = 0
		for room in rooms:
			if room.in_this_room(character_pos[0], character_pos[1]):
				for room_y in range(room.height+3):
					for room_x in range(room.width+3):
						for y in range(7):
							for x in range(7):
								light_pos = [room_x-3+x+room.wall_left, room_y-3+y+room.wall_top]
								if light_pos[0] < 128 and light_pos[1] < 128: 
									map_list[light_pos[1]][light_pos[0]].set_light(31)
						for y in range(5):
							for x in range(5):
								light_pos = [room_x-2+x+room.wall_left, room_y-2+y+room.wall_top]
								if light_pos[0] < 128 and light_pos[1] < 128: 
									map_list[light_pos[1]][light_pos[0]].set_light(63)
						for y in range(3):
							for x in range(3):
								light_pos = [room_x-1+x+room.wall_left, room_y-1+y+room.wall_top]
								if light_pos[0] < 128 and light_pos[1] < 128: 
									map_list[light_pos[1]][light_pos[0]].set_light(127)						
						map_list[room_y+room.wall_top][room_x+room.wall_left].set_light(255)
		for y in range(9):
			for x in range(9):
				light_pos = [character_pos[0]-4+x, character_pos[1]-4+y]
				if light_pos[0] < 128 and light_pos[1] < 128: 
					map_list[light_pos[1]][light_pos[0]].set_light(31)
		for y in range(7):
			for x in range(7):
				light_pos = [character_pos[0]-3+x, character_pos[1]-3+y]
				if light_pos[0] < 128 and light_pos[1] < 128: 
					map_list[light_pos[1]][light_pos[0]].set_light(63)
		for y in range(5):
			for x in range(5):
				light_pos = [character_pos[0]-2+x, character_pos[1]-2+y]
				if light_pos[0] < 128 and light_pos[1] < 128: 
					map_list[light_pos[1]][light_pos[0]].set_light(127)
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
					x_tile.set_alpha(x.light)
					screen.blit(x_tile, (x_counter*8, counter*8))
				if x.type == 1 and x.water == False:
					x_tile = floor_tile
					x_tile.set_alpha(x.light)
					screen.blit(x_tile, (x_counter*8, counter*8))
				if x.type == 2:
					x_tile = wall_tile
					x_tile.set_alpha(x.light)
					screen.blit(x_tile, (x_counter*8, counter*8))
				if x.type == 3 and x.water  == False:
					x_tile = hall_tile
					x_tile.set_alpha(x.light)
					screen.blit(x_tile, (x_counter*8, counter*8))
				if x.water == True:
					screen.blit(water_tile, (x_counter*8, counter*8))
				x_counter+=1
			counter += 1
		x_tile = destination_tile
		x_tile.set_alpha(map_list[destination[1]][destination[0]].light)
		screen.blit(x_tile, (destination[0]*8, destination[1]*8))
		screen.blit(character_tile, (character_pos[0]*8, character_pos[1]*8))
		for enemy in enemies:
			x_tile = water_tile
			x_tile.set_alpha(map_list[enemy[1]][enemy[0]].light)
			screen.blit(x_tile, (enemy[0]*8, enemy[1]*8))
		pygame.display.update()
		for enemy in enemies:
			if enemy == character_pos:
				print('You Lose')
				return
		if character_pos == destination:
			return
		events = pygame.event.get()
		key = pygame.key.get_pressed()
		move_speed = 1
		mods = pygame.key.get_mods()
		if mods & KMOD_SHIFT:
			move_speed = 2
		if not moved_this_turn:
			if key[pygame.K_w] or key[pygame.K_UP]:
				w_count += move_speed
				if w_count >= 20:
					w_count = 0
					if map_list[character_pos[1]-1][character_pos[0]].type != 2:
						w_count += 16
						character_pos[1] -= 1
						moved_this_turn = True
			else:
				w_count = 0
		if not moved_this_turn:
			if key[pygame.K_s] or key[pygame.K_DOWN]:
				s_count += move_speed
				if s_count >= 20:
					s_count = 0
					if map_list[character_pos[1]+1][character_pos[0]].type != 2:
						s_count += 16
						character_pos[1] += 1
						moved_this_turn = True
			else:
				s_count = 0
		if not moved_this_turn:
			if key[pygame.K_a] or key[pygame.K_LEFT]:
				a_count += move_speed
				if a_count >= 20:
					a_count = 0
					if map_list[character_pos[1]][character_pos[0]-1].type != 2:
						a_count += 16
						character_pos[0] -= 1
						moved_this_turn = True
			else:
				a_count = 0
		if not moved_this_turn:
			if key[pygame.K_d] or key[pygame.K_RIGHT]:
				d_count += move_speed
				if d_count >= 20:
					d_count = 0
					if map_list[character_pos[1]][character_pos[0]+1].type != 2:
						d_count += 16
						character_pos[0] += 1
						moved_this_turn = True
			else:
				d_count = 0
		for event in events:
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				if not moved_this_turn:
					if event.key == pygame.K_w or event.key == pygame.K_UP:
						if map_list[character_pos[1]-move_speed][character_pos[0]].type != 2 and map_list[character_pos[1]-1][character_pos[0]].type != 2:
							character_pos[1] -= move_speed
							moved_this_turn = True
				if not moved_this_turn:
					if event.key == pygame.K_s or event.key == pygame.K_DOWN:
						if map_list[character_pos[1]+move_speed][character_pos[0]].type != 2 and map_list[character_pos[1]+1][character_pos[0]].type != 2:
							character_pos[1] += move_speed
							moved_this_turn = True
				if not moved_this_turn:
					if event.key == pygame.K_a or event.key == pygame.K_LEFT:
						if map_list[character_pos[1]][character_pos[0]-move_speed].type != 2 and map_list[character_pos[1]][character_pos[0]-1].type != 2:
							character_pos[0] -= move_speed
							moved_this_turn = True
				if not moved_this_turn:			
					if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
						if map_list[character_pos[1]][character_pos[0]+move_speed].type != 2 and map_list[character_pos[1]][character_pos[0]+1].type != 2:
							character_pos[0] += move_speed
							moved_this_turn = True
				if event.key == pygame.K_SPACE:
					return

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
	print_map_dots(fill_start_pos, destination_pos)
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
	print_map()
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
	for x in range(random.randrange(4, 17)):
		room = random_room(rooms)
		print('Made room %(counter)i' % {'counter' : x + 1})
		room.tile_map(map_list)
		print_map()
		rooms.append(room)
	tile_rooms()
	return rooms

def make_enemy():
	enemy_room = random.choice(rooms)
	enemy_pos = [enemy_room.x1 + random.randrange(0, enemy_room.width), enemy_room.y1 + random.randrange(0, enemy_room.height)]
	if enemy_pos != character_pos:
		if not enemy_pos in enemies:
			return enemy_pos
	else:
		return make_enemy()
rooms = make_rooms()
make_corridors()
unfill()
tile_rooms()
char_room = rooms[0]
character_pos = [char_room.x1 + random.randrange(0, char_room.width), char_room.y1 + random.randrange(0, char_room.height)]
end_room = rooms[random.randrange(1, len(rooms))]
end_pos = [end_room.x1 + random.randrange(0, end_room.width), end_room.y1 + random.randrange(0, end_room.height)]
enemies = []
for enemy in range(random.randrange(1,5)):
	enemies.append(make_enemy())
print(enemies)
print_map_game(end_pos)