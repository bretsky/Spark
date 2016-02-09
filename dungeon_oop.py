import sys
import random
import pygame
from pygame.locals import *
from time import clock as get_time

# sys.dont_write_bytecode = True
# Not sure if necessary
WIN = pygame.event.Event(pygame.USEREVENT)
LOSE = pygame.event.Event(pygame.USEREVENT)
BG_TILE = 0
FLOOR_TILE = 1
WALL_TILE = 2
HALL_TILE = 3

class Game():
	def __init__(self):
		self.dungeon = Dungeon()
		self.character = Character()
		self.initialise_screen()
		self.create_tiles()
		char_room = self.dungeon.rooms[0]
		self.character.pos = [char_room.x1 + random.randrange(0, char_room.width), char_room.y1 + random.randrange(0, char_room.height)]
		end_room = self.dungeon.rooms[random.randrange(1, len(self.dungeon.rooms))]
		self.destination = [end_room.x1 + random.randrange(0, end_room.width), end_room.y1 + random.randrange(0, end_room.height)]
		self.enemies = Enemies()
		self.enemies.create_enemies(self.dungeon, self.character)
		self.run()

	def create_tiles(self):
		tile_size = self.tile_size
		self.floor_tile = pygame.Surface((tile_size, tile_size)).convert()
		self.floor_tile.fill((30, 16, 3))
		self.wall_tile = pygame.Surface((tile_size, tile_size)).convert()
		self.wall_tile.fill((63, 63, 63))
		self.bg_tile = pygame.Surface((tile_size, tile_size)).convert()
		self.bg_tile.fill((70, 45, 10))
		self.water_tile = pygame.Surface((tile_size, tile_size)).convert()
		self.water_tile.fill((16, 16, 160))
		self.hall_tile = pygame.Surface((tile_size, tile_size)).convert()
		self.hall_tile.fill((148, 120, 78))
		self.character_tile = pygame.Surface((tile_size, tile_size)).convert()
		self.character_tile.fill((255, 255, 255))
		self.destination_tile = pygame.Surface((tile_size, tile_size)).convert()
		self.destination_tile.fill((255, 0, 0))
		self.enemy_tile = pygame.Surface((tile_size,tile_size)).convert()
		self.enemy_tile.fill((255, 255, 0))
		self.start_tile = pygame.Surface((tile_size, tile_size)).convert()
		self.start_tile.fill((0, 255, 0))
		self.dead_tile = pygame.Surface((tile_size, tile_size)).convert()
		self.dead_tile.fill((255, 128, 0))
		self.health_pixel = pygame.Surface((1,2)).convert()
		self.health_pixel.fill((255,0,0))
		tile_type_list = [self.bg_tile, self.floor_tile, self.wall_tile, self.hall_tile]
		self.tile_list = []
		for tile in tile_type_list:
			alpha_list = []
			for alpha in range(256):
				x_tile = tile.copy()
				x_tile.set_alpha(alpha)
				alpha_list.append(x_tile)
			self.tile_list.append(alpha_list)

	def initialise_screen(self):
		pygame.init()
		infoObject = pygame.display.Info()
		print(infoObject.current_h)
		self.screen_x = 128*int((infoObject.current_h-72.0)/128.0)
		print(self.screen_x)
		self.screen_y = self.screen_x
		self.tile_size = int(self.screen_x/128)
		self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
		pygame.display.set_caption(self.dungeon.name)
		self.screen_bg = pygame.Surface((self.screen_x, self.screen_y)).convert()
		self.screen_bg.fill((0, 0, 0))

	def run(self):
		screen = self.screen
		tile_size = self.tile_size
		screen_bg = self.screen_bg
		print_go = True
		jumped_this_turn = False
		jump_wait_counter = 0
		jump_time = False
		get_time()
		frame_counter = 0
		seconds = 2
		w_accel = 1
		a_accel = 1
		s_accel = 1
		d_accel = 1
		w_time = False
		a_time = False
		s_time = False
		d_time = False
		jump_midpoint = False
		framerate = pygame.time.Clock()
		self.on_move_events()
		while print_go == True:
			framerate.tick(60)
			frame_time = framerate.get_time()
			if get_time() >= seconds:
				print(framerate.get_fps())
				seconds += 2
			if jumped_this_turn:
				if not jump_time:
					jump_time = pygame.time.get_ticks()
				if pygame.time.get_ticks()-jump_time >= 250 and not jump_midpoint:
					jump_midpoint = True
					print('Enemy moves during recovery')
					self.on_move_events()
				if pygame.time.get_ticks()-jump_time >= 500:
					jumped_this_turn = False
					jump_time = False
					jump_midpoint = False
					print('Recovery Done')
			screen.blit(screen_bg, (0,0))
			counter = 0
			for y in self.dungeon.map_list:
				x_counter = 0
				for x in y:
					if x.light:
						if x.visible:
							alpha = x.light
						else:
							alpha = round(x.light/2)
						screen.blit(self.tile_list[x.type][alpha], (x_counter*tile_size, counter*tile_size))
					x_counter+=1
				counter += 1
			x_tile = self.destination_tile
			if self.dungeon.map_list[self.destination[1]][self.destination[0]].visible:
				x_tile.set_alpha(self.dungeon.map_list[self.destination[1]][self.destination[0]].light)
			else:
				x_tile.set_alpha(self.dungeon.map_list[self.destination[1]][self.destination[0]].light/2)
			screen.blit(x_tile, (self.destination[0]*tile_size, self.destination[1]*tile_size))
			screen.blit(self.character_tile, (self.character.pos[0]*tile_size, self.character.pos[1]*tile_size))
			for enemy in range(len(self.enemies.dying_locations)):
				enemy_location = self.enemies.dying_locations[enemy]
				x_tile = self.dead_tile
				x_tile.set_alpha(min(self.dungeon.map_list[enemy_location[1]][enemy_location[0]].light,255.0-(255.0*(self.enemies.dying_enemies[enemy].check_if_dead())/45.0)))
				if self.dungeon.map_list[enemy_location[1]][enemy_location[0]].visible:
					screen.blit(x_tile, (enemy_location[0]*tile_size, enemy_location[1]*tile_size))
			for enemy in self.enemies.locations:				
				x_tile = self.enemy_tile
				if self.dungeon.map_list[enemy[1]][enemy[0]].light:
					x_tile.set_alpha(self.dungeon.map_list[enemy[1]][enemy[0]].light)
					if self.dungeon.map_list[enemy[1]][enemy[0]].visible:
						screen.blit(x_tile, (enemy[0]*tile_size, enemy[1]*tile_size))
			for pixel in range(round(self.screen_x*self.character.health/self.character.max_health)):
				screen.blit(self.health_pixel, (pixel, 0))
			pygame.display.update()
			self.events = pygame.event.get()
			self.key = pygame.key.get_pressed()
			self.move_speed = 1
			mods = pygame.key.get_mods()
			if mods & KMOD_SHIFT:
				self.move_speed = 2
			for event in self.events:
				if event.type == pygame.QUIT:
					return
				if event == WIN:
					return
				if event == LOSE:
					return
				if not jumped_this_turn:
					if event.type == MOUSEBUTTONUP and event.button == 1:
						position = pygame.mouse.get_pos()
						position = [int(x/tile_size) for x in position]
						print(position)
						if position in self.enemies.locations:
							if position[0] > self.character.pos[0]-2 and position[0] < self.character.pos[0]+2:
								if position[1] > self.character.pos[1]-2 and position[1] < self.character.pos[1]+2:
									self.enemies.damage(self.enemies.locations.index(position), 1)
									print('Attack successful')
									self.on_move_events()
				if event.type == pygame.KEYDOWN:
					if not jumped_this_turn:
						if event.key == pygame.K_w or event.key == pygame.K_UP:
							if self.dungeon.map_list[self.character.pos[1]-self.move_speed][self.character.pos[0]].type != 2 and self.dungeon.map_list[self.character.pos[1]-1][self.character.pos[0]].type != 2:
								if not [self.character.pos[0],self.character.pos[1]-self.move_speed] in self.enemies.locations:
									self.character.pos[1] -= self.move_speed
									print('Moved')
									if self.move_speed == 2:
										jumped_this_turn = True
										print('You jumped')
									self.on_move_events()
					if not jumped_this_turn:
						if event.key == pygame.K_s or event.key == pygame.K_DOWN:
							if self.dungeon.map_list[self.character.pos[1]+self.move_speed][self.character.pos[0]].type != 2 and self.dungeon.map_list[self.character.pos[1]+1][self.character.pos[0]].type != 2:
								if not [self.character.pos[0],self.character.pos[1]+self.move_speed] in self.enemies.locations:
									self.character.pos[1] += self.move_speed
									print('Moved')
									if self.move_speed == 2:
										jumped_this_turn = True
										print('You jumped')
									self.on_move_events()									
					if not jumped_this_turn:
						if event.key == pygame.K_a or event.key == pygame.K_LEFT:
							if self.dungeon.map_list[self.character.pos[1]][self.character.pos[0]-self.move_speed].type != 2 and self.dungeon.map_list[self.character.pos[1]][self.character.pos[0]-1].type != 2:
								if not [self.character.pos[0]-self.move_speed,self.character.pos[1]] in self.enemies.locations:
									self.character.pos[0] -= self.move_speed
									print('Moved')
									if self.move_speed == 2:
										jumped_this_turn = True
										print('You jumped')
									self.on_move_events()									
					if not jumped_this_turn:			
						if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
							if self.dungeon.map_list[self.character.pos[1]][self.character.pos[0]+self.move_speed].type != 2 and self.dungeon.map_list[self.character.pos[1]][self.character.pos[0]+1].type != 2:
								if not [self.character.pos[0]+self.move_speed,self.character.pos[1]] in self.enemies.locations:
									self.character.pos[0] += self.move_speed
									print('Moved')
									if self.move_speed == 2:
										jumped_this_turn = True
										print('You jumped')
									self.on_move_events()									
					if event.key == pygame.K_SPACE:
						return
			if not jumped_this_turn:
				if self.key[pygame.K_w] or self.key[pygame.K_UP]:
					if not w_time:
						w_time = pygame.time.get_ticks()
					w_time_val = (pygame.time.get_ticks()-w_time)*w_accel*self.move_speed
					while w_time_val >= 200:
						w_time = False
						w_time_val -= 200
						if self.dungeon.map_list[self.character.pos[1]-1][self.character.pos[0]].type != 2:
							if not [self.character.pos[0],self.character.pos[1]-1] in self.enemies.locations:
								w_accel = 10
								self.character.pos[1] -= 1
								print('Moved')
								self.on_move_events()
				else:
					w_accel = 1
					w_time = False
			if not jumped_this_turn:
				if self.key[pygame.K_s] or self.key[pygame.K_DOWN]:
					if not s_time:
						s_time = pygame.time.get_ticks()
					s_time_val = (pygame.time.get_ticks()-s_time)*s_accel*self.move_speed
					while s_time_val >= 200:
						s_time = False
						s_time_val -= 200
						if self.dungeon.map_list[self.character.pos[1]+1][self.character.pos[0]].type != 2:
							if not [self.character.pos[0],self.character.pos[1]+1] in self.enemies.locations:
								s_accel = 10
								self.character.pos[1] += 1
								print('Moved')
								self.on_move_events()
				else:
					s_accel = 1
					s_time = False
			if not jumped_this_turn:
				if self.key[pygame.K_a] or self.key[pygame.K_LEFT]:
					if not a_time:
						a_time = pygame.time.get_ticks()
					a_time_val = (pygame.time.get_ticks()-a_time)*a_accel*self.move_speed
					while a_time_val >= 200:
						a_time = False
						a_time_val -= 200
						if self.dungeon.map_list[self.character.pos[1]][self.character.pos[0]-1].type != 2:
							if not [self.character.pos[0]-1,self.character.pos[1]] in self.enemies.locations:
								a_accel = 10
								self.character.pos[0] -= 1
								print('Moved')
								self.on_move_events()
				else:
					a_accel = 1
					a_time = False
			if not jumped_this_turn:
				if self.key[pygame.K_d] or self.key[pygame.K_RIGHT]:
					if not d_time:
						d_time = pygame.time.get_ticks()
					d_time_val = (pygame.time.get_ticks()-d_time)*d_accel*self.move_speed
					while d_time_val >= 200:
						d_time = False
						d_time_val -= 200
						if self.dungeon.map_list[self.character.pos[1]][self.character.pos[0]+1].type != 2:
							if not [self.character.pos[0]+1,self.character.pos[1]] in self.enemies.locations:
								d_accel = 10
								self.character.pos[0] += 1
								print('Moved')
								self.on_move_events()
				else:
					d_accel = 1
					d_time = False
		return

	def on_move_events(self):
		print('on_move_events called')
		tile_size = self.tile_size
		self.character.regen_counter
		self.character.regen_rate
		self.character.health
		self.character.max_health
		self.dungeon.map_list
		for y in self.dungeon.map_list:
			for x in y:
				x.set_visible(False)
		for room in self.dungeon.rooms:
			if room.in_this_room(self.character.pos[0], self.character.pos[1]):
				if not room.discovered:
					room.discover()
					for room_y in range(room.height+3):
						for room_x in range(room.width+3):
							for y in range(11):
								for x in range(11):
									light_pos = [room_x-5+x+room.wall_left, room_y-5+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1:
										self.dungeon.map_list[light_pos[1]][light_pos[0]].set_light(15)
							for y in range(9):
								for x in range(9):
									light_pos = [room_x-4+x+room.wall_left, room_y-4+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1: 
										self.dungeon.map_list[light_pos[1]][light_pos[0]].set_light(31)
							for y in range(7):
								for x in range(7):
									light_pos = [room_x-3+x+room.wall_left, room_y-3+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1: 
										self.dungeon.map_list[light_pos[1]][light_pos[0]].set_light(63)
							for y in range(5):
								for x in range(5):
									light_pos = [room_x-2+x+room.wall_left, room_y-2+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1: 
										self.dungeon.map_list[light_pos[1]][light_pos[0]].set_light(127)
							for y in range(3):
								for x in range(3):
									light_pos = [room_x-1+x+room.wall_left, room_y-1+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1: 
										self.dungeon.map_list[light_pos[1]][light_pos[0]].set_light(255)						
							self.dungeon.map_list[room_y+room.wall_top][room_x+room.wall_left].set_light(255)
		for y in range(13):
			for x in range(13):
				light_pos = [self.character.pos[0]-tile_size+x, self.character.pos[1]-tile_size+y]
				if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1: 
					self.dungeon.map_list[light_pos[1]][light_pos[0]].set_light(15)
					self.dungeon.map_list[light_pos[1]][light_pos[0]].set_visible(True)
		for y in range(11):
			for x in range(11):
				light_pos = [self.character.pos[0]-5+x, self.character.pos[1]-5+y]
				if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1:
					self.dungeon.map_list[light_pos[1]][light_pos[0]].set_light(31)
		for y in range(9):
			for x in range(9):
				light_pos = [self.character.pos[0]-4+x, self.character.pos[1]-4+y]
				if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1:
					self.dungeon.map_list[light_pos[1]][light_pos[0]].set_light(63)
		for y in range(7):
			for x in range(7):
				light_pos = [self.character.pos[0]-3+x, self.character.pos[1]-3+y]
				if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1:
					self.dungeon.map_list[light_pos[1]][light_pos[0]].set_light(127)
		for y in range(5):
			for x in range(5):
				light_pos = [self.character.pos[0]-2+x, self.character.pos[1]-2+y]
				if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1:
					self.dungeon.map_list[light_pos[1]][light_pos[0]].set_light(255)
		for y in range(3):
			for x in range(3):
				light_pos = [self.character.pos[0]-1+x, self.character.pos[1]-1+y]
				if light_pos[0] < 128 and light_pos[1] < 128: 
					self.dungeon.map_list[light_pos[1]][light_pos[0]].set_light(255)		
		print('Moved this turn')
		self.character.regen_counter += 1
		if self.character.regen_counter >= self.character.regen_rate:
			if self.character.health >= self.character.max_health:
				self.character.regen_counter = int(self.character.regen_rate/2.0)
			else: 
				self.character.health += int(self.character.regen_counter/self.character.regen_rate)
				print(self.character.health)
				self.character.regen_counter = 0			
		for enemy in self.enemies.locations:
			if enemy[0] > self.character.pos[0]-2 and enemy[0] < self.character.pos[0]+2 and enemy[1] > self.character.pos[1]-2 and enemy[1] < self.character.pos[1]+2:
				print('Imma attack you!')
				self.character.health -= 1
				print(self.character.health)
			elif random.randrange(1,8) != 0:
				if self.dungeon.map_list[enemy[1]][enemy[0]].visible:
					print('Enemy is visible')
					move_horizontal = random.choice([True, False])
					if move_horizontal:
						print('Horizontal movement has priority')
						if enemy[0] < self.character.pos[0] and self.dungeon.map_list[enemy[1]][enemy[0]+1].type != 2 and not [enemy[0]+1, enemy[1]] in self.enemies.locations:
							print('You are to my right')
							enemy[0] += 1
						elif enemy[1] < self.character.pos[1] and self.dungeon.map_list[enemy[1]+1][enemy[0]].type != 2 and not [enemy[0], enemy[1]+1] in self.enemies.locations:
							print('You are below me')
							enemy[1] += 1
						elif enemy[1] > self.character.pos[1] and self.dungeon.map_list[enemy[1]-1][enemy[0]].type != 2 and not [enemy[0], enemy[1]-1] in self.enemies.locations:
							print('You are above me')
							enemy[1] -= 1
						elif enemy[0] > self.character.pos[0] and self.dungeon.map_list[enemy[1]][enemy[0]-1].type != 2 and not [enemy[0]-1, enemy[1]] in self.enemies.locations:
							print('You are to my left')
							enemy[0] -= 1
						else:
							pass
							print('No possible movement')
					if not move_horizontal:
						print('Vertical movement has priority')
						if enemy[1] < self.character.pos[1] and self.dungeon.map_list[enemy[1]+1][enemy[0]].type != 2 and not [enemy[0], enemy[1]+1] in self.enemies.locations:
							print('You are below me')
							enemy[1] += 1
						elif enemy[0] < self.character.pos[0] and self.dungeon.map_list[enemy[1]][enemy[0]+1].type != 2 and not [enemy[0]+1, enemy[1]] in self.enemies.locations:
							print('You are to my right')
							enemy[0] += 1
						elif enemy[0] > self.character.pos[0] and self.dungeon.map_list[enemy[1]][enemy[0]-1].type != 2 and not [enemy[0]-1, enemy[1]] in self.enemies.locations:
							print('You are to my left')
							enemy[0] -= 1
						elif enemy[1] > self.character.pos[1] and self.dungeon.map_list[enemy[1]-1][enemy[0]].type != 2 and not [enemy[0], enemy[1]-1] in self.enemies.locations:
							print('You are above me')
							enemy[1] -= 1
						else:
							pass
							print('No possible movement')
				else:
					print("I'm moving randomly!")
					direction = random.randrange(0,4)
					if direction == 0 and self.dungeon.map_list[enemy[1]][enemy[0]+1].type != 2 and not [enemy[0]+1, enemy[1]] in self.enemies.locations:
						enemy[0] += 1
					if direction == 1 and self.dungeon.map_list[enemy[1]+1][enemy[0]].type != 2 and not [enemy[0], enemy[1]+1] in self.enemies.locations:
						enemy[1] += 1
					if direction == 2 and self.dungeon.map_list[enemy[1]-1][enemy[0]].type != 2 and not [enemy[0], enemy[1]-1] in self.enemies.locations:
						enemy[1] -= 1
					if direction == 3 and self.dungeon.map_list[enemy[1]][enemy[0]-1].type != 2 and not [enemy[0]-1, enemy[1]] in self.enemies.locations:
						enemy[0] -= 1
			else:
				pass
				print("Hurr durr, I'm just gonna sit here")
		if self.character.health <= 0:
			print('You Lose')
			pygame.event.post(LOSE)
		if self.character.pos == self.destination:
			print('You Win!')
			pygame.event.post(WIN)
		self.enemies.check_if_dead()
		print('END TURN\n\n\n\n')

class Character():
	def __init__(self):
		self.position = [0, 0]
		self.health = 10
		self.max_health = 10
		self.regen_rate = 15
		self.regen_counter = 0

class Dungeon():
	def __init__(self):
		self.import_files()
		self.name = self.random_dungeon_name()
		self.map_list = [[Tile(BG_TILE, False) for y in range(128)] for x in range(128)]
		self.corridors_made = 0
		self.rooms = self.make_rooms()
		self.make_corridors()
		self.unfill()
		self.tile_rooms()

	def import_files(self):
		geo_file = open(r'data\dungeon\geographical_features.txt')
		dungeon_attr_file = open(r'data\dungeon\dungeon_attributes.txt')
		dungeon_adj_file = open(r'data\dungeon\dungeon_adjectives.txt')
		dungeon_word_file = open(r'data\dungeon\dungeon_words.txt')
		self.geo_list = geo_file.read().splitlines()
		self.dungeon_attr_list = dungeon_attr_file.read().splitlines()
		self.dungeon_adj_list = dungeon_adj_file.read().splitlines()
		self.dungeon_word_list = dungeon_word_file.read().splitlines()
		print("Possible names: ", len(self.dungeon_word_list)*len(self.geo_list) + len(self.dungeon_adj_list)*len(self.geo_list) + len(self.geo_list)*len(self.dungeon_attr_list) + len(self.dungeon_adj_list)*len(self.geo_list)*len(self.dungeon_attr_list) + len(self.geo_list)*len(self.dungeon_adj_list)*len(self.dungeon_attr_list))

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
		self.unfill()
		fill_start = random.choice(self.rooms)
		self.fill(fill_start.x1, fill_start.y1)
		start_room = fill_start
		destination = random.choice(self.rooms)
		fill_start_pos = [fill_start.x1, fill_start.y1]
		destination_pos = [destination.x1, destination.y1]
		if not self.map_list[destination.y1][destination.x1].water:
			if not destination.intercepts(start_room):
				seed = random.randrange(2)
				self.corridors_made += 1
				if seed == 1:
					y_choices = [start_room.wall_top, start_room.wall_bottom]
					x = random.randrange(start_room.x1, start_room.x2+1)
					y = random.randrange(start_room.y1, start_room.y2+1)
					destination_y = random.randrange(destination.height) + destination.y1
					while y < destination_y:
						self.carve_map(x, y)
						y += 1
					while y > destination_y:
						self.carve_map(x, y)
						y += -1
					while x < destination.x1:
						self.carve_map(x, y)
						x += 1
					while x > destination.x2:
						self.carve_map(x, y)
						x += -1
				if seed == 0:
					x_choices = [start_room.wall_left, start_room.wall_right]
					x = random.randrange(start_room.x1, start_room.x2+1)
					y = random.randrange(start_room.y1, start_room.y2+1)
					destination_x = random.randrange(destination.width) + destination.x1
					while x < destination_x:
						self.carve_map(x, y)
						x += 1
					while x > destination_x:
						self.carve_map(x, y)
						x += -1
					while y < destination.y1:
						self.carve_map(x, y)
						y += 1
					while y > destination.y2:
						self.carve_map(x, y)
						y += -1
				print('Successfully created corridor %(corridor)i' % {'corridor' : self.corridors_made})
			else:
				print('Start and destination were the same, regenerating')
				return self.make_corridors()
		else:
			print('Invalid room pair, regenerating')
			return self.make_corridors()
		self.unfill()
		fill_start = random.choice(self.rooms)
		self.fill(fill_start.x1, fill_start.y1)
		if self.corridors_made > 12:
			self.map_list = [[Tile(0, False) for y in range(128)] for x in range(128)]
			self.rooms = make_rooms()
			self.tile_rooms()
			print('Dungeon was too complex, regenerating')
			self.corridors_made = 0
			return self.make_corridors()
		for y in self.map_list:
			for x in y:
				if x.type == 1 and x.water == False:
					return self.make_corridors()

	def fill(self, x, y):
		if self.map_list[y][x].type == 1 or self.map_list[y][x].type == 3:
			if self.map_list[y][x].water == False:
				self.map_list[y][x].water = True
				self.fill(x-1, y)
				self.fill(x+1, y)
				self.fill(x, y-1)
				self.fill(x, y+1)
		else:
			return

	def unfill(self):
		for x in range(128):
			for y in range(128):
				self.map_list[y][x].water = False

	def random_room(self):
		x = random.randrange(1, 127)
		y = random.randrange(1, 127)
		w = random.randrange(1, 15)
		h = random.randrange(1, 15)
		x2 = x + w
		y2 = y + h
		room = Room(x, x2, y, y2)
		if x2 >= 127 or y2 >= 127:
			return self.random_room()
		for x in self.rooms:
			if room.intercepts(x):
				print('Room conflicted with existing room, regenerating')
				return self.random_room()
		else:
			print('Made room dimensions')
			return room

	def carve_map(self, x, y):
		for row in range(y-1, y+2):
			for column in range(x-1, x+2):
				if self.map_list[row][column].type == 0:
					self.map_list[row][column] = Tile(2, False)
		else:
			self.map_list[y][x] = Tile(3, False)

	def make_rooms(self):
		self.rooms = []
		for x in range(random.randrange(4, 15)):
			room = self.random_room()
			print('Made room %(counter)i' % {'counter' : x + 1})
			self.maplist = room.tile_map(self.map_list)
			self.rooms.append(room)
		self.tile_rooms()
		return self.rooms

	def tile_rooms(self):
		for x in range(128):
			for y in range(128):
				for room in self.rooms:
					if room.in_this_room(x, y):
						self.map_list[y][x] = Tile(1, False)

class Tile:
	def __init__(self, tile_type, water):
		self.type = tile_type
		self.water = water
		self.light = 0
		self.visible = False
	def set_light(self, value):
		if value > self.light:
			self.light = value
	def set_visible(self, visible):
		self.visible = visible

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



class Enemy():
	def __init__(self, monster_type, hp, location, original=False):
		self.type = monster_type
		self.hp = hp
		self.alive = True
		self.turns_dying = 0
		self.x = location[0]
		self.y = location[1]
		self.original = original

	def kill(self):
		self.alive = False

	def check_if_dead(self):
		if not self.alive:
			self.turns_dying += 1
		return self.turns_dying

class Enemies():
	def __init__(self):
		self.count = 0
		self.original_count = 0
		self.alive = 0
		self.dying = 0
		self.dead = 0
		self.locations = []
		self.dying_locations = []
		self.enemies = []
		self.dying_enemies = []

	def place_enemy(self, dungeon, character, original=False):
		enemy_room = random.choice(dungeon.rooms)
		enemy_pos = [enemy_room.x1 + random.randrange(0, enemy_room.width), enemy_room.y1 + random.randrange(0, enemy_room.height)]
		if enemy_pos != character.pos:
			if not enemy_pos in self.locations:
				self.locations.append(enemy_pos)
				self.enemies.append(Enemy('monster', 5, enemy_pos, original))
				self.count += 1
				if original:
					self.original_count += 1
				self.alive += 1
		else:
			self.place_enemy(dungeon, character, original)

	def create_enemies(self, dungeon, character):
		for enemy in range(random.randrange(2,len(dungeon.rooms))):
			self.place_enemy(dungeon, character, True)
		print(self.locations)
		print(self.enemies)

	def damage(self, enemy_index, value):
		enemy = self.enemies[enemy_index]
		enemy.hp -= value
		if enemy.hp <= 0:
			self.kill(enemy_index)

	def kill(self, enemy_index):
		enemy = self.enemies[enemy_index]
		self.dying_enemies.append(enemy)
		self.dying_locations.append(self.locations[enemy_index])
		del self.locations[enemy_index]
		del self.enemies[enemy_index]
		self.alive -= 1
		self.dying += 1
		self.dead += 1
		enemy.kill()

	def check_if_dead(self):
		for i in range(len(self.dying_enemies)):
			turns_dying = self.dying_enemies[i].check_if_dead()
			if turns_dying > 45:
				self.remove(i)

	def remove(self, enemy_index):
		self.dying -= 1
		del self.dying_locations[enemy_index]
		del self.dying_enemies[enemy_index]
		

# dungeon = Dungeon()
# for x in range(100000):
# 	print(dungeon.random_dungeon_name())
game = Game()