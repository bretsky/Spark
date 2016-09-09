import random
import PyBearLibTerminal as brlb
from screeninfo import screeninfo
# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput
import decimal 
from time import perf_counter as get_time
from copy import deepcopy
import json
import time

def signed_pow(i, n):
	return abs(i)/i * abs(i)**n

def smooth_explode():
	val = 0
	for i in range(6):
		roll = random.random()
		val += roll
		if roll < 0.95:
			return val
		print('exploded')
	return val

def explode(l):
	val = 0
	for i in range(4):
		pick = random.choice(l)
		val += pick
		if val != max(l):
			break
	return val

def round_rand(n):
	r = random.choice([True, False])
	if r:
		return int(decimal.Decimal(n).quantize(decimal.Decimal(1), rounding=decimal.ROUND_HALF_UP))
	else:
		return int(decimal.Decimal(n).quantize(decimal.Decimal(1), rounding=decimal.ROUND_HALF_DOWN))

def ceiling(n, p=-1):
	return float(decimal.Decimal(n).quantize(decimal.Decimal(str(10**p)), rounding=decimal.ROUND_CEILING))

def round_up(n, p=1):
	return int(decimal.Decimal(n).quantize(decimal.Decimal(p), rounding=decimal.ROUND_HALF_UP))

def randint(start, stop):
	if start != stop:
		return random.randrange(start, stop + 1)
	return start

def p_choice(n, total):
	keys = list(n.keys())
	r = random.randrange(total)
	x = -1
	while x < r:
		key = random.choice(keys)
		x += n[key]
	return key

def r_key_search(key, var):
	if hasattr(var,'items'):
		for k, v in var.items():
			if k == key:
				return [k]
			if isinstance(v, dict):
				result = r_key_search(key, v)
				if result:
					result.insert(0, k)
					return result
			elif isinstance(v, list):
				for d in v:
					result =  r_key_search(key, d)
					if result:
						result.insert(0, k)
						return result
	return False

def get_from_path(d, path):
	# print(d)
	if path:
		for s in path:
			d = d[s]
	return deepcopy(d)

class Dungeon():
	def __init__(self, level, animate=False, name=False):
		self.animate = animate
		self.level = level
		self.import_files()
		if name:
			self.name = name
		else:
			self.name = self.random_dungeon_name()
		self.map_list = [[Tile(BG_TILE, False) for y in range(64)] for x in range(64)]
		for y in range(len(self.map_list)):
			for x in range(len(self.map_list)):
				if min(min(x, y), 63 - max(x, y)) == 0:
					self.map_list[y][x].type = 2
				elif min(min(x, y), 63 - max(x, y)) < 5:
					if random.randrange(min(min(x, y), 63 - max(x, y))**2 + 1) == 0:
						self.map_list[y][x].type = 2
		if self.animate:
			self.debug_draw() #animate
		self.corridors_made = 0
		start = get_time()
		self.rooms = self.make_rooms()
		self.destination = random.choice(tuple(random.choice(self.rooms).tiles))
		self.start = False
		while self.start == self.destination or self.start == False:
			self.start = random.choice(tuple(random.choice(self.rooms).tiles))
		print('made rooms in', get_time()-start)
		self.debug = False
		start = get_time()
		self.make_corridors()
		# try:
		# 	self.make_corridors()
		# except RuntimeError:
		# 	self.debug = True
		# 	print('RuntimeError occurred')
		print('made corridors in', get_time()-start)
		if self.animate:
			self.persistent_draw()
		self.unfill()
		self.tile_rooms()

	def import_files(self):
		geo_file = open('data/dungeon/geographical_features.txt')
		dungeon_attr_file = open('data/dungeon/dungeon_attributes.txt')
		dungeon_adj_file = open('data/dungeon/dungeon_adjectives.txt')
		dungeon_word_file = open('data/dungeon/dungeon_words.txt')
		self.geo_list = geo_file.read().splitlines()
		self.dungeon_attr_list = dungeon_attr_file.read().splitlines()
		self.dungeon_adj_list = dungeon_adj_file.read().splitlines()
		self.dungeon_word_list = dungeon_word_file.read().splitlines()
		print("Possible names: ", len(self.dungeon_word_list)*len(self.geo_list) + len(self.dungeon_adj_list)*len(self.geo_list) + len(self.geo_list)*len(self.dungeon_attr_list) + len(self.dungeon_adj_list)*len(self.geo_list)*len(self.dungeon_attr_list) + len(self.geo_list)*len(self.dungeon_adj_list)*len(self.dungeon_attr_list))

	def darken(self, room):
		for wall in room.walls:
			self.map_list[wall[1]][wall[0]].visible = False
			self.map_list[wall[1]][wall[0]].light = 0
		for tile in room.tiles:
			self.map_list[tile[1]][tile[0]].visible = False
			self.map_list[tile[1]][tile[0]].light = 0

	def random_dungeon_name(self):
		num = random.randrange(0,5)
		if num == 0:
			dungeon_name = ' '.join(word[0].upper() + word[1:] for word in random.choice(self.dungeon_word_list).split()) + ' ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(self.geo_list).split())
		elif num == 1:
			dungeon_name = 'The ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(self.dungeon_adj_list).split()) + ' ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(self.geo_list).split())
		elif num == 2:
			dungeon_name = 'The ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(self.geo_list).split()) + ' of ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(self.dungeon_attr_list).split())
		elif num == 3:
			dungeon_name = 'The ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(self.dungeon_adj_list).split()) + ' ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(self.geo_list).split()) + ' of ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(self.dungeon_attr_list).split())
		elif num == 4:
			dungeon_name = 'The ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(self.geo_list).split()) + ' of ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(self.dungeon_adj_list).split()) + ' ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(self.dungeon_attr_list).split())
		return dungeon_name

	def make_corridors(self):
		self.corridors = []
		for y in range(len(self.map_list)):
			for x in range(len(self.map_list[y])):
				if self.map_list[y][x].type == 0:
					self.maze_trail = []
					if self.suitable_starting_point((x, y)):
						self.maze(x, y)
						self.corridors.extend(self.maze_trail)
		self.find_connectors()
		self.make_doors()
		self.remove_dead_ends()
		# self.persistent_draw()

	def suitable_starting_point(self, coord):
		for x in range(3):
			for y in range(3):
				if self.map_list[coord[1] + y -1][coord[0] + x -1].type == 3:
					self.map_list[coord[1]][coord[0]].type = 4
					return False
		return True

	def creates_loop(self, starting_coord, new_coord):
		change_coord = [starting_coord[i]-new_coord[i] for i in range(2)]
		if change_coord[0] != 0:
			for x in range(3):
				for y in range(3):
					if new_coord[0] + x - 1 != starting_coord[0]:
						if self.map_list[new_coord[1] + y -1][new_coord[0] + x -1].type == 3:
							self.map_list[new_coord[1]][new_coord[0]].type = 4
							return True
		if change_coord[1] != 0:
			for x in range(3):
				for y in range(3):
					if new_coord[1] + y - 1 != starting_coord[1]:
						if self.map_list[new_coord[1] + y -1][new_coord[0] + x -1].type == 3:
							self.map_list[new_coord[1]][new_coord[0]].type = 4
							return True
		return False

	def is_significant(self, starting_coord, new_coord):	
		if self.map_list[new_coord[1]][new_coord[0]].type != 4:
			return True
		return self.creates_loop(starting_coord, new_coord)

	def maze(self, x, y):
		directions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
		directions = [d for d in directions if self.map_list[d[1]][d[0]].type == 0]
		direction = ()
		self.maze_trail.append((x, y))
		self.map_list[y][x].type = 3
		while direction != self.maze_trail[0]:
			self.branch_trail = []
			while len(directions) > 0:
				if self.animate:
					if random.randrange(3) == 0:
						self.debug_refresh() #animate
				direction = directions.pop(random.randrange(len(directions)))
				self.branch_trail.append(direction)
				if len(self.branch_trail) >= 3:
					if self.branch_trail[-3][0] != self.branch_trail[-1][0] and self.branch_trail[-3][1] != self.branch_trail[-1][1]:
						first_change = (self.branch_trail[-3][0] - self.branch_trail[-2][0], self.branch_trail[-3][1] - self.branch_trail[-2][1])
						second_change = (self.branch_trail[-2][0] - self.branch_trail[-1][0], self.branch_trail[-2][1] - self.branch_trail[-1][1])
						if not self.map_list[self.branch_trail[-2][1] - first_change[1] + second_change[1]][self.branch_trail[-2][0] - first_change[0] + second_change[0]].type == 2:
							self.map_list[self.branch_trail[-2][1] - first_change[1] + second_change[1]][self.branch_trail[-2][0] - first_change[0] + second_change[0]].type = 4
				for d in directions:
					self.map_list[d[1]][d[0]].type = 4
				x, y = direction
				self.map_list[y][x].type = 3
				directions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
				directions = [d for d in directions if self.map_list[d[1]][d[0]].type == 0 and not self.creates_loop(direction, d)]
			self.maze_trail.extend(self.branch_trail)
			index = 0
			while len(directions) == 0 and index + len(self.maze_trail) > 0:
				index -= 1
				direction = self.maze_trail[index]
				x, y = direction
				directions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
				directions = [d for d in directions if not self.is_significant(direction, d)]

	def regionize(self):
		self.non_region_tiles = []
		self.regions = {}
		for y in range(len(self.map_list)):
			for x in range(len(self.map_list[y])):
				if self.map_list[y][x].type in set((3, 1, 5)):
					self.non_region_tiles.append((x, y))
		region = 0
		while len(self.non_region_tiles) > 0:
			
			self.fill(*self.non_region_tiles[0])
			if self.animate:
				self.debug_refresh() #animate
			region_tiles = set()
			for tile in self.non_region_tiles:
				if self.map_list[tile[1]][tile[0]].water:
					region_tiles.add(tile)
					self.map_list[tile[1]][tile[0]].region = region
			self.non_region_tiles = [tile for tile in self.non_region_tiles if tile not in region_tiles]
			self.regions[region] = list(region_tiles)
			self.unfill()
			region += 1
		for room in self.rooms:
			midpoint = room.midpoint
			room.region = self.map_list[midpoint[1]][midpoint[0]].region
		self.room_regions = {}
		for region in list(self.regions.keys()):
			region_rooms = []
			for room in self.rooms:
				if room.region == region:
					region_rooms.append(room)
			if region_rooms:
				self.room_regions[region] = region_rooms

	def in_bounds(self, x, y):
		if max(x, y) >= 64 or min(x, y) < 0:
			return False
		return True

	def find_connectors(self):
		# brlb.close()
		self.connectors = []
		self.regionize()

		for room in self.rooms:
			for wall in room.walls:
				x, y = wall
				directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
				region_not_found = True
				d = 0
				while region_not_found and d < len(directions):
					if self.in_bounds(x + directions[d][0], y + directions[d][1]):
						if self.map_list[y + directions[d][1]][x + directions[d][0]].region != -1:
							potential_connectors = []
							region = self.map_list[y + directions[d][1]][x + directions[d][0]].region
							i = 0
							connected = False
							while i < 4 and not connected:
								if self.in_bounds(x - directions[d][0] * i, y - directions[d][1] * i):
									connecting_region = self.map_list[y - directions[d][1] * i][x - directions[d][0] * i].region
									if self.map_list[y - directions[d][1] * i][x - directions[d][0] * i].type == 4:
										connected = True
									elif connecting_region not in (-1, region):			
										self.connectors.append(potential_connectors)
										for x, y in potential_connectors:
											self.map_list[y][x].connector = True
										# self.debug_refresh() #animate
										connected = True
									elif connecting_region == region:
										connected = True
									else:
										potential_connectors.append((x - directions[d][0] * i, y - directions[d][1] * i))
								i += 1
					d += 1
		for connection in self.connectors:
			for connector in connection:
				x, y = connector
				self.map_list[y][x].connector = True

	def delete_connectors(self):
		for i in range(len(self.connectors)):
			if random.randrange(50) == 0:
				for x, y in self.connectors[i]:
					self.map_list[y][x].type = 5
			for x, y in self.connectors[i]:
				self.map_list[y][x].connector = False
			if self.animate:
				self.debug_refresh() #animate
		self.connectors = []

	def make_doors(self):
		while len(self.connectors) > 0:
			main_room = random.choice(self.room_regions[random.choice(list(self.room_regions.keys()))])
			potential_connectors = [connection for connection in self.connectors for connector in connection if connector in [wall for room in self.room_regions[main_room.region] for wall in room.walls]]
			if potential_connectors:
				connection = random.choice(potential_connectors)
				for connector in connection:
					self.map_list[connector[1]][connector[0]].type = 5
					if self.animate:
						self.debug_refresh() #animate
				self.delete_connectors()
				self.find_connectors()

	def remove_dead_ends(self):
		self.find_dead_ends()
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		count = 1
		remain = random.randrange(0, 4)
		while len(self.dead_ends) > remain:			
			for x, y in self.dead_ends:
				if random.randrange(0, count*15) != 0:
					self.map_list[y][x].type = 4
					self.corridors.remove((x, y))
				else:
					d = [direction for direction in directions if self.map_list[direction[1] + y][direction[0] + x].type == 4]
					if len(d) > 0:
						d = random.choice(d)
						self.map_list[d[1] + y][d[0] + x].type = 3
						self.corridors.append((d[0] + x, d[1] + y))
				if self.animate:			
					self.debug_refresh() #animate
			count += 1
			self.find_dead_ends()


	def find_dead_ends(self):
		self.dead_ends = []
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		for x, y in self.corridors:
			d = [direction for direction in directions if self.map_list[direction[1] + y][direction[0] + x].type in (2, 4)]
			if len(d) >= 3:
				self.dead_ends.append((x, y))


	def fill(self, x, y):
		potential_pos = set()
		potential_pos.add((x, y))
		new_pos = set()
		filled_pos = set()
		while len(potential_pos) > 0:
			potential_pos.update(new_pos)
			potential_pos.difference_update(filled_pos)
			for x, y in potential_pos:
				if self.map_list[y][x].type == 1 or self.map_list[y][x].type == 3 or self.map_list[y][x].type == 5:
					if self.map_list[y][x].water == False:
						self.map_list[y][x].water = True
						if self.animate:
							if random.randrange(0, 4) == 0:
								self.debug_refresh() #animate
						new_pos.add((x-1, y))
						new_pos.add((x+1, y))
						new_pos.add((x, y-1))
						new_pos.add((x, y+1))
				filled_pos.add((x, y))
		return

	def unfill(self):
		for x in range(1, 63):
			for y in range(1, 63):
				self.map_list[y][x].water = False

	def random_scale(self):
		return int(sum([explode([1,1,1,1,1,1,2,2,3,4,5,6,7,8,9,10,10,10,10,10,10,10]) for i in range(4)])/3 + 3)

	def random_room(self):
		SQUARENESS = 1
		xscale = self.random_scale()
		yscale = self.random_scale()
		p1 = (random.randrange(64), random.randrange(64))
		p2 = (p1[0] + xscale, p1[1] + int(signed_pow(random.random()-0.5, SQUARENESS)*yscale))
		p3 = (p2[0] + int(signed_pow(random.random()-0.5, SQUARENESS)*xscale), p2[1] + yscale)
		rand = (random.random()-0.5, random.random()-0.5)
		p4 = (p1[0] + int(signed_pow(rand[0], SQUARENESS)*xscale), p3[1] + int(signed_pow(rand[1], SQUARENESS)*yscale))
		p = [p1, p2, p3, p4]		
		room = Room(*p)
		if room.in_bounds(0, 64):
			return room
		else:
			return self.random_room()

	def carve_map(self, x, y):
		for row in range(y-1, y+2):
			for column in range(x-1, x+2):
				if self.map_list[row][column].type == 0:
					self.map_list[row][column] = Tile(2, False)
		else:
			self.map_list[y][x] = Tile(3, False)

	def random_room_count(self):
		return 2*int(sum([explode([1,1,1,1,1,1,2,2,3,4,5,6,7,8,9,10,10,10,10,10,10,10]) for i in range(4)]) + 4)

	def place(self, room):
		if self.rooms:
			for existing_room in self.rooms:
				if room.intercepts(existing_room):
					return self.rooms
		self.rooms.append(room)
		return self.rooms

	def make_rooms(self):
		self.rooms = []
		# print(type(self.rooms))
		if self.animate:
			self.debug_draw() #animate
		for x in range(self.random_room_count()):
			room = self.random_room()
			# print('Made room %(counter)i' % {'counter' : x + 1})
			# print(type(self.rooms))
			self.rooms = self.place(room)
		for room in self.rooms:
			room.tile_map(self.map_list)
			if self.animate:
				self.debug_refresh() #animate
		self.tile_rooms()
		return self.rooms

	def tile_rooms(self):
		for room in self.rooms:		
			for x, y in room.tiles:
				self.map_list[y][x] = Tile(1, False)

	def get_room(self, x, y):
		for room in self.rooms:
			if room.in_this_room(x, y):
				return room
		return False

	def debug_draw(self):
		brlb.open()
		brlb.set('window.title=d-gen; font: unifont-8.0.01.ttf, size=12x12; window.size=64x64;')
		brlb.composition(brlb.TK_OFF)
		brlb.refresh()
		for y in range(len(self.map_list)):
			for x in range(len(self.map_list[y])):
				if self.map_list[y][x].water:
					brlb.color(brlb.color_from_argb(255, 0, 0, 255))
				elif self.map_list[y][x].connector:
					brlb.color(brlb.color_from_argb(255, 255, 0, 0))
				else:
					brlb.color(brlb.color_from_argb(255, 255, 255, 255))
				if self.map_list[y][x].type == 1:
					brlb.put(x, y, '.')
				elif self.map_list[y][x].type == 2:
					brlb.put(x, y, 9608)
				elif self.map_list[y][x].type == 3:
					brlb.put(x, y, '#')
				elif self.map_list[y][x].type == 4:
					brlb.put(x, y, 9618)
				elif self.map_list[y][x].type == 0:
					brlb.put(x, y, 'O')
				elif self.map_list[y][x].type == 5:
					brlb.color(brlb.color_from_argb(255, 255, 255, 0))
					brlb.put(x, y, 'X')
		brlb.refresh()
		closed = False
		while closed != brlb.TK_CLOSE and closed != brlb.TK_SPACE:
			if brlb.has_input():
				
				closed = brlb.read()

	def persistent_draw(self):
		brlb.open()
		brlb.set('window.title=d-gen; font: unifont-8.0.01.ttf, size=12x12; window.size=64x64;')
		brlb.composition(brlb.TK_OFF)
		brlb.refresh()
		for y in range(len(self.map_list)):
			for x in range(len(self.map_list[y])):
				if self.map_list[y][x].water:
					brlb.color(brlb.color_from_argb(255, 0, 0, 255))
				elif self.map_list[y][x].connector:
					brlb.color(brlb.color_from_argb(255, 255, 0, 0))
				else:
					brlb.color(brlb.color_from_argb(255, 255, 255, 255))
				if self.map_list[y][x].type == 1:
					brlb.put(x, y, '.')
				elif self.map_list[y][x].type == 2:
					brlb.put(x, y, 9608)
				elif self.map_list[y][x].type == 3:
					brlb.put(x, y, '#')
				elif self.map_list[y][x].type == 4:
					brlb.put(x, y, 9618)
				elif self.map_list[y][x].type == 0:
					brlb.put(x, y, 'O')
				elif self.map_list[y][x].type == 5:
					brlb.color(brlb.color_from_argb(255, 255, 255, 0))
					brlb.put(x, y, 'X')
		for room in self.rooms:
			brlb.color(brlb.color_from_argb(255, 0, 255, 255))
			brlb.put(room.midpoint[0], room.midpoint[1], 9673)
		brlb.refresh()
		closed = False
		while closed != brlb.TK_CLOSE:
			if brlb.has_input():		
				closed = brlb.read()

	def debug_refresh(self):
		for y in range(len(self.map_list)):
			for x in range(len(self.map_list[y])):
				if self.map_list[y][x].water:
					brlb.color(brlb.color_from_argb(255, 0, 0, 255))
				elif self.map_list[y][x].connector:
					brlb.color(brlb.color_from_argb(255, 255, 0, 0))
				else:
					brlb.color(brlb.color_from_argb(255, 255, 255, 255))
				if self.map_list[y][x].type == 1:
					brlb.put(x, y, '.')
				elif self.map_list[y][x].type == 2:
					brlb.put(x, y, 9608)
				elif self.map_list[y][x].type == 3:
					brlb.put(x, y, '#')
				elif self.map_list[y][x].type == 4:
					brlb.put(x, y, 9618)
				elif self.map_list[y][x].type == 0:
					brlb.put(x, y, 'O')
				elif self.map_list[y][x].type == 5:
					brlb.color(brlb.color_from_argb(255, 255, 255, 0))
					brlb.put(x, y, 'X')
		brlb.refresh()
		closed = False
		while closed != brlb.TK_CLOSE and closed != brlb.TK_SPACE:
			if brlb.has_input():			
				closed = brlb.read()
				if closed == brlb.TK_CLOSE:
					brlb.close()

	def discover(self, room):
		for wall in room.walls:
			self.map_list[wall[1]][wall[0]].seen = True
			self.map_list[wall[1]][wall[0]].visible = True
			self.map_list[wall[1]][wall[0]].light = 5
		for tile in room.tiles:
			self.map_list[tile[1]][tile[0]].seen = True
			self.map_list[tile[1]][tile[0]].visible = True
			self.map_list[tile[1]][tile[0]].light = 5

class Line():
	def __init__(self, p0, p1):
		self.octants = {0: self.to_zero_from_zero, 1: self.to_one_from_zero, 2: self.to_two_from_zero, 3: self.to_three_from_zero, 4: self.to_four_from_zero, 5: self.to_five_from_zero, 6: self.to_six_from_zero, 7: self.to_seven_from_zero}
		self.x0, self.y0 = p0
		self.x1, self.y1 = p1
		self.p0 = p0
		self.p1 = p1
		# self.points = self.plot_line()
		# self.points_continuous = self.plot_line_continuous()

	def calculate_slope(self):
		return (self.x1 - self.x0),(self.y1 - self.y0)

	def to_zero_from_zero(self, x, y):
		return (x, y)

	def to_one_from_zero(self, x, y):
		return (y, x)

	def to_two_from_zero(self, x, y):
		return (-y, x)

	def to_three_from_zero(self, x, y):
		return (-x, y)

	def to_four_from_zero(self, x, y):
		return (-x, -y)

	def to_five_from_zero(self, x, y):
		return (-y, -x)

	def to_six_from_zero(self, x, y):
		return (y, -x)

	def to_seven_from_zero(self, x, y):
		return (x, -y)

	def plot_line_continuous(self):
		indices = []
		if self.x1 == self.x0 or self.y1 == self.y0 or abs(self.x1 - self.x0) == abs(self.y1 - self.y0):
			x = self.x0
			y = self.y0
			dx = self.x1 - x
			dy = self.y1 - y
			while x != self.x1 or y != self.y1:
				# print(x, y)
				indices.append((x, y))
				if dx != 0 and dy != 0:
					indices.append((x + int(dx/abs(dx)), y))
				if dx != 0:
					x += int(dx/abs(dx))
				if dy != 0:
					y += int(dy/abs(dy))
			indices.append((self.x1, self.y1))
			self.length = len(indices)
			return indices
		octant = self.octant()
		x0, y0 = self.to_zero(octant, self.x0, self.y0)
		x1, y1 = self.to_zero(octant, self.x1, self.y1)
		self.dx = x1 - x0
		self.dy = y1 - y0
		y = y0
		self.D = self.dy - self.dx
		for x in range(x0, x1):
			if self.D >= 0:
				indices.append((x, y))
				y += 1
				self.D -= self.dx
			self.D += self.dy
			indices.append((x, y))
		indices.append((x1, y1))
		self.length = len(indices)
		return [self.from_zero(octant, x, y) for (x, y) in indices]

	def plot_line(self):
		indices = []
		if self.x1 == self.x0 or self.y1 == self.y0 or abs(self.x1 - self.x0) == abs(self.y1 - self.y0):
			x = self.x0
			y = self.y0
			dx = self.x1 - x
			dy = self.y1 - y
			while x != self.x1 or y != self.y1:
				indices.append((x, y))
				if dx != 0:
					x += int(dx/abs(dx))
				if dy != 0:
					y += int(dy/abs(dy))
			indices.append((self.x1, self.y1))
			self.length = len(indices)
			return indices
		octant = self.octant()
		x0, y0 = self.to_zero(octant, self.x0, self.y0)
		x1, y1 = self.to_zero(octant, self.x1, self.y1)
		self.dx = x1 - x0
		self.dy = y1 - y0
		y = y0
		self.D = self.dy - self.dx
		for x in range(x0, x1):
			if self.D >= 0:
				y += 1
				self.D -= self.dx
			self.D += self.dy
			indices.append((x, y))
		indices.append((x1, y1))
		self.length = len(indices)
		return [self.from_zero(octant, x, y) for (x, y) in indices]

	def from_zero(self, octant, x, y):
		return self.octants[octant](x, y)

	def to_zero(self, octant, x, y):
		if octant == 0:
			return (x, y)
		if octant == 1:
			return (y, x)
		if octant == 2:
			return (y, -x)
		if octant == 3:
			return (-x, y)
		if octant == 4:
			return (-x, -y)
		if octant == 5:
			return (-y, -x)
		if octant == 6:
			return (-y, x)
		if octant == 7:
			return (x, -y)

	def octant(self):
		dx = self.x1 - self.x0
		dy = self.y1 - self.y0
		if dx > 0:
			if dy > 0:
				if dy > dx:
					return 1
				else:
					return 0
			else:
				if abs(dy) < dx:
					return 7
				else:
					return 6
		else:
			if dy > 0:
				if dy > abs(dx):
					return 2
				else:
					return 3
			else:
				if abs(dy) > abs(dx):
					return 5
				else:
					return 4

	def intersects(self, line):
		endpoints = (max(self.p1.x, line.p1.x), min(self.p2.x, line.p2.x))
		endpoints = (self.f(x) - line.f(x) for x in endpoints)
		if min(endpoints) <= 0 and max(endpoints) >= 0:
			return True
		return False


class Tile:
	def __init__(self, tile_type, water):
		self.type = tile_type
		self.water = water
		self.light = 0
		self.visible = False
		self.seen = False
		self.region = -1
		self.connector = False
		self.occupant = False

	def light_level(self):
		return min(self.light, 5)

	def luminosity(self):
		if not self.visible:
			return 4278203136
		return LUMINOSITY[self.light_level()]


class Room():
	def __init__(self, p1, p2, p3, p4):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.p4 = p4
		self.walls = self.make_walls()
		self.midpoint = (round_up((self.p1[0] + self.p2[0] + self.p3[0] + self.p4[0])/4), round_up((self.p1[1] + self.p2[1] + self.p3[1] + self.p4[1])/4))
		self.fix()
		self.region = -1
		
	def fix(self):
		self.tile()
		self.walls = self.trim_walls(self.walls)

	def make_walls(self):
		walls = []
		walls.extend(Line(self.p1, self.p2).plot_line_continuous())
		walls.extend(Line(self.p2, self.p3).plot_line_continuous())
		walls.extend(Line(self.p3, self.p4).plot_line_continuous())
		walls.extend(Line(self.p4, self.p1).plot_line_continuous())
		return set(walls)

	def intercepts(self, room):
		for wall in room.walls:
			if wall in self.tiles:
				return True
		for wall in self.walls:
			if wall in room.tiles:
				return True
		return False

	def fill(self, x, y):
		if not (x, y) in self.walls and not (x, y) in self.tiles:
			self.tiles.add((x, y))
		for i in range(3):
			for j in range(3):
				if not (x + i - 1, y + j -1) in self.tiles and not (x + i - 1, y + j -1) in self.walls:
					self.fill(x + i - 1, y + j -1)

	def tile(self):
		self.tiles = set()
		self.fill(*self.midpoint)
		return None

	def tile_map(self, level_map):
		for x, y in self.walls:
			level_map[y][x] = Tile(2, False)
		for x, y in self.tiles:
			level_map[y][x] = Tile(1, False)

	def trim_walls(self, walls):
		good_walls = set()
		for wall in walls:
			if self.near_room(wall):
				good_walls.add(wall)		
		return good_walls

	def near_room(self, p):
		for x in range(3):
			for y in range(3):
				if (p[0] + x - 1, p[1] + y -1) in self.tiles:
					return True
		return False

	def in_bounds(self, lbound, hbound):
		if max(max(self.p2), max(self.p3), max(self.p4)) >= hbound or min(min(self.p1), min(self.p2), min(self.p4)) < lbound:
			return False
		return True

	def in_this_room(self, p):
		return tuple(p) in self.tiles		

class Game():
	def __init__(self, tutorial=False):

		self.log = Log()	
		self.dungeons = []
		self.gods = []
		self.inventories = []
		self.descend(game_start=True)
		self.initialise_screen()
		self.KEYPAD_BINDS = {brlb.TK_KP_8: "up", brlb.TK_KP_2: "down", brlb.TK_KP_4: "left", brlb.TK_KP_6: "right", brlb.TK_KP_5: "stay"}
		self.ARROW_BINDS = {brlb.TK_UP: "up", brlb.TK_DOWN: "down", brlb.TK_LEFT: "left", brlb.TK_RIGHT: "right", brlb.TK_SPACE: "stay"}		
		self.WASD_BINDS = {brlb.TK_W: "up", brlb.TK_S: "down", brlb.TK_A: "left", brlb.TK_D: "right", brlb.TK_SPACE: "stay"}
		self.MOVEMENTS = {"up": self.up, "down": self.down, "left": self.left, "right": self.right, "stay": self.stay}
		self.MOVEMENT_BINDS = {0: self.WASD_BINDS, 1: self.ARROW_BINDS, 2: self.KEYPAD_BINDS}
		if tutorial:
			run = self.tutorial()
		if not run:
			return
		print(self.character)
		for i in range(25):
			print(self.character.xp_for_level(i+1))
		self.character.inventory.set_dims(self.screen_x, self.screen_y)
		self.character.set_dims(self.screen_x, self.screen_y)
		self.state = "game"
		print('finished setup')
		self.run()

	def descend(self, game_start=False):
		self.log.update()
		if game_start:
			new_floor = True
		else:
			new_floor = self.dungeons.index(self.dungeon) == len(self.dungeons) - 1
		if not game_start and new_floor:
			self.dungeons.append(Dungeon(len(self.dungeons) + 1, name=self.dungeon.name))
			self.dungeon = self.dungeons[-1]
		elif not game_start:
			self.dungeon = self.dungeons[self.dungeons.index(self.dungeon) + 1]
		else:
			self.dungeons.append(Dungeon(len(self.dungeons) + 1, name=False))
			self.dungeon = self.dungeons[-1]
		self.log.log('Welcome to level {l} of '.format(l=self.dungeon.level) + self.dungeon.name)
		if not game_start and new_floor:
			self.gods.append(God(self.dungeon, self.character))
			self.god = self.gods[-1]
		elif not game_start:
			self.god = self.gods[self.gods.index(self.god) + 1]
			self.character.pos = self.dungeon.start
			self.god.characters[0] = self.character
		else:
			self.gods.append(God(self.dungeon))
			self.god = self.gods[-1]
			self.character = self.god.get_char_by_id(0)
		if new_floor:
			self.inventories.append(Inventory())
			self.inventory = self.inventories[-1]
		else:
			self.inventory = self.inventories[self.inventories.index(self.inventory)]
		self.circle = False
		self.current_room = False
		self.update_light()

	def ascend(self):
		self.log.update()
		if not self.dungeons.index(self.dungeon) == 0:
			self.dungeon = self.dungeons[self.dungeons.index(self.dungeon) - 1]
			self.character.pos = self.dungeon.destination
			self.log.log('Welcome to level {l} of '.format(l=self.dungeon.level) + self.dungeon.name)
			self.god = self.gods[self.gods.index(self.god) - 1]
			self.inventory = self.inventories[self.inventories.index(self.inventory) - 1]
			self.circle = False
			self.current_room = False
			self.update_light()
		else:
			self.log.log('You are already on the top floor')

	def tutorial(self):
		control_names = ['WASD', 'the arrow keys', 'the numpad']
		title = "Choose controls:"
		a_choice = 4*' ' + "1) WASD"
		b_choice = 4*' ' + "2) Arrow keys"
		c_choice = 4*' ' + "3) Numpad"
		choices = (a_choice, b_choice, c_choice)
		start_x = self.screen_x//2 - len(b_choice)//2
		start_y = self.screen_y//2 - 2
		brlb.printf(start_x, start_y, title)
		brlb.printf(start_x, start_y + 1, a_choice)
		brlb.printf(start_x, start_y + 2, b_choice)
		brlb.printf(start_x, start_y + 3, c_choice)
		brlb.refresh()
		key = False
		self.controls = -1
		while key != brlb.TK_ENTER or self.controls == -1:
			if brlb.has_input():
				key = brlb.read()
				if key == brlb.TK_CLOSE:
					return False 
				elif key == brlb.TK_1:
					self.controls = 0
				elif key == brlb.TK_2:
					self.controls = 1
				elif key == brlb.TK_3:
					self.controls = 2
				start_x = self.screen_x//2 - len(b_choice)//2
				start_y = self.screen_y//2 - 2
				brlb.color(4294967295)
				brlb.printf(start_x, start_y, title)
				for i in range(len(choices)):
					if i == self.controls:
						brlb.color(4294950481)
					else:
						brlb.color(4294967295)
					brlb.printf(start_x, start_y + i + 1, choices[i])
				brlb.refresh()
		self.MOVEMENT_BINDS = self.MOVEMENT_BINDS[self.controls]
		brlb.clear()
		brlb.color(4294967295)
		intro = "This is you"
		continue_prompt = "press any key to continue"
		intro_running = True
		brlb.printf(self.screen_x//2 - len(intro)//2, self.screen_y//2 - 2, intro)
		brlb.put(self.screen_x//2, self.screen_y//2, '@')
		brlb.printf(self.screen_x//2 - len(continue_prompt)//2, self.screen_y//2 + 2, continue_prompt)
		brlb.refresh()
		while intro_running:
			brlb.set("input.filter = [keyboard, close]")
			if brlb.has_input():
				key = brlb.read()
				if key == brlb.TK_CLOSE:
					return False
				else:
					print(key)
					intro_running = False
				brlb.printf(self.screen_x//2 - len(intro)//2, self.screen_y//2 - 2, intro)
				brlb.put(self.screen_x//2, self.screen_y//2, '@')
				brlb.printf(self.screen_x//2 - len(continue_prompt)//2, self.screen_y//2 + 2, continue_prompt)
				brlb.refresh()
		brlb.set("input.filter = []")
		brlb.clear()
		if self.controls == 2:
			still = "Press 5 to stand still for a turn."
		elif self.controls < 2:
			still = "Press space to stand still for a turn."
		intro = "Use " + control_names[self.controls] + ' to move. ' + still
		continue_prompt = "press escape to continue"
		intro_running = True
		pos = [self.screen_x//2, self.screen_y//2]
		brlb.printf(self.screen_x//2 - len(intro)//2, self.screen_y//2 - 2, intro)
		brlb.printf(self.screen_x//2 - len(continue_prompt)//2, self.screen_y//2 + 2, continue_prompt)
		brlb.put(pos[0], pos[1], '@')
		brlb.refresh()
		while intro_running:
			if brlb.has_input():
				brlb.clear()
				key = brlb.read()
				if key == brlb.TK_CLOSE:
					return False
				if key == brlb.TK_ESCAPE:
					intro_running = False
				if key in list(self.MOVEMENT_BINDS.keys()):
					if self.MOVEMENT_BINDS[key] == "up":
						pos[1] -= 1
					if self.MOVEMENT_BINDS[key] == "down":
						pos[1] += 1
					if self.MOVEMENT_BINDS[key] == "left":
						pos[0] -= 1
					if self.MOVEMENT_BINDS[key] == "right":
						pos[0] += 1
				brlb.printf(self.screen_x//2 - len(intro)//2, self.screen_y//2 - 2, intro)
				brlb.printf(self.screen_x//2 - len(continue_prompt)//2, self.screen_y//2 + 2, continue_prompt)
				brlb.put(pos[0], pos[1], '@')
				brlb.refresh()
		brlb.clear()
		intro = "You are trapped in {d}. You must fight to stay alive. Survive as long as you can and try to escape.".format(d=self.dungeon.name)
		intro_lines = []
		length = int(self.screen_x*0.61803398875)
		while len(intro) > length:
			intro_lines.append(intro[:intro.rfind(' ', 0, length)])
			intro = intro[intro.rfind(' ', 0, length) + 1:]
		intro_lines.append(intro)
		continue_prompt = "press escape to continue"
		intro_running = True
		pos = [self.screen_x//2 - length//2, self.screen_y//2 - len(intro_lines)//2]
		for line_index in range(len(intro_lines)):
			brlb.printf(pos[0], pos[1] + line_index, intro_lines[line_index])
		brlb.printf(self.screen_x//2 - len(continue_prompt)//2, pos[1] + len(intro_lines) + 1, continue_prompt)
		brlb.refresh()
		while intro_running:
			if brlb.has_input():
				key = brlb.read()
				if key == brlb.TK_CLOSE:
					return False
				if key == brlb.TK_ESCAPE:
					intro_running = False
				for line_index in range(len(intro_lines)):
					brlb.printf(pos[0], pos[1] + line_index, intro_lines[line_index])
				brlb.printf(self.screen_x//2 - len(continue_prompt)//2, pos[1] + len(intro_lines) + 1, continue_prompt)
				brlb.refresh()
		while intro_running:
			if brlb.has_input():
				key = brlb.read()
				if key == brlb.TK_CLOSE:
					return False
				if key == brlb.TK_ESCAPE:
					intro_running = False
				for line_index in range(len(intro_lines)):
					brlb.printf(pos[0], pos[1] + line_index, intro_lines[line_index])
				brlb.printf(self.screen_x//2 - len(continue_prompt)//2, pos[1] + len(intro_lines) + 1, continue_prompt)
				brlb.refresh()
		brlb.set("input.filter = []")
		return True

	def unobstructed(self, coords, dest):
		coords.remove(dest)
		for x, y in coords:
			if self.dungeon.map_list[y][x].type in WALL_TILES:
				return False
		return True

	def initialise_screen(self):
		brlb.open()
		print('opened')
		monitors = screeninfo.get_monitors()
		monitor = sorted(monitors, key=lambda x: x.height * x.width, reverse=True)[0]
		print(monitor.width, monitor.height)
		self.screen_y = int(monitor.height*0.61803398875//16)
		self.screen_x = int(monitor.width*0.61803398875//8)
		print('calculated screen size')		
		print(self.screen_x, self.screen_y)
		brlb.set('window.title="{d}"; font: unifont-8.0.01.ttf, size=12; window.size={w}x{h};'.format(d=self.dungeon.name, w=self.screen_x, h=self.screen_y))
		print('configured')
		brlb.composition(brlb.TK_OFF)
		# brlb.refresh()


	def run(self):
		closed = False
		self.update_light()
		self.draw()
		while closed == False:
			# brlb.refresh()
			if brlb.has_input():
				closed = self.on_move_events()

		return 0
	
	def draw_fullcircle(self, center, r):
		x = r
		y = 0
		err = 0
		indices = []
		while x >= y:
			# indices.extend(Line((self.character.pos[0] + x, self.character.pos[1] + y), (self.character.pos[0] - x, self.character.pos[1] + y)).plot_line())
			# indices.extend(Line((self.character.pos[0] + y, self.character.pos[1] + x), (self.character.pos[0] - y, self.character.pos[1] + x)).plot_line())
			# indices.extend(Line((self.character.pos[0] + y, self.character.pos[1] - x), (self.character.pos[0] - y, self.character.pos[1] - x)).plot_line())
			# indices.extend(Line((self.character.pos[0] + x, self.character.pos[1] - y), (self.character.pos[0] - x, self.character.pos[1] - y)).plot_line())
			indices.append((center[0] + x, center[1] + y))
			indices.append((center[0] + y, center[1] + x))
			indices.append((center[0] + y, center[1] - x))
			indices.append((center[0] + x, center[1] - y))
			indices.append((center[0] - x, center[1] + y))
			indices.append((center[0] - y, center[1] + x))
			indices.append((center[0] - y, center[1] - x))
			indices.append((center[0] - x, center[1] - y))
			y += 1
			err += 1 + 2*y
			if 2*(err - x) + 1 > 0:
				x -= 1
				err += 1 - 2*x
		indices.extend(self.fill(center[0], center[1], indices))
		# print('finished filling')
		return indices

	def fill(self, x, y, bounds):
		# print('filling')
		potential_pos = set()
		potential_pos.add((x, y))
		new_pos = set()
		filled_pos = []
		tried_pos = set()
		while len(potential_pos) > 0:
			potential_pos.update(new_pos)
			potential_pos.difference_update(tried_pos)
			for x, y in potential_pos:
				if not (x, y) in bounds:
					new_pos.add((x-1, y))
					new_pos.add((x+1, y))
					new_pos.add((x, y-1))
					new_pos.add((x, y+1))
					filled_pos.append((x, y))
				tried_pos.add((x, y))
		return filled_pos

	def stay(self, x, y):
		self.player_action = True
		return x, y

	def up(self, x, y):
		y -= 1
		if self.dungeon.map_list[y][x].type in WALL_TILES:
			return (x, y + 1)
		self.player_action = True
		self.log.update()
		if self.dungeon.map_list[y][x].occupant:
			enemy = self.dungeon.map_list[y][x].occupant
			damage = self.character.attack(enemy)
			self.log.log(self.character.name.capitalize() + ' attacked ' + enemy.name + ', dealing ' + str(damage) + ' damage')
			if enemy.hp <= 0:
				self.log.log(enemy.name + ' died')
				self.log.log('You gained ' + str(enemy.xp_worth) + ' xp')
				self.character.xp += enemy.xp_worth
				self.inventory.drop(self.god.enemy_types[enemy.type]["attributes"]["drops"], enemy.level, enemy.pos)
				self.god.kill(enemy.id)
			return (x, y + 1)
		self.dungeon.map_list[y][x].occupant = self.character
		self.dungeon.map_list[y + 1][x].occupant = False
		return (x, y)

	def down(self, x, y):
		y += 1
		if self.dungeon.map_list[y][x].type in WALL_TILES:	
			return (x, y - 1)
		self.player_action = True
		self.log.update()
		if self.dungeon.map_list[y][x].occupant:
			enemy = self.dungeon.map_list[y][x].occupant
			damage = self.character.attack(enemy)
			self.log.log(self.character.name.capitalize() + ' attacked ' + enemy.name + ', dealing ' + str(damage) + ' damage')
			if enemy.hp <= 0:
				self.log.log(enemy.name + ' died')
				self.log.log('You gained ' + str(enemy.xp_worth) + ' xp')
				self.character.xp += enemy.xp_worth
				self.inventory.drop(self.god.enemy_types[enemy.type]["attributes"]["drops"], enemy.level, enemy.pos)
				self.god.kill(enemy.id)			
			return (x, y - 1)
		self.dungeon.map_list[y][x].occupant = self.character
		self.dungeon.map_list[y - 1][x].occupant = False
		return (x, y)

	def right(self, x, y):
		x += 1
		if self.dungeon.map_list[y][x].type in WALL_TILES:
			return (x - 1, y)
		self.player_action = True
		self.log.update()
		if self.dungeon.map_list[y][x].occupant:
			enemy = self.dungeon.map_list[y][x].occupant
			damage = self.character.attack(enemy)
			self.log.log(self.character.name.capitalize() + ' attacked ' + enemy.name + ', dealing ' + str(damage) + ' damage')
			if enemy.hp <= 0:
				self.log.log(enemy.name + ' died')
				self.log.log('You gained ' + str(enemy.xp_worth) + ' xp')
				self.character.xp += enemy.xp_worth
				self.inventory.drop(self.god.enemy_types[enemy.type]["attributes"]["drops"], enemy.level, enemy.pos)
				self.god.kill(enemy.id)			
			return (x - 1, y)
		self.dungeon.map_list[y][x].occupant = self.character
		self.dungeon.map_list[y][x - 1].occupant = False
		return (x, y)

	def left(self, x, y):
		x -= 1
		if self.dungeon.map_list[y][x].type in WALL_TILES:
			return (x + 1, y)
		self.player_action = True
		self.log.update()
		if self.dungeon.map_list[y][x].occupant:
			enemy = self.dungeon.map_list[y][x].occupant
			damage = self.character.attack(enemy)
			self.log.log(self.character.name.capitalize() + ' attacked ' + enemy.name + ', dealing ' + str(damage) + ' damage')
			if enemy.hp <= 0:
				self.log.log(enemy.name + ' died')
				self.log.log('You gained ' + str(enemy.xp_worth) + ' xp')
				self.character.xp += enemy.xp_worth
				self.inventory.drop(self.god.enemy_types[enemy.type]["attributes"]["drops"], enemy.level, enemy.pos)
				self.god.kill(enemy.id)
			return (x + 1, y)
		self.dungeon.map_list[y][x].occupant = self.character
		self.dungeon.map_list[y][x + 1].occupant = False
		return (x, y)

	def move(self, key):
		return self.MOVEMENTS[self.MOVEMENT_BINDS[key]](self.character.pos[0], self.character.pos[1])

	def translate_to_screen(self, x, y):
		return (x - self.character.pos[0] + self.screen_x//2, y - self.character.pos[1] + self.screen_y//2)

	def distance(self, p1, p2):
		return sum([abs(p1[i] - p2[i])**2 for i in range(2)])**(1/2)

	def update_light(self):
		if self.circle:
			for x, y in self.circle:
				if self.dungeon.in_bounds(x, y):
					self.dungeon.map_list[y][x].visible = False
					self.dungeon.map_list[y][x].light = 0
		if self.current_room:
			if self.current_room.in_this_room(self.character.pos):
				self.dungeon.discover(self.current_room)
			else:
				self.dungeon.darken(self.current_room)
				self.current_room = False
		if not self.current_room:
			for room in self.dungeon.rooms:
				if room.in_this_room(self.character.pos):
					self.dungeon.discover(room)
					self.current_room = room
					break
		self.circle = self.draw_fullcircle(self.character.pos, 16)
		# print('drew the circle!')
		for x, y in self.circle:
			if self.dungeon.in_bounds(x, y):
				if not self.dungeon.map_list[y][x].type == 0:			
					if not self.dungeon.map_list[y][x].visible:
						line = Line(self.character.pos, (x, y))
						points = line.plot_line()
						# points.append((x, y))
						tile = self.dungeon.map_list[y][x]
						if self.unobstructed(points, (x, y)):
							tile.seen = True
							tile.visible = True
							tile.light += 1
							if line.length > 12:
								tile.light += 1
							elif line.length > 8:
								tile.light += 2
							elif line.length > 4:
								tile.light += 3
							elif line.length <= 4:
								tile.light += 4
							for index in range(len(points)):
								i, j = points[len(points) - index - 1]
								# i, j = points[index]
								tile = self.dungeon.map_list[j][i]
								if not tile.visible:
									tile.seen = True
									tile.visible = True
									tile.light += 1
									if line.length - index > 12:
										tile.light += 1
									elif line.length - index > 8:
										tile.light += 2
									elif line.length - index > 4:
										tile.light += 3
									elif line.length - index <= 4:
										tile.light += 4
								else:
									break

	def unequip(self, item, character):
		for equipment in self.character.equipment_keys:
			if character.equipment[equipment] == item:
				character.equipment[equipment] = False
		item.equipped = False



	def equip(self, item, character, location=False):
		if item.equipped:
			self.unequip(item, character)
		elif location:
			if character.equipment[location].info["equip"] == "2hand":
				character.equipment["lhand"].equipped = False
				character.equipment["rhand"].equipped = False
				character.equipment["lhand"] = False
				character.equipment["rhand"] = False
			else:
				character.equipment[location].equipped = False
			character.equipment[location] = item
			item.equipped = True
		elif item.info["equip"] == "2hand":
			if character.equipment["lhand"]:
				character.equipment["lhand"].equipped = False
			if character.equipment["rhand"]:
				character.equipment["rhand"].equipped = False
			character.equipment["lhand"] = item
			character.equipment["rhand"] = item
			item.equipped = True
		elif item.info["equip"] == "1hand":
			if not character.equipment["rhand"]:
				character.equipment["rhand"] = item
				item.equipped = True
			elif not character.equipment["lhand"]:
				character.equipment["lhand"] = item
				item.equipped = True
			else:
				character.inventory.choose_equip = True
				character.inventory.equip_choices = ["lhand", "rhand"]
		elif item.info["equip"] == "body":
			if character.equipment["body"]:
				character.equipment["body"].equipped = False
			character.equipment["body"] = item
			item.equipped = True
		elif item.info["equip"] == "head":
			if character.equipment["head"]:
				character.equipment["head"].equipped = False
			character.equipment["head"] = item
			item.equipped = True

	def on_move_events(self):
		# brlb.refresh()
		self.draw()
		self.player_action = False
		key = brlb.read()
		if key == brlb.TK_CLOSE:
			return True
		if self.state == "game":
			if key in list(self.MOVEMENT_BINDS.keys()):
				self.character.pos = self.move(key)
				if self.MOVEMENT_BINDS[key] != "stay":
					self.update_light()
			elif self.character.pos == self.dungeon.destination:
				if brlb.state(brlb.TK_SHIFT):
					if key == brlb.TK_PERIOD:
						self.descend()
			elif self.character.pos == self.dungeon.start:
				if brlb.state(brlb.TK_SHIFT):
					if key == brlb.TK_COMMA:
						self.ascend()
		if self.state == "inventory":
			if self.character.inventory.choose_equip:
				if key in list(self.MOVEMENT_BINDS.keys()):
					if self.MOVEMENT_BINDS[key] == "left":
						self.equip(self.character.inventory.items[self.character.inventory.item - 1 + (self.character.inventory.page - 1) * self.character.inventory.list_height], self.character, location=self.character.inventory.equip_choices[0])
						self.character.inventory.choose_equip = False
					elif self.MOVEMENT_BINDS[key] == "right":
						self.equip(self.character.inventory.items[self.character.inventory.item - 1 + (self.character.inventory.page - 1) * self.character.inventory.list_height], self.character, location=self.character.inventory.equip_choices[1])
						self.character.inventory.choose_equip = False
			elif key in list(self.MOVEMENT_BINDS.keys()):
				self.character.inventory.select_menu = False
				if self.MOVEMENT_BINDS[key] == "left":
					self.character.inventory.page = max(1, self.character.inventory.page - 1)
					self.character.inventory.item = 1
				elif self.MOVEMENT_BINDS[key] == "right":
					self.character.inventory.page = min(self.character.inventory.pages, self.character.inventory.page + 1)
					self.character.inventory.item = self.character.inventory.list_height * (self.character.inventory.page - 1) + 1
				elif self.MOVEMENT_BINDS[key] == "up":
					self.character.inventory.item = max(1, self.character.inventory.item - 1)
				elif self.MOVEMENT_BINDS[key] == "down":
					self.character.inventory.item = min(min(self.character.inventory.list_height, len(self.character.inventory.items) - (self.character.inventory.page - 1) * self.character.inventory.list_height), self.character.inventory.item + 1)
			elif len(self.character.inventory.items) > 0:
				if key == brlb.TK_ENTER and not self.character.inventory.select_menu:
					self.character.inventory.select_menu = not self.character.inventory.select_menu
					# self.character.inventory.menu_x, self.character.inventory.menu_y = brlb.state(brlb.TK_MOUSE_X), brlb.state(brlb.TK_MOUSE_Y)
				elif key == brlb.TK_ENTER and self.character.inventory.select_menu:
					self.equip(self.character.inventory.items[self.character.inventory.item - 1 + (self.character.inventory.page - 1) * self.character.inventory.list_height], self.character)
					self.character.inventory.select_menu = not self.character.inventory.select_menu
		if key == brlb.TK_I:
			self.character.inventory.select_menu = False
			self.character.inventory.show = not self.character.inventory.show
			self.character.show_equipment = False
			if self.character.inventory.show:
				self.state = "inventory"
			else:
				self.state = "game"
		if key == brlb.TK_E:
			self.character.show_equipment = not self.character.show_equipment
			self.character.inventory.show = False
			if self.character.show_equipment:
				self.state = "equipment"
			else:
				self.state = "game"
		if key == brlb.TK_ESCAPE:
			self.character.inventory.show = False
			self.character.show_equipment = False
			self.character.inventory.select_menu = False
			self.state = "game"
			# print(self.character.inventory.show)
		# for x, y in circle:
		# 	if self.dungeon.in_bounds(x, y):
		# 		if self.dungeon.map_list[y][x].visible:
		# 			for i, j in SIDES:
		# 					if self.dungeon.in_bounds(x + i, y + j):
		# 						if self.dungeon.map_list[y + j][x + i].visible:
		# 							self.dungeon.map_list[y][x].light += 1
		
		if self.player_action:
			if self.god.turn():
				pass
				# print(len(self.god.characters))
				# print('\n'.join([str(character) for character in self.god.characters]))
			character_turn = self.character.turn()
			if character_turn:
				self.log.log(self.character.name + character_turn)
			while self.character.xp > self.character.next_level:
				self.character.level += 1
				self.log.log(self.character.name + ' are now level ' + str(self.character.level))
				self.character.next_level = self.character.xp_for_level(self.character.level)
			# print(len(self.god.characters))
			
			for character in self.god.characters:
				if character.hp <= 0:
					self.log.log(character.name + ' died')
					self.god.kill(character.id)
				# elif self.distance(character.pos, self.character.pos) <= 10 and self.distance(character.pos, self.character.pos) > 1:
				elif self.dungeon.map_list[character.pos[1]][character.pos[0]].visible and self.distance(character.pos, self.character.pos) > 1:
					trail = self.pathfind(character.pos, self.character.pos)
					if not self.dungeon.map_list[trail[1][1]][trail[1][0]].occupant:
						self.dungeon.map_list[character.pos[1]][character.pos[0]].occupant = False
						character.pos = trail[1]
						self.dungeon.map_list[character.pos[1]][character.pos[0]].occupant = character
				elif self.distance(character.pos, self.character.pos) == 1:
					damage = character.attack(self.character)
					self.log.log(character.name + ' attacked ' + self.character.name + ', dealing ' + str(damage) + ' damage')
			if self.character.hp <= 0:
				self.log.log(self.character.name.capitalize() + ' died')
				self.log.log(self.character.name.capitalize() + ' killed ' + str(sum([len(god.killed_ids) for god in self.gods])) + ' enemies')
				self.end_game() 
			moved_ids = []
			for item in self.inventory.items:
				# print(item.info["location"], self.character.pos)
				if item.info["location"] == self.character.pos:
					# print(item.info["name"])
					self.log.log(self.character.name + ' picked up ' + item.info["name"])
					self.inventory.move(self.character.inventory, item.id)
					moved_ids.append(item.id)
			for item_id in moved_ids:
				self.inventory.remove(item_id)
		return False

	def draw(self):	
		brlb.clear()
		self.log.show(self.screen_x - 40, 0)
		self.character.inventory.refresh()
		self.character.refresh()
		brlb.layer(0)
		for y in range(len(self.dungeon.map_list)):
			for x in range(len(self.dungeon.map_list[y])):
				if self.dungeon.map_list[y][x].type == BG_TILE:
					pass
				elif self.dungeon.map_list[y][x].type in WALL_TILES and self.dungeon.map_list[y][x].visible:
					pos = self.translate_to_screen(x, y)
					brlb.color(self.dungeon.map_list[y][x].luminosity())
					brlb.put(pos[0], pos[1], 9608)
				elif self.dungeon.map_list[y][x].type in FLOOR_TILE and self.dungeon.map_list[y][x].visible:
					pos = self.translate_to_screen(x, y)
					brlb.color(self.dungeon.map_list[y][x].luminosity())
					brlb.put(pos[0], pos[1], '.')					
				elif self.dungeon.map_list[y][x].type in HALL_TILE and self.dungeon.map_list[y][x].visible:
					pos = self.translate_to_screen(x, y)
					brlb.color(self.dungeon.map_list[y][x].luminosity())
					brlb.put(pos[0], pos[1], '.')
				elif self.dungeon.map_list[y][x].type in DOOR_TILE and self.dungeon.map_list[y][x].visible:
					pos = self.translate_to_screen(x, y)
					brlb.color(self.dungeon.map_list[y][x].luminosity())
					brlb.put(pos[0], pos[1], 'X')
				elif self.dungeon.map_list[y][x].type in WALL_TILES and self.dungeon.map_list[y][x].seen:
					pos = self.translate_to_screen(x, y)
					brlb.color(self.dungeon.map_list[y][x].luminosity())
					brlb.put(pos[0], pos[1], 9608)
				elif self.dungeon.map_list[y][x].type in FLOOR_TILE and self.dungeon.map_list[y][x].seen:
					pos = self.translate_to_screen(x, y)
					brlb.color(self.dungeon.map_list[y][x].luminosity())
					brlb.put(pos[0], pos[1], '.')					
				elif self.dungeon.map_list[y][x].type in HALL_TILE and self.dungeon.map_list[y][x].seen:
					pos = self.translate_to_screen(x, y)
					brlb.color(self.dungeon.map_list[y][x].luminosity())
					brlb.put(pos[0], pos[1], '.')
				elif self.dungeon.map_list[y][x].type in DOOR_TILE and self.dungeon.map_list[y][x].seen:
					pos = self.translate_to_screen(x, y)
					brlb.color(self.dungeon.map_list[y][x].luminosity())
					brlb.put(pos[0], pos[1], 'X')
		pos = self.translate_to_screen(*self.dungeon.start)
		brlb.color(brlb.pick_color(pos[0], pos[1], 0))
		brlb.put(pos[0], pos[1], '↑')
		# print(self.distance(self.character.pos, self.dungeon.destination))
		pos = self.translate_to_screen(*self.dungeon.destination)
		brlb.color(brlb.pick_color(pos[0], pos[1], 0))
		brlb.put(pos[0], pos[1], '↓')
		brlb.composition(brlb.TK_ON)
		for item in self.inventory.items:
			if self.dungeon.map_list[item.info["location"][1]][item.info["location"][0]].visible:
				pos = self.translate_to_screen(*item.info["location"])
				brlb.clear_area(pos[0], pos[1], 1, 1)
		for item in self.inventory.items:
			if self.dungeon.map_list[item.info["location"][1]][item.info["location"][0]].visible:
				pos = self.translate_to_screen(*item.info["location"])
				# print(item.info["colour"])
				brlb.color(item.info["colour"] + self.dungeon.map_list[item.info["location"][1]][item.info["location"][0]].light_level()*51*256**3)
				# print(self.dungeon.map_list[item.info["location"][1]][item.info["location"][0]].light_level()*51*255**3)
				brlb.put(pos[0], pos[1], item.info["key"])
		brlb.composition(brlb.TK_OFF)
		for character in self.god.characters[1:]:
			if self.dungeon.map_list[character.pos[1]][character.pos[0]].visible:
				pos = self.translate_to_screen(*character.pos)
				# brlb.clear_area(pos[0], pos[1], 1, 1)
				brlb.color(brlb.color_from_argb(self.dungeon.map_list[character.pos[1]][character.pos[0]].light_level()*51, 255, 0, 0))
				brlb.put(pos[0], pos[1], character.attributes['key'])	
		brlb.color(brlb.color_from_argb(255, 255, 255, 255))
		brlb.clear_area(0, 0, len(str(self.character.hp)), 1)
		brlb.printf(0, 0, 'HP: ' + str(int(self.character.hp)))
		# brlb.clear_area(self.screen_x//2, self.screen_y//2, 1, 1)
		brlb.put(self.screen_x//2, self.screen_y//2, '@')
		brlb.refresh()
		return 0

	def get_path(self, path_dict, end, start):
		path = [end]
		point = end
		while point != start:
			path.append(path_dict[point])
			point = path_dict[point]
		return path[::-1]

	def end_game(self):
		self.MOVEMENT_BINDS = {}
		print(self.character.inventory)


	def pathfind(self, a, b):
		a = tuple(a)
		b = tuple(b)
		# print(a, b)
		frontier = [(a, 0)]
		came_from = {}
		cost_so_far = {a: 0}
		for i in range(8192):
			current = frontier.pop(0)[0]
			if current == b:
				break
			for side in SIDES:
				side = tuple([side[i] + current[i] for i in range(2)])
				if not self.dungeon.map_list[side[1]][side[0]].type in WALL_TILES:
					new_cost = cost_so_far[current] + 1
					if self.dungeon.map_list[side[1]][side[0]].occupant:
						new_cost += 6
					if side not in list(cost_so_far.keys()) or new_cost < cost_so_far[side]:
						cost_so_far[side] = new_cost
						priority = new_cost + abs(side[0] - b[0]) + abs(side[1] - b[1])
						frontier.append((side, priority))
						frontier = sorted(frontier, key=lambda x: x[1])
						came_from[side] = current
		return self.get_path(came_from, b, a)

class Item():
	def __init__(self, item_id, item_info):
		self.id = item_id
		self.info = item_info
		self.equipped = False

	def __str__(self):
		item_string = ''
		item_string += self.info['name']
		item_string += ': ' + str(self.info)
		return item_string

	def __repr__(self):
		return self.__str__()

class Handler():
	def __init__(self):
		self.used_ids = set()
		self.last_id = -1

	def get_id(self):
		self.last_id += 1
		self.used_ids.add(self.last_id)
		return self.last_id


class Inventory(Handler):
	def __init__(self, width=False, height=False):
		super().__init__()
		self.item_source = json.load(open('items.json', encoding='utf-8'))
		self.materials = json.load(open('materials.json', encoding='utf-8'))
		self.mat_abbr = {'m': 'metallic', 'w':'wooden', 'f': 'flexible', 'p':'precious'}
		self.display_keys = {"name": "Name", "key": "Key", "mat": "Material"}
		self.key_order = ["name", "key", "mat"]
		self.equip_names = {"head": "Head", "body": "Body", "lhand": "Left Hand", "rhand": "Right Hand"}
		self.items = []
		self.show = False
		self.select_menu = False
		self.choose_equip = False
		self.selection = 0
		self.width = width
		self.height = height
		self.menu_x = 0
		self.menu_y = 0
		self.page = 1
		self.item = 1	

	def set_dims(self, w, h):
		self.width = w
		self.height = h
		self.start_x = int(self.width*0.125)
		self.start_y = int(self.height*0.125)
		self.menu_x = self.width // 2
		self.list_height = int(self.height*0.875) - self.start_y - 3

	def refresh(self, width=False, height=False):
		# print(self.show)
		# self.items = sorted(self.items, key=lambda x: x.info["name"])
		self.pages = max(int(ceiling(len(self.items) / (int(self.height*0.875) - self.start_y - 3), 0)), 1)
		if width:
			self.width = width
			self.start_x = int(self.width*0.125)
			self.menu_x = self.width // 2
		if height:
			self.height = height
			self.start_y = int(self.height*0.125)
			self.list_height = int(self.height*0.875) - self.start_y - 3
		brlb.color(brlb.color_from_argb(227, 25, 25, 25))
		if self.show:
			# print(self.pages)
			# print('displaying')
			brlb.layer(2)
			for x in range(self.start_x, int(self.width*0.875)):
				for y in range(self.start_y, int(self.height*0.875)):
					brlb.put(x, y, 9608)
			if len(self.items) > 0:
				brlb.layer(3)
				brlb.color(brlb.color_from_argb(255, 255, 255, 255))
				for index in range(min(len(self.items) - (self.page - 1) * self.list_height, self.list_height)):
					if index + 1 == self.item:
						for key_index in range(len(self.key_order)):
							brlb.color(4294967295)
							attribute = self.display_keys[self.key_order[key_index]] + ': '
							for c in range(len(attribute)):
								brlb.put(self.width // 2 + c, self.start_y + 1 + key_index, attribute[c])
							if self.key_order[key_index] == "key":
								brlb.color(self.items[index + (self.page - 1) * self.list_height].info["colour"] + 255*256**3)
							key_length = len(attribute) - 1
							attribute = str(self.items[index + (self.page - 1) * self.list_height].info[self.key_order[key_index]])
							for c in range(len(attribute)):
								brlb.put(self.width // 2 + key_length + c, self.start_y + 1 + key_index, attribute[c])
						brlb.color(4294967295)
						key_index = len(self.key_order)
						for key in sorted(list(self.items[index + (self.page - 1) * self.list_height].info["stats"].keys())):
							attribute = key + ': ' + str(self.items[index + (self.page - 1) * self.list_height].info["stats"][key])
							for c in range(len(attribute)):
								brlb.put(self.width // 2 + c, self.start_y + 1 + key_index, attribute[c])
							key_index += 1
						self.menu_x = self.width // 2
						self.menu_y = self.start_y + 1 + key_index
						brlb.color(4294967295)
						brlb.put(self.menu_x, self.menu_y, 9484)
						for i in range(5):
							brlb.put(self.menu_x + 1 + i, self.menu_y, 9472)
						brlb.put(self.menu_x + 6, self.menu_y, 9488)
						brlb.put(self.menu_x, self.menu_y + 1, 9474)
						if self.selection == 0 and self.select_menu:
							brlb.color(4294950481)
						brlb.printf(self.menu_x + 1, self.menu_y + 1, 'Equip')
						brlb.color(4294967295)
						brlb.put(self.menu_x + 6, self.menu_y + 1, 9474)
						brlb.put(self.menu_x, self.menu_y + 2, 9492)
						for i in range(5):
							brlb.put(self.menu_x + 1 + i, self.menu_y + 2, 9472)
						brlb.put(self.menu_x + 6, self.menu_y + 2, 9496)
						if self.choose_equip:
							brlb.printf(self.menu_x, self.menu_y + 4, '(LEFT) ' + self.equip_names[self.equip_choices[0]] + ' | (RIGHT) ' + self.equip_names[self.equip_choices[1]])
						brlb.color(4294950481)
					else:
						brlb.color(4294967295)
					if self.items[index + (self.page - 1) * self.list_height].equipped:
						brlb.put(self.start_x, self.start_y + 1 + index, 'E')
					for c in range(len(self.items[index + (self.page - 1) * self.list_height].info["name"])):
						brlb.put(self.start_x + 2 + c, self.start_y + 1 + index, self.items[index + (self.page - 1) * self.list_height].info["name"][c])
				page_numbers = ' '.join([str(i + 1) for i in range(self.pages)])
				for c in range(len(page_numbers)):
					if page_numbers[c] == str(self.page):
						brlb.color(4294950481)
					else:
						brlb.color(4294967295)
					brlb.put(self.width//2 - len(page_numbers)//2 + c, int(self.height*0.875) - 2, page_numbers[c])
				# if self.show_menu:




	def get_item_by_id(self, item_id):
		if item_id in self.used_ids:
			for item in self.items:
				if item.id == item_id:
					return item
		return False

	def material_roll(self):
		if random.random() > 0.25:
			return round_rand((random.random()*5 + 1 + random.random()*5 + 1)/2)
		else:
			return random.randint(1, 6)

	def choose(self, group):
		hierarchy = r_key_search(group, self.item_source)	
		while random.randrange(10) == 0 and len(hierarchy) > 1:
			hierarchy.pop()
		choices = get_from_path(json.load(open('items.json', encoding='utf-8')), hierarchy)
		# print(choices)
		# while "name" not in list(choices.keys()):
		# 		choices = choices[random.choice(list(choices.keys()))]
		try:
			while "name" not in list(choices.keys()):
				choices = choices[random.choice(list(choices.keys()))]
		except (ValueError, IndexError) as e:
			print('WTF!!!!', choices, hierarchy, e)
		return choices

	def roll_stat(self, base, level, material_tier):
		roll = random.uniform((level / 2), (level * 1.5))
		return max(0, round(roll + (base + level * (material_tier - 3.5)), 2))

	def item_smith(self, item_info, level, location):
		
		try:
			if "mat" in list(item_info.keys()):
				if item_info["mat"]:
					# print(item_info)
					material_tier = self.material_roll()
					mat_type = item_info["mat"]
					material = random.choice(list(self.materials[self.mat_abbr[mat_type]][str(material_tier)].keys()))
					item_info["mat"] = material
					item_info["name"] = material + " " + item_info["name"]
					item_info["mat_tier"] = material_tier
					item_info["colour"] = int(self.materials[self.mat_abbr[mat_type]][str(material_tier)][material], 16)
				else:
					item_info["mat_tier"] = 3.5
					item_info["colour"] = int(item_info["colour"], 16)
		except (ValueError, IndexError) as e:
			print('WTF!!!!', item_info, e)
		item_info["name"] += " [" + str(level) + "]"
		item_info["level"] = level
		for stat in list(item_info["stats"].keys()):
			if stat in ["skl", "wgt"]:
				item_info["stats"][stat] = ceiling(random.uniform(0.75*item_info["stats"][stat], 1.25*item_info["stats"][stat]))
			else:
				item_info["stats"][stat] = self.roll_stat(item_info["stats"][stat], level, item_info["mat_tier"])
		item_info["location"] = location
		item = Item(self.get_id(), item_info)
		self.items.append(item)
		return item

	def drop(self, drop_table, level, location):
		drops = []
		for drop in drop_table:
			# print(drop)
			chance = drop["chance"]
			# chance *= 4
			if chance >= 100:
				drops.append(self.item_smith(self.choose(drop["type"]), level, location))
				chance /= 2
			while random.randrange(100) < chance:
				drops.append(self.item_smith(self.choose(drop["type"]), level, location))
				chance /= 1.5
		return drops

	def remove(self, item_id):
		for item in self.items:
			if item.id == item_id:
				return self.items.pop(self.items.index(item))

	def move(self, inventory, item_id):
		inventory.items.append(self.get_item_by_id(item_id))


	def __str__(self):
		return ',\n'.join([str(item) for item in self.items])

class Character():
	def __init__(self, char_id, level, char_type, stats, attributes, name, x, y):
		self.id = char_id
		self.pos = (x, y)
		self.stats = stats
		self.attributes = attributes
		self.type = char_type
		self.level = level
		self.hp = self.stats['hp']
		self.name = name.capitalize()
		self.inventory = Inventory()
		self.equipment = {"head": False, "body": False, "lhand": False, "rhand": False}
		self.equipment_keys = ["head", "body", "lhand", "rhand"]
		self.current_equipment = 0
		self.show_equipment = False
		print('xp:', (sum(list(self.stats.values()))/33 + self.level)/3)
		self.xp_worth = ceiling((sum(list(self.stats.values()))/33 + self.level)/3, -2)
		print('xp rounded:', self.xp_worth)
		self.xp = 0
		self.next_level = self.xp_for_level(self.level)

	def xp_for_level(self, level):
		if level == 1:
			return 7
		xp = 0
		x = 0
		for i in range(level):
			x += i**1.05*5.4 - i**0.5 + 3
		return int(7 + x)

	def attack(self, target):
		basedamage = 30
		print(target.name, 'def:', target.get_stat('def'))
		print(self.name, 'str:', self.get_stat('str'))
		damage = ceiling(((2*self.level + 10)* self.get_stat('str')*basedamage/(250*target.get_stat('def')) + 2) * random.uniform(0.85, 1))
		damage_no_items = ceiling(((2*self.level + 10)* self.stats['str']*basedamage/(250*target.stats['def']) + 2) * random.uniform(0.85, 1))
		print('Items:', damage)
		print('No items:', damage_no_items, '\n')
		target.hp -= damage
		return damage

	def get_stat(self, stat):
		total = 0
		for key in self.equipment_keys:
			if self.equipment[key]:
				if stat in list(self.equipment[key].info["stats"].keys()):
					# print(self.equipment[key].info["stats"][stat])
					total += self.equipment[key].info["stats"][stat]
		total += self.stats[stat]
		return round(total, 2)

	# def attack(self, target):
	# 	min_damage = max(self.level/10, round(random.random()*self.level/5, 1))
	# 	roll = (random.random() + random.random())/2
	# 	mult = ((self.stats['str'] + target.stats['def'])/8)
	# 	print('roll:', roll)
	# 	damage = roll*mult
	# 	mitigation = (self.stats['str'] - target.stats['def'])/2
	# 	damage = damage + mitigation
	# 	print('raw damage:', damage)
	# 	print('min damage:', min_damage)
	# 	while damage < 0:
	# 		damage += min_damage
	# 	print('damage:', damage)
	# 	print('target def:', target.stats['def'])
	# 	print('self str:', self.stats['str'])
		
	# 	target.hp -=  max(0.1, round(damage, 1))
	# 	return max(0.1, round(damage, 1))

	def __str__(self):
		objdict = {'ID': hex(self.id), 'type': str(self.type), 'level': self.level, 'location': self.pos, 'name': self.name}
		return ', '.join([key + ': ' + str(self.stats[key]) for key in list(self.stats.keys())] + [key + ': ' + str(objdict[key]) for key in list(objdict.keys())])

	def turn(self):
		roll = random.randrange(self.stats['end'])
		oldhp = self.hp
		self.hp += roll/100
		self.hp = min(self.stats['hp'], self.hp)
		if oldhp != self.hp and self.hp == self.stats['hp']:
			return ' have returned to normal health'
		return False

class Player(Character):
	def __init__(self, char_id, level, char_type, stats, attributes, name, x, y):
		super().__init__(char_id, level, char_type, stats, attributes, name, x, y)


	def set_dims(self, w, h):
		self.width = w
		self.height = h
		self.start_x = int(self.width*0.125)
		self.start_y = int(self.height*0.125)
		self.list_height = int(self.height*0.875) - self.start_y - 3


	def refresh(self, width=False, height=False):
		# print(self.show)
		if width:
			self.width = width
			self.start_x = int(self.width*0.125)
		if height:
			self.height = height
			self.start_y = int(self.height*0.125)
			self.list_height = int(self.height*0.875) - self.start_y - 3
		brlb.color(brlb.color_from_argb(227, 25, 25, 25))
		if self.show_equipment:
			# print(self.pages)
			# print('displaying')
			brlb.layer(2)
			for x in range(self.start_x, int(self.width*0.875)):
				for y in range(self.start_y, int(self.height*0.875)):
					brlb.put(x, y, 9608)
			brlb.layer(3)
			brlb.color(brlb.color_from_argb(255, 255, 255, 255))
			brlb.printf(self.width // 2 - 6, self.start_y + 1, "Head: ")
			if self.equipment["head"]:
				for c in range(len(self.equipment["head"].info["name"])):
					brlb.put(self.width // 2 + c, self.start_y + 1, self.equipment["head"].info["name"][c])
			brlb.printf(self.width // 2 - 6, self.start_y + 2, "Body: ")
			if self.equipment["body"]:
				for c in range(len(self.equipment["body"].info["name"])):
					brlb.put(self.width // 2 + c, self.start_y + 2, self.equipment["body"].info["name"][c])
			brlb.printf(self.width // 2 - 11, self.start_y + 3, "Left Hand: ")
			if self.equipment["lhand"]:
				for c in range(len(self.equipment["lhand"].info["name"])):
					brlb.put(self.width // 2 + c, self.start_y + 3, self.equipment["lhand"].info["name"][c])
			brlb.printf(self.width // 2 - 12, self.start_y + 4, "Right Hand: ")
			if self.equipment["rhand"]:
				for c in range(len(self.equipment["rhand"].info["name"])):
					brlb.put(self.width // 2 + c, self.start_y + 4, self.equipment["rhand"].info["name"][c])

class Enemy(Character):
	def __init__(self, char_id, level, char_type, stats, attributes, name, x, y):
		super().__init__(char_id, level, char_type, stats, attributes, name, x, y)


class God(Handler):
	def __init__(self, dungeon, character=False):
		super().__init__()
		self.killed_ids = set()
		self.dungeon = dungeon
		self.keys = {'e': 'enders', 'v': 'vowels', 'c': 'consonants', 'o': 'connectors'}
		self.names = json.load(open('names.json', encoding='utf-8'))
		self.sums = {key:sum([self.names[self.keys[key]][k] for k in list(self.names[self.keys[key]].keys())]) for key in list(self.keys.keys())}
		self.enemy_types = json.load(open('enemies.json', encoding='utf-8'))
		self.stats = ["def", "dex", "end", "eva", "hp", "int", "mag", "spd", "str", "wis"]
		self.player_level = 3
		self.characters = []
		if not character:
			self.spawn(user=True)
		else:
			self.characters.append(character)
			self.dungeon.map_list[self.dungeon.start[1]][self.dungeon.start[0]].occupant = character
			character.pos = self.dungeon.start
			del self.enemy_types['player'] 
		self.populate()

	def get_char_by_id(self, char_id):
		if char_id in self.used_ids:
			for character in self.characters:
				if character.id == char_id:
					return character
		return False

	def roll_stat(self, base, level):
		roll = random.randrange(1, 4)
		return int(roll + (base + 10) // 2 + level * 3)

	def random_name(self):
		structures = [random.choice(self.names['structures']) for i in range(random.randrange(1, 5))]
		name = ''
		structures = ''.join(structures)
		structures = structures.replace('ec', 'eoc')
		for c in structures:
			name += p_choice(self.names[self.keys[c]], self.sums[c])
		# print(name)
		return name

	def generate_stats(self, enemy_type, level):
		stats = {}
		for stat in self.stats:
			stats[stat] = self.roll_stat(self.enemy_types[enemy_type][stat] , level)
		return stats

	def spawn(self, user=False):
		if not user:
			room = random.choice(self.dungeon.rooms)
			point = random.choice(list(room.tiles))
			if not self.dungeon.map_list[point[1]][point[0]].visible:
				level = round_up((randint(round_up(self.dungeon.level*0.9),round_up(self.dungeon.level*1.1)) + randint(round_up(self.dungeon.level*0.9),round_up(self.dungeon.level*1.1)))/2)
				enemy_type = random.choice(list(self.enemy_types.keys()))
				enemy = Enemy(self.get_id(), level, enemy_type, self.generate_stats(enemy_type, level), self.enemy_types[enemy_type]["attributes"], self.random_name(), *point)
				self.characters.append(enemy)
				print(enemy.stats)
				print(enemy.type)
				print(enemy.level, '\n')
				self.dungeon.map_list[point[1]][point[0]].occupant = enemy
			else:
				return self.spawn()
		else:
			point = self.dungeon.start
			player = Player(self.get_id(), 1, 'player', self.generate_stats('player', 1), self.enemy_types['player']['attributes'], 'you', *point)
			del self.enemy_types['player']
			self.characters.append(player)
			self.dungeon.map_list[point[1]][point[0]].occupant = player

	def kill(self, char_id):
		character = self.get_char_by_id(char_id)
		self.killed_ids.add(character)
		self.dungeon.map_list[character.pos[1]][character.pos[0]].occupant = False
		self.characters.remove(character)

	def turn(self):
		attempts = max(1, len(self.dungeon.rooms) - len(self.characters))
		for i in range(attempts):
			if random.randrange(50) == 0:
				self.spawn()
				return True
		return False

	def populate(self):
		for i in range(random.randrange(12, 42)):
			self.turn()

class Log():
	def __init__(self, starting_info=False):
		self.history = []
		self.new_info = 0
		if starting_info:
			self.log(starting_info)

	def update(self):
		self.new_info = 0	

	def log(self, info):
		self.new_info += 1
		if len(info) > 40:
			split = info.rfind(' ', 0, 40)
			overflow = info[split:]
			info = info[:split]
			self.history.append(info)
			self.log(overflow)
		else:
			self.history.append(info)
		if len(self.history) > 7:
			self.history.pop(0)
		

	def show(self, x, y):
		brlb.layer(1)
		# print('showing log')
		for i in range(len(self.history)):
			if len(self.history) - i <= self.new_info:
				brlb.color(4294950481)
			else:
				brlb.color(4294967295)
			for c in range(len(self.history[i])):
				brlb.put(x+c, y+i, self.history[i][c])


BG_TILE = 0
FLOOR_TILE = set([1])
WALL_TILES = set([2, 4])
HALL_TILE = set([3])
DOOR_TILE = set([5])
# print(brlb.color_from_argb(255, 204, 204, 204))
SIDES = [(1, 0), (-1, 0), (0, 1), (0, -1)]
LUMINOSITY = [16777215, 872415231, 1728053247, 2583691263, 3439329279, 4294967295]

# with PyCallGraph(output=GraphvizOutput()):
# 	Game()
# inv = Inventory()
# my_god = God(Dungeon(1))
# for i in range(100):
# 	enemy_type = random.choice(list(my_god.enemy_types.keys()))
# 	print(enemy_type, ':', inv.drop(my_god.enemy_types[enemy_type]["attributes"]["drops"], 1))
Game(tutorial=True)