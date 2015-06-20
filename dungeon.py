import random
import pygame
from pygame.locals import *
import sys
import time
sys.setrecursionlimit(5000)
class Tile:
	def __init__(self, tile_type, water):
		self.type = tile_type
		self.water = water
character_pos = [0, 0]
map_list = [[Tile(0, False) for y in range(128)] for x in range(128)]
pygame.init()
screen_x = 1024
screen_y = 1024
screen = pygame.display.set_mode((screen_x, screen_y))
floor_tile = pygame.Surface((8, 8)).convert()
floor_tile.fill((0,0,0))
wall_tile = pygame.Surface((8, 8)).convert()
wall_tile.fill((64, 64, 64))
bg_tile = pygame.Surface((8, 8)).convert()
bg_tile.fill((70, 45, 10))
water_tile = pygame.Surface((8, 8)).convert()
water_tile.fill((16, 16, 160))
hall_tile = pygame.Surface((8, 8)).convert()
hall_tile.fill((128, 128, 128))
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
		# map_string = ''
		for y in map_list:
			x_counter = 0
			for x in y:

				if x.type == 0:
					screen.blit(bg_tile, (x_counter*8, counter*8))
					# map_string += '╦'
				if x.type == 1 and x.water == False:
					screen.blit(floor_tile, (x_counter*8, counter*8))
					# map_string += '.'
				if x.type == 2:
					screen.blit(wall_tile, (x_counter*8, counter*8))
					# map_string += 'I'
				if x.type == 3 and x.water  == False:
					screen.blit(hall_tile, (x_counter*8, counter*8))
					# map_string += ','
				if x.water == True:
					screen.blit(water_tile, (x_counter*8, counter*8))
					# map_string += '*'
				x_counter+=1
			
			# map_string += '\n'
			counter += 1

		screen.blit(character_tile, (character_pos[0]*8, character_pos[1]*8))
		pygame.display.update()
		# map_string += '\n\n\n\n\n\n\n\n'
		# print(map_string)
		events = pygame.event.get()
		key = pygame.key.get_pressed()
		if key[pygame.K_w] or key[pygame.K_UP]:
			w_count += 1
			if w_count == 20:
				w_count = 0
				if character_pos[1] != 0:
					w_count += 16
					character_pos[1] -= 1
		else:
			w_count = 0
		if key[pygame.K_s] or key[pygame.K_DOWN]:
			s_count += 1
			if s_count == 20:
				s_count = 0
				if character_pos[1] != len(map_list)-1:
					s_count += 16
					character_pos[1] += 1
		else:
			s_count = 0
		if key[pygame.K_a] or key[pygame.K_LEFT]:
			a_count += 1
			if a_count == 20:
				a_count = 0
				if character_pos[0] != 0:
					a_count += 16
					character_pos[0] -= 1
		else:
			a_count = 0
		if key[pygame.K_d] or key[pygame.K_RIGHT]:
			d_count += 1
			if d_count == 20:
				d_count = 0
				if character_pos[0] != len(map_list)-1:
					d_count += 16
					character_pos[0] += 1
		else:
			d_count = 0
		for event in events:
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w or event.key == pygame.K_UP:
					if character_pos[1] != 0:
						character_pos[1] -= 1
				if event.key == pygame.K_s or event.key == pygame.K_DOWN:
					if character_pos[1] != len(map_list)-1:
						character_pos[1] += 1
				if event.key == pygame.K_a or event.key == pygame.K_LEFT:
					if character_pos[0] != 0:
						character_pos[0] -= 1
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					if character_pos[0] != len(map_list)-1:
						character_pos[0] += 1
				if event.key == pygame.K_SPACE:
					return
				
	return

def print_map_dots(fill_start, destination):
	print_go = True
	while print_go == True:
		
		framerate.tick(55)
		counter = 0
		# map_string = ''
		for y in map_list:
			x_counter = 0
			for x in y:

				if x.type == 0:
					screen.blit(bg_tile, (x_counter*8, counter*8))
					# map_string += '╦'
				if x.type == 1 and x.water == False:
					screen.blit(floor_tile, (x_counter*8, counter*8))
					# map_string += '.'
				if x.type == 2:
					screen.blit(wall_tile, (x_counter*8, counter*8))
					# map_string += 'I'
				if x.type == 3 and x.water  == False:
					screen.blit(hall_tile, (x_counter*8, counter*8))
					# map_string += ','
				if x.water == True:
					screen.blit(water_tile, (x_counter*8, counter*8))
					# map_string += '*'
				x_counter+=1
			
			# map_string += '\n'
			counter += 1
		screen.blit(destination_tile, (destination.x1*8, destination.y1*8))
		screen.blit(start_tile, (fill_start.x1*8, fill_start.y1*8))
		# screen.blit(character_tile, (character_pos[0]*4, character_pos[1]*4))
		pygame.display.update()
		# map_string += '\n\n\n\n\n\n\n\n'
		# print(map_string)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
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
	# tile_rooms()
	# print_map()
	unfill()
	fill_start = random.choice(rooms)
	fill(fill_start.x1, fill_start.y1)
	
	start_room = fill_start
	destination = random.choice(rooms)
	print_map_dots(fill_start, destination)
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

rooms = make_rooms()
make_corridors()
unfill()
tile_rooms()
char_room = rooms[0]
character_pos = [char_room.x1, char_room.y1]
print_map()

# if True:
# 	counter = 0
# 	map_string = ''
# 	for y in map_list:
# 		x_counter = 0
# 		for x in y:

# 			if x.type == 0:
# 				map_string += '╦'
# 			if x.type == 1 and x.water == False:
# 				map_string += '.'
# 			if x.type == 2:
# 				map_string += 'I'
# 			if x.type == 3 and x.water  == False:
# 				map_string += ','
# 			if x.water == True:
# 				map_string += '*'
# 			x_counter+=1
		
# 		map_string += '\n'
# 		counter += 1
# 	map_string += '\n\n\n\n\n\n\n\n'
# 	print(map_string)
# print(char_room.x1, char_room.x2, char_room.y1, char_room.y2)
# print(character_pos)
# print(character_pos[0]*4, character_pos[1]*4)
# for room in rooms:
# 	print((room.x1, room.y1))

print_map()
