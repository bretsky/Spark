import random
import pygame
from pygame.locals import *
import sys
sys.setrecursionlimit(5000)
class Tile:
	def __init__(self, tile_type, water):
		self.type = tile_type
		self.water = water

map_list = [[Tile(0, False) for y in range(128)] for x in range(128)]
pygame.init()
screen = pygame.display.set_mode((512, 512))
floor_tile = pygame.Surface((4, 4)).convert()
floor_tile.fill((0,0,0))
wall_tile = pygame.Surface((4, 4)).convert()
wall_tile.fill((64, 64, 64))
bg_tile = pygame.Surface((4, 4)).convert()
bg_tile.fill((70, 45, 10))
water_tile = pygame.Surface((4, 4)).convert()
water_tile.fill((16, 16, 160))
hall_tile = pygame.Surface((4, 4)).convert()
hall_tile.fill((128, 128, 128))
rooms = []
framerate = pygame.time.Clock()

def print_map():
	print_go = True
	while print_go == True:
		
		framerate.tick(30)
		counter = 0
		# map_string = ''
		for y in map_list:
			x_counter = 0
			for x in y:

				if x.type == 0:
					screen.blit(bg_tile, (x_counter*4, counter*4))
					# map_string += '╦'
				if x.type == 1 and x.water == False:
					screen.blit(floor_tile, (x_counter*4, counter*4))
					# map_string += '.'
				if x.type == 2:
					screen.blit(wall_tile, (x_counter*4, counter*4))
					# map_string += 'I'
				if x.type == 3 and x.water  == False:
					screen.blit(hall_tile, (x_counter*4, counter*4))
					# map_string += ','
				if x.water == True:
					screen.blit(water_tile, (x_counter*4, counter*4))
					# map_string += '*'
				x_counter+=1
			
			# map_string += '\n'
			counter += 1
		pygame.display.update()
		# map_string += '\n\n\n\n\n\n\n\n'
		# print(map_string)
		events = pygame.event.get()
		for x in events:
			if x.type == pygame.QUIT:
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
				level_map[x][y] = Tile(2, False)
		for y in range(self.y1, self.y2+1):
			for x in range(self.x1, self.x2+1):
				level_map[x][y] = Tile(1, False)

def carve_map(x, y, level_map):
	for row in range(y-1, y+2):
		for column in range(x-1, x+2):
			if level_map[column][row].type == 0:
				level_map[column][row] = Tile(2, False)
	else:
		level_map[x][y] = Tile(3, False)

def tile_rooms():
	for x in range(128):
		for y in range(128):
			for room in rooms:
				if room.in_this_room(x, y):
					map_list[x][y] = Tile(1, False)




def fill(x, y):
	if map_list[x][y].type == 1 or map_list[x][y].type == 3:
		if map_list[x][y].water == False:
			map_list[x][y].water = True
			fill(x-1, y)
			fill(x+1, y)
			fill(x, y-1)
			fill(x, y+1)
	else:
		return

def unfill():
	for x in range(128):
		for y in range(128):
			map_list[x][y].water = False

def make_corridors():
	# tile_rooms()
	# print_map()
	unfill()
	fill_start = random.choice(rooms)
	fill(fill_start.x1, fill_start.y1)
	start_room = fill_start
	destination = random.choice(rooms)
	if not map_list[destination.x1][destination.y1].water:
		if not destination.intercepts(start_room):
			seed = random.randrange(2)
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
	else:
		return make_corridors()
	unfill()
	fill_start = random.choice(rooms)
	fill(fill_start.x1, fill_start.y1)
	# print_map()
	for y in map_list:
		for x in y:
			if x.type == 1 and x.water == False:
				return make_corridors()
	else:
		return
	

def random_room():
	x = random.randrange(1, 127)
	y = random.randrange(1, 127)
	w = random.randrange(1, 15)
	h = random.randrange(1, 15)
	x2 = x + w
	y2 = y + h
	room = Room(x, x2, y, y2)
	if x2 >= 127 or y2 >= 127:
		return random_room()
	for x in rooms:
		if room.intercepts(x):
			return random_room()
	else:
		return room

rooms = []
for x in range(random.randrange(4, 21)):
	room = random_room()
	room.tile_map(map_list)
	rooms.append(room)
tile_rooms()


make_corridors()
unfill()
tile_rooms()

print_map()

