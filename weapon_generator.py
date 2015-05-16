import random 
from numpy.random import choice
from decimal import *
import os

getcontext().prec = 64



def rationalize(weight_list):
	weight_sum = 0
	weight_ratio_list = []
	for x in weight_list:
		weight_sum += Decimal(x)
	for x in weight_list:
		x = Decimal(x)
		weight_ratio_list.append(Decimal(Decimal(x)/weight_sum))
	return weight_ratio_list

def random_material(material_type):
	material_rarity = []
	for x in range(34):
		material_rarity.append(Decimal(34**(1/1.5)) - Decimal(x**(1/1.5)))
	material_rarity = rationalize(material_rarity)
	material_dict = materials['dict']
	possible_material_dict = material_dict[material_type]
	possible_material_list = materials[material_type]
	material = choice(possible_material_list, p=material_rarity)	
	material_stat = possible_material_dict[material]
	material_attributes = [material, material_stat]
	return material_attributes

def weapon_class_chooser():
	weapon_class = random.choice(classes)
	return weapon_class

def setup():
	data_dict = {}
	for s in classes:
		weapon_dict = {}
		weapons_file = open(r'items\weapons\%(weapon)s.txt' % {'weapon' : s.replace(' ','_')})
		weapons_data_list = weapons_file.read().splitlines()
		weapons_split = []
		weapon_list = []
		for x in weapons_data_list:
			x = x.split('/')
			weapon_data = x
			for x in weapon_data:
				weapons_split.append(x)
		material = []
		rarity_linear = []
		weapons_descript = []
		for x in weapons_split:
			if (weapons_split.index(x) + 1) % 4 == 1:
				material.append(x)
			elif (weapons_split.index(x) + 1) % 4 == 2:
				rarity_linear.append(int(x))
			elif (weapons_split.index(x) + 1) % 4 == 3:
				weapon_list.append(x)
			else:
				weapons_descript.append(x)
		weapons = {}
		rarity = []
		for x in rarity_linear:
			x = int(x)
			rarity.append(Decimal(x**(1/1.5)))
		rarity = rationalize(rarity)
		for weapon in range(len(weapon_list)):
			if material[weapon] == 's':
				weapon_level = round((10-int(rarity_linear[weapon]))**2.09590327429)
				weapon_type = 'special' + ' ' + s
			else:
				weapon_level = round((int((10-rarity_linear[weapon]/2))))
				weapon_type = s
			weapons[weapon_list[weapon]] = Weapon(material_type=material[weapon], rarity_linear=rarity_linear[weapon], rarity=rarity[weapon], name=weapon_list[weapon], weapon_class=s, level=weapon_level, descript=weapons_descript[weapon], weapon_type = weapon_type)
		# weapon_dict['material'] = material
		# weapon_dict['rarity_linear'] = rarity_linear
		weapon_dict['rarity'] = rarity
		weapon_dict['weapons'] = weapons
		# weapon_dict['weapons_info'] = weapons_info
		data_dict[s] = weapon_dict
	return data_dict

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
		self.level = round((self.level*material_stat)**(0.562151993))
		self.material_stat = material_stat
		self.material = material
		self.descript = self.descript.replace('%m', material)
	def set_info(self, info):
		self.info = info

def random_weapon(weapon_type='rand', maxlevel=100):

	def weapon_chooser(weapon_class):
		class_dict = data_dict[weapon_class]
		rarity = class_dict['rarity']
		weapon_list = list(class_dict['weapons'].keys())
		random_weapon = choice(weapon_list, p=rarity)
		weapon_attributes = {}
		weapons = class_dict['weapons']
		weapon = class_dict['weapons'][random_weapon]
		weapon_material = weapon.material_type
		if weapon_material == 's':
			weapon.set_material(material='special', material_stat=1)
			# weapon_attributes['type'] = 'special ' + weapon_class 
			# weapon_attributes['material'] = 'special'
			# weapon_attributes['material_stat'] = 1	
		if weapon_material == 'm':
			material_pick = random_material('metal')
			weapon.set_material(material=material_pick[0], material_stat=material_pick[1])
			# weapon_attributes['material'] = material_pick[0]
			# weapon_attributes['material_stat'] = material_pick[1]
			# weapon_attributes['type'] = weapon_class
		if weapon_material == 'w':
			material_pick = random_material('wood')
			weapon.set_material(material=material_pick[0], material_stat=material_pick[1])
			# weapon_attributes['material'] = material_pick[0]
			# weapon_attributes['material_stat'] = material_pick[1]
			# weapon_attributes['type'] = weapon_class
		# weapon_attributes['weapon'] = random_weapon
		# weapon_attributes['class'] = weapon_class
		# weapon_attributes['skill'] = weapon_class
		# weapon_attributes['info'] = weapon.info.replace('%m', weapon_attributes['material'])
		# weapon_rarity = int(rarity_linear[weapon_index])
		# if weapon_material == 's':
		# 	weapon_level = round((10-int(weapon_rarity))**2.09590327429)
		# if not weapon_material == 's':
		# 	weapon.level = round((weapon.level*weapon_attributes['material_stat'])**(0.562151993))	
		if weapon.level > maxlevel:
			return weapon_chooser(weapon_class)
		material = weapon.material
		material = ' '.join(word[0].upper() + word[1:] for word in material.split())
		weapon_name = weapon.name
		weapon_name = ' '.join(word[0].upper() + word[1:] for word in weapon_name.split())
		weapon_type = weapon.weapon_type
		weapon_type = ' '.join(word[0].upper() + word[1:] for word in weapon_type.split())
		weapon_skill = weapon.weapon_class
		weapon_skill = ' '.join(word[0].upper() + word[1:] for word in weapon_skill.split())
		if weapon_material == 's':
			weapon_info = (weapon_name + ' (' + weapon_type + ' - No Material Bonus' + ' - Requires Level ' + str(weapon.level) + ' ' + weapon_skill + ' Skill' + ')')
		else:
			weapon_info = (material + ' ' + weapon_name + ' (' + weapon_type + ' - Material Bonus x' + str(weapon.material_stat) + ' - Requires Level ' + str(weapon.level) + ' ' + weapon_skill + ' Skill' + ')')
		weapon.set_info(weapon_info)
		return weapon

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
		weapon = random_weapon('rand')
		weapon_list.append(weapon.info + ' Description: ' + weapon.descript)
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
			
def material_lister():
	metallic_material_file = open(r'items\weapons\metallic_materials.txt')
	metallic_materials = metallic_material_file.read().splitlines()
	metallic_material_stats = {}
	wooden_material_file = open(r'items\weapons\wooden_materials.txt')
	wooden_materials = wooden_material_file.read().splitlines()
	wooden_material_stats = {}
	for x in range(len(metallic_materials)):
		metallic_material_stats[metallic_materials[x]] = round((x+1)**1.6)
	for x in range(len(wooden_materials)):
		wooden_material_stats[wooden_materials[x]] = round((x+1)**1.6)
	material_dict = {'metal' : metallic_material_stats, 'wood' : wooden_material_stats}
	dict_list = {'metal' : metallic_materials, 'wood' : wooden_materials, 'dict' : material_dict}
	return dict_list	

materials = material_lister()
classes = ['ranged','long bladed','shield','magic', 'blunt', 'concealed', 'gadget', 'book']
data_dict = setup()
print(user_process(input('How many weapons to generate? (Type "end" to close program.) '))
)
