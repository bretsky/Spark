import random 
from numpy.random import choice
from decimal import *

getcontext().prec = 64

def legendary_setup():
	legendary_data_dict = {}
	for s in classes:
		weapon_dict = {}
		weapons_file = open(r'items\legendary_weapons\legendary_%(weapon)s.txt' % {'weapon' : s.replace(' ','_')})
		weapons_data_list = weapons_file.read().splitlines()
		weapons_split = []
		weapons = []
		for x in weapons_data_list:
			x = x.split('/')
			weapon_data = x
			for x in weapon_data:
				weapons_split.append(x)
		weapons_info = []
		for x in weapons_split:
			if (weapons_split.index(x) + 1) % 2 == 1:
				weapons.append(x)
			else:
				weapons_info.append(x)
		weapon_dict['weapons'] = weapons
		weapon_dict['weapons_info'] = weapons_info
		legendary_data_dict[s] = weapon_dict
	title_file = open(r'items\legendary_weapons\newspaper_titles.txt')
	title_list = title_file.read().splitlines()
	legendary_data_dict['titles'] = title_list
	return legendary_data_dict

def isnumeric(n):
		try:
				i = float(n)
		except (ValueError, TypeError):
			return False
		return True

class Weapon():
	def __init__(self, material_type, rarity, rarity_linear, name, descript, level, weapon_class, weapon_type):
		self.material_type = material_type
		self.rarity = rarity
		self.rarity_linear = rarity_linear
		self.name = name
		self.descript = descript
		self.level = level
		self.weapon_class = weapon_class
		self.weapon_type = weapon_type
	def set_material(self, material, material_stat):
		if self.material_type != 's':
			self.level = round((self.level*material_stat**1.5)**(0.562151993))
		self.material_stat = material_stat
		self.material = material
		self.descript = self.descript.replace('%m', material)
	def set_info(self, info):
		self.info = info

def random_legendary_weapon(weapon_type='rand'):

	def weapon_chooser(weapon_class):		
		class_dict = legendary_data_dict[weapon_class]
		weapons = class_dict['weapons']
		random_weapon = random.choice(weapons)
		weapon_index = weapons.index(random_weapon)  
		weapon_attributes = {}
		random_weapon_info = class_dict['weapons_info'][weapon_index]
		weapon_attributes['info'] = random_weapon_info.replace('%t', random.choice(legendary_data_dict['titles']))
		weapon_attributes['weapon'] = random_weapon
		weapon_attributes['type'] = 'legendary ' + weapon_class 
		weapon_attributes['material'] = 'legendary'
		weapon_attributes['material_stat'] = 64
		weapon_attributes['class'] = weapon_class
		weapon_attributes['skill'] = weapon_class
		weapon_attributes['level'] = 120
		weapon = weapon_attributes['weapon']
		weapon = ' '.join(word[0].upper() + word[1:] for word in weapon.split())
		weapon_type = weapon_attributes['type']
		weapon_type = ' '.join(word[0].upper() + word[1:] for word in weapon_type.split())
		weapon_skill = weapon_attributes['skill']
		weapon_skill = ' '.join(word[0].upper() + word[1:] for word in weapon_skill.split())
		weapon_name = (weapon + ' (' + weapon_type + ' - No Material Bonus' + ' - Requires Level ' + str(weapon_attributes['level']) + ' ' + weapon_skill + ' Skill' + ')'+ ' Info: ' + weapon_attributes['info'])
		weapon_attributes['name'] = weapon_name
		return weapon_attributes

	def weapon_class_chooser():
		classes = ['ranged','long bladed','shield','magic', 'blunt', 'concealed', 'gadget', 'book']
		weapon_class = random.choice(classes)
		return weapon_class

	if weapon_type == 'rand':
		return weapon_chooser(weapon_class_chooser())
	else:	
		return weapon_chooser(weapon_type)

def weapon_generator(weapons_limit):
	counter = 0
	weapon_list = []
	while counter <= weapons_limit - 1:
		random_weapon_attributes = random_legendary_weapon('rand')
		weapon_list.append(random_weapon_attributes['name'])
		counter += 1
	return weapon_list

def user_process(user_input):
	end_process = False
	while end_process != True:
		if user_input != 'end' and isnumeric(user_input) == True:
			weapon_generator_list = weapon_generator(int(user_input))
			print('')
			for x in range(len(weapon_generator_list)):
				print(weapon_generator_list[x] + '\n')
			return user_process(input('How many more weapons to generate? (Type "end" to close program.) '))
		elif user_input == 'end':
			return 'Closing...'
			sleep(100)
			break

		else:
			return user_process(input('How many more weapons to generate? (Must be a number.) '))
classes = ['ranged','long bladed','shield','magic', 'blunt', 'concealed', 'gadget', 'book']

legendary_data_dict = legendary_setup()
print(user_process(input('How many weapons to generate? (Type "end" to close program.) '))
)