import sys
import random
import pygame
from pygame.locals import *
from time import clock

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
		self.character = Character()
		self.dungeon = Dungeon()
		self.create_tiles()


	def create_tiles(self):
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
		tile_type_list = [bg_tile, floor_tile, wall_tile, hall_tile]
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
		print(screen_x)
		self.screen_y = self.screen_x
		self.tile_size = int(screen_x/128)
		self.screen = pygame.display.set_mode((screen_x, screen_y))
		pygame.display.set_caption(self.dungeon.name)
		screen_bg = pygame.Surface((screen_x, screen_y)).convert()
		screen_bg.fill((0, 0, 0))

	def run(self):
		screen = self.screen
		tile_size = self.tile_size
		print_go = True
		jumped_this_turn = False
		jump_wait_counter = 0
		jump_time = False
		time.clock()
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
			if time.clock() >= seconds:
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
					if x.visible:
						alpha = x.light
					else:
						alpha = round(x.light/2)
					screen.blit(self.tile_list[x.type][alpha], (x_counter*tile_size, counter*tile_size))
					x_counter+=1
				counter += 1
			x_tile = self.destination_tile
			if self.dungeon.map_list[destination[1]][destination[0]].visible:
				x_tile.set_alpha(map_list[destination[1]][destination[0]].light)
			else:
				x_tile.set_alpha(map_list[destination[1]][destination[0]].light/2)
			screen.blit(x_tile, (destination[0]*tile_size, destination[1]*tile_size))
			screen.blit(self.character_tile, (character_pos[0]*tile_size, character_pos[1]*tile_size))
			for enemy in self.dead_enemy_locations:
				x_tile = dead_tile
				x_tile.set_alpha(min(self.dungeon.map_list[enemy[1]][enemy[0]].light,255.0-(255.0*(self.dead_enemies[self.dead_enemy_locations.index(enemy)].turns_dead)/45.0)))
				if self.dungeon.map_list[enemy[1]][enemy[0]].visible:
					screen.blit(x_tile, (enemy[0]*tile_size, enemy[1]*tile_size))
			for enemy in self.enemy_locations:				
				x_tile = enemy_tile
				x_tile.set_alpha(self.dungeon.map_list[enemy[1]][enemy[0]].light)
				if map_list[enemy[1]][enemy[0]].visible:
					screen.blit(x_tile, (enemy[0]*tile_size, enemy[1]*tile_size))
			for pixel in range(round(screen_x*character_health/max_character_health)):
				screen.blit(health_pixel, (pixel, 0))
			pygame.display.update()
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
			for event in events:
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
						if position in enemy_locations:
							if position[0] > character_pos[0]-2 and position[0] < character_pos[0]+2:
								if position[1] > character_pos[1]-2 and position[1] < character_pos[1]+2:
									enemies[enemy_locations.index(position)].damage(1)
									print('Attack successful')
									on_move_events()
				if event.type == pygame.KEYDOWN:
					if not jumped_this_turn:
						if event.key == pygame.K_w or event.key == pygame.K_UP:
							if map_list[character_pos[1]-move_speed][character_pos[0]].type != 2 and map_list[character_pos[1]-1][character_pos[0]].type != 2:
								if not [character_pos[0],character_pos[1]-move_speed] in enemy_locations:
									character_pos[1] -= move_speed
									print('Moved')
									if move_speed == 2:
										jumped_this_turn = True
										print('You jumped')
									on_move_events()
					if not jumped_this_turn:
						if event.key == pygame.K_s or event.key == pygame.K_DOWN:
							if map_list[character_pos[1]+move_speed][character_pos[0]].type != 2 and map_list[character_pos[1]+1][character_pos[0]].type != 2:
								if not [character_pos[0],character_pos[1]+move_speed] in enemy_locations:
									character_pos[1] += move_speed
									print('Moved')
									if move_speed == 2:
										jumped_this_turn = True
										print('You jumped')
									on_move_events()									
					if not jumped_this_turn:
						if event.key == pygame.K_a or event.key == pygame.K_LEFT:
							if map_list[character_pos[1]][character_pos[0]-move_speed].type != 2 and map_list[character_pos[1]][character_pos[0]-1].type != 2:
								if not [character_pos[0]-move_speed,character_pos[1]] in enemy_locations:
									character_pos[0] -= move_speed
									print('Moved')
									if move_speed == 2:
										jumped_this_turn = True
										print('You jumped')
									on_move_events()									
					if not jumped_this_turn:			
						if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
							if map_list[character_pos[1]][character_pos[0]+move_speed].type != 2 and map_list[character_pos[1]][character_pos[0]+1].type != 2:
								if not [character_pos[0]+move_speed,character_pos[1]] in enemy_locations:
									character_pos[0] += move_speed
									print('Moved')
									if move_speed == 2:
										jumped_this_turn = True
										print('You jumped')
									on_move_events()									
					if event.key == pygame.K_SPACE:
						return
			if not jumped_this_turn:
				if key[pygame.K_w] or key[pygame.K_UP]:
					if not w_time:
						w_time = pygame.time.get_ticks()
					w_time_val = (pygame.time.get_ticks()-w_time)*w_accel*move_speed
					while w_time_val >= 200:
						w_time = False
						w_time_val -= 200
						if map_list[character_pos[1]-1][character_pos[0]].type != 2:
							if not [character_pos[0],character_pos[1]-1] in enemy_locations:
								w_accel = 10
								character_pos[1] -= 1
								print('Moved')
								on_move_events()
				else:
					w_accel = 1
					w_time = False
			if not jumped_this_turn:
				if key[pygame.K_s] or key[pygame.K_DOWN]:
					if not s_time:
						s_time = pygame.time.get_ticks()
					s_time_val = (pygame.time.get_ticks()-s_time)*s_accel*move_speed
					while s_time_val >= 200:
						s_time = False
						s_time_val -= 200
						if map_list[character_pos[1]+1][character_pos[0]].type != 2:
							if not [character_pos[0],character_pos[1]+1] in enemy_locations:
								s_accel = 10
								character_pos[1] += 1
								print('Moved')
								on_move_events()
				else:
					s_accel = 1
					s_time = False
			if not jumped_this_turn:
				if key[pygame.K_a] or key[pygame.K_LEFT]:
					if not a_time:
						a_time = pygame.time.get_ticks()
					a_time_val = (pygame.time.get_ticks()-a_time)*a_accel*move_speed
					while a_time_val >= 200:
						a_time = False
						a_time_val -= 200
						if map_list[character_pos[1]][character_pos[0]-1].type != 2:
							if not [character_pos[0]-1,character_pos[1]] in enemy_locations:
								a_accel = 10
								character_pos[0] -= 1
								print('Moved')
								on_move_events()
				else:
					a_accel = 1
					a_time = False
			if not jumped_this_turn:
				if key[pygame.K_d] or key[pygame.K_RIGHT]:
					if not d_time:
						d_time = pygame.time.get_ticks()
					d_time_val = (pygame.time.get_ticks()-d_time)*d_accel*move_speed
					while d_time_val >= 200:
						d_time = False
						d_time_val -= 200
						if map_list[character_pos[1]][character_pos[0]+1].type != 2:
							if not [character_pos[0]+1,character_pos[1]] in enemy_locations:
								d_accel = 10
								character_pos[0] += 1
								print('Moved')
								on_move_events()
				else:
					d_accel = 1
					d_time = False
		return

	def on_move_events():
		print('on_move_events called')
		global regen_counter
		global regen_rate
		global character_health
		global max_character_health
		global map_list
		for y in map_list:
			for x in y:
				x.set_visible(False)
		for room in rooms:
			if room.in_this_room(character_pos[0], character_pos[1]):
				if not room.discovered:
					room.discover()
					for room_y in range(room.height+3):
						for room_x in range(room.width+3):
							for y in range(11):
								for x in range(11):
									light_pos = [room_x-5+x+room.wall_left, room_y-5+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1:
										map_list[light_pos[1]][light_pos[0]].set_light(15)
							for y in range(9):
								for x in range(9):
									light_pos = [room_x-4+x+room.wall_left, room_y-4+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1: 
										map_list[light_pos[1]][light_pos[0]].set_light(31)
							for y in range(tile_size):
								for x in range(tile_size):
									light_pos = [room_x-3+x+room.wall_left, room_y-3+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1: 
										map_list[light_pos[1]][light_pos[0]].set_light(63)
							for y in range(5):
								for x in range(5):
									light_pos = [room_x-2+x+room.wall_left, room_y-2+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1: 
										map_list[light_pos[1]][light_pos[0]].set_light(127)
							for y in range(3):
								for x in range(3):
									light_pos = [room_x-1+x+room.wall_left, room_y-1+y+room.wall_top]
									if light_pos[0] < 128 and light_pos[1] < 128 and light_pos[0] > -1  and light_pos[1] > -1: 
										map_list[light_pos[1]][light_pos[0]].set_light(255)						
							map_list[room_y+room.wall_top][room_x+room.wall_left].set_light(255)
		for y in range(13):
			for x in range(13):
				light_pos = [character_pos[0]-tile_size+x, character_pos[1]-tile_size+y]
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
		for y in range(tile_size):
			for x in range(tile_size):
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
		print('Moved this turn')
		regen_counter += 1
		if regen_counter >= regen_rate:
			if character_health >= max_character_health:
				regen_counter = int(regen_rate/2.0)
			else: 
				character_health += int(regen_counter/regen_rate)
				print(character_health)
				regen_counter = 0			
		for enemy in enemy_locations:
			if enemies[enemy_locations.index(enemy)].alive:
				if enemy[0] > character_pos[0]-2 and enemy[0] < character_pos[0]+2 and enemy[1] > character_pos[1]-2 and enemy[1] < character_pos[1]+2:
					print('Imma attack you!')
					character_health -= 1
					print(character_health)
				elif random.randrange(1,8) != 0:
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
								pass
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
								pass
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
					pass
					print("Hurr durr, I'm just gonna sit here")
		if character_health <= 0:
			print('You Lose')
			pygame.event.post(LOSE)
		if character_pos == destination:
			print('You Win!')
			pygame.event.post(WIN)
		for enemy in enemies:
			if not enemy.alive:
				dead_enemies.append(enemy)
				dead_enemy_locations.append(enemy_locations[enemies.index(enemy)])
				del enemy_locations[enemies.index(enemy)]
				del enemies[enemies.index(enemy)]
		print('END TURN\n\n\n\n')

	def place_enemy():
		enemy_room = random.choice(self.dungeon.rooms)
		enemy_pos = [enemy_room.x1 + random.randrange(0, enemy_room.width), enemy_room.y1 + random.randrange(0, enemy_room.height)]
		if enemy_pos != character.position:
			if not enemy_pos in self.enemy_locations:
				return [enemy_pos,Enemy('monster', 5)]
		return self.place_enemy()

	def create_enemies():
		for enemy in range(random.randrange(2,len(self.dungeon.rooms))):
			enemy_info = self.place_enemy()
			self.enemy_locations.append(enemy_info[0])
			self.enemies.append(enemy_info[1])

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

	def import_files(self):
		geo_file = open(r'data\dungeon\geographical_features.txt')
		dungeon_attr_file = open(r'data\dungeon\dungeon_attributes.txt')
		dungeon_adj_file = open(r'data\dungeon\dungeon_adjectives.txt')
		dungeon_word_file = open(r'data\dungeon\dungeon_words.txt')
		self.geo_list = geo_file.read().splitlines()
		self.dungeon_attr_list = dungeon_attr_file.read().splitlines()
		self.dungeon_adj_list = dungeon_adj_file.read().splitlines()
		self.dungeon_word_list = dungeon_word_file.read().splitlines()

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
		fill(fill_start.x1, fill_start.y1)
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
		fill(fill_start.x1, fill_start.y1)
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
			return random_room(self.rooms)
		for x in self.rooms:
			if room.intercepts(x):
				print('Room conflicted with existing room, regenerating')
				return random_room(self.rooms)
		else:
			print('Made room dimensions')
			return room

	def carve_map(self, x, y):
		for row in range(y-1, y+2):
			for column in range(x-1, x+2):
				if self.maplist[row][column].type == 0:
					self.maplist[row][column] = Tile(2, False)
		else:
			self.maplist[y][x] = Tile(3, False)

	def make_rooms(self):
		self.rooms = []
		for x in range(random.randrange(4, 15)):
			room = random_room(self.rooms)
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
	def __init__(self, monster_type, hp):
		self.type = monster_type
		self.hp = hp
		self.alive = True
		self.turns_dead = 0
	def damage(self, value):
		self.hp -= value
		if self.hp <= 0:
			self.alive = False
