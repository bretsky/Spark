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
		weapons = []
		for x in weapons_data_list:
			x = x.split('/')
			weapon_data = x
			for x in weapon_data:
				weapons_split.append(x)
		material = []
		rarity_linear = []
		weapons_info = []
		for x in weapons_split:
			if (weapons_split.index(x) + 1) % 4 == 1:
				material.append(x)
			elif (weapons_split.index(x) + 1) % 4 == 2:
				rarity_linear.append(x)
			elif (weapons_split.index(x) + 1) % 4 == 3:
				weapons.append(x)
			else:
				weapons_info.append(x)
		rarity = []
		for x in rarity_linear:
			x = int(x)
			rarity.append(Decimal(x**(1/1.5)))
		rarity = rationalize(rarity)
		weapon_dict['material'] = material
		weapon_dict['rarity_linear'] = rarity_linear
		weapon_dict['rarity'] = rarity
		weapon_dict['weapons'] = weapons
		weapon_dict['weapons_info'] = weapons_info
		data_dict[s] = weapon_dict
	return data_dict

def isnumeric(n):
        try:
                i = float(n)
        except (ValueError, TypeError):
            return False
        return True

def random_weapon(weapon_type='rand', maxlevel=100):

	def weapon_chooser(weapon_class):
		class_dict = data_dict[weapon_class]
		weapons = class_dict['weapons']
		rarity = class_dict['rarity']
		rarity_linear = class_dict['rarity_linear']
		weapons_info = class_dict['weapons_info']
		random_weapon = choice(weapons, p=rarity)
		weapon_attributes = {}
		weapon_index = int(weapons.index(random_weapon))
		weapon_material = class_dict['material'][weapon_index]
		if weapon_material == 's':
			weapon_attributes['type'] = 'special ' + weapon_class 
			weapon_attributes['material'] = 'special'
			weapon_attributes['material_stat'] = 1	
		if weapon_material == 'm':
			material_pick = random_material('metal')
			weapon_attributes['material'] = material_pick[0]
			weapon_attributes['material_stat'] = material_pick[1]
			weapon_attributes['type'] = weapon_class
		if weapon_material == 'w':
			material_pick = random_material('wood')
			weapon_attributes['material'] = material_pick[0]
			weapon_attributes['material_stat'] = material_pick[1]
			weapon_attributes['type'] = weapon_class
		weapon_attributes['weapon'] = random_weapon
		weapon_attributes['class'] = weapon_class
		weapon_attributes['skill'] = weapon_class
		weapon_attributes['info'] = weapons_info[weapon_index].replace('%m', weapon_attributes['material'])
		weapon_rarity = int(rarity_linear[weapon_index])
		if weapon_material == 's':
			weapon_level = round((10-int(weapon_rarity))**2.09590327429)
		else:
			weapon_level = round((int((10-weapon_rarity/2)*weapon_attributes['material_stat']))**(0.562151993))			
		if weapon_level > maxlevel:
			return weapon_chooser(weapon_class)
		weapon_attributes['level'] = weapon_level
		material = weapon_attributes['material']
		material = ' '.join(word[0].upper() + word[1:] for word in material.split())
		weapon = weapon_attributes['weapon']
		weapon = ' '.join(word[0].upper() + word[1:] for word in weapon.split())
		weapon_type = weapon_attributes['type']
		weapon_type = ' '.join(word[0].upper() + word[1:] for word in weapon_type.split())
		weapon_skill = weapon_attributes['skill']
		weapon_skill = ' '.join(word[0].upper() + word[1:] for word in weapon_skill.split())
		if weapon_material == 's':
			weapon_name = (weapon + ' (' + weapon_type + ' - No Material Bonus' + ' - Requires Level ' + str(weapon_level) + ' ' + weapon_skill + ' Skill' + ')' + ' Info: ' + weapon_attributes['info'])
		else:
			weapon_name = (material + ' ' + weapon + ' (' + weapon_type + ' - Material Bonus x' + str(weapon_attributes['material_stat']) + ' - Requires Level ' + str(weapon_level) + ' ' + weapon_skill + ' Skill' + ')' + ' Info: ' + weapon_attributes['info'])
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
		random_weapon_attributes = random_weapon('rand')
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
