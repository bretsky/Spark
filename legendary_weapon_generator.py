import random 
from numpy.random import choice
from decimal import *

getcontext().prec = 64

def random_weapon(weapon_type='rand', maxlevel=100):

	def weapon_chooser(weapon_class):		
		if weapon_class == 'ranged':
			ranged_weapons_file = open('ranged_weapons.txt')
			ranged_weapons_data = ranged_weapons_file.read().splitlines()
			ranged_weapons_split = []
			ranged_weapons = []
			for x in ranged_weapons_data:
				x = x.split('/')
				weapon_data = x
				for x in weapon_data:
					ranged_weapons_split.append(x)
			ranged_material = []
			ranged_rarity_linear = []
			for x in ranged_weapons_split:
				if (ranged_weapons_split.index(x) + 1) % 3 == 1:
					ranged_material.append(x)
				elif (ranged_weapons_split.index(x) + 1) % 3 == 2:
					ranged_rarity_linear.append(x)
				else:
					ranged_weapons.append(x)
			ranged_rarity = []
			for x in ranged_rarity_linear:
				x = int(x)
				ranged_rarity.append(Decimal(x**(1/1.5)))
			ranged_rarity = rationalize(ranged_rarity)
			random_weapon = choice(ranged_weapons, p=ranged_rarity)
			if ranged_material[ranged_weapons.index(random_weapon)] == 's':
				weapon_attributes = {}
				weapon_attributes['weapon'] = random_weapon
				weapon_attributes['type'] = 'special ranged' 
				weapon_attributes['material'] = 'special'
				weapon_attributes['material_stat'] = 1
				weapon_attributes['class'] = 'ranged'
				weapon_attributes['skill'] = 'ranged weapon'
				weapon_index = ranged_weapons.index(random_weapon)
				weapon_rarity = int(ranged_rarity_linear[weapon_index])
				weapon_level = round((10-int(ranged_rarity_linear[ranged_weapons.index(random_weapon)]))**2.09590327429)
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
				weapon_name = (weapon + ' (' + weapon_type + ' - No Material Bonus' + ' - Requires Level ' + str(weapon_level) + ' ' + weapon_skill + ' Skill' + ')')
				weapon_attributes['name'] = weapon_name
				return weapon_attributes
			else:
				if ranged_material[ranged_weapons.index(random_weapon)] == 'm':
					material = random_material('metal')
				else:
					material = random_material('wood')
				weapon_attributes = {}
				weapon_attributes['weapon'] = random_weapon
				weapon_attributes['type'] = 'ranged' 
				weapon_attributes['material'] = material[0]
				weapon_attributes['material_stat'] = material[1]
				weapon_attributes['class'] = 'ranged'
				weapon_attributes['skill'] = 'ranged weapon'
				weapon_index = ranged_weapons.index(random_weapon)
				weapon_rarity = int(ranged_rarity_linear[weapon_index])
				weapon_level = round((int((10-weapon_rarity)*material[1]))**(0.562151993))
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
				weapon_name = (material + ' ' + weapon + ' (' + weapon_type + ' - Material Bonus x' + str(weapon_attributes['material_stat']) + ' - Requires Level ' + str(weapon_level) + ' ' + weapon_skill + ' Skill' + ')')
				weapon_attributes['name'] = weapon_name
				return weapon_attributes
		

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
	metallic_material_file = open('metallic_materials.txt')
	metallic_materials = metallic_material_file.read().splitlines()
	metallic_material_stats = {}
	wooden_material_file = open('wooden_materials.txt')
	wooden_materials = wooden_material_file.read().splitlines()
	wooden_material_stats = {}
	for x in range(len(metallic_materials)):
		metallic_material_stats[metallic_materials[x]] = round((x+1)**1.7)
	for x in range(len(wooden_materials)):
		wooden_material_stats[wooden_materials[x]] = round((x+1)**1.7)
	material_dict = {'metal' : metallic_material_stats, 'wood' : wooden_material_stats}
	dict_list = {'metal' : metallic_materials, 'wood' : wooden_materials, 'dict' : material_dict}
	return dict_list	

materials = material_lister()

print(user_process(input('How many weapons to generate? (Type "end" to close program.) '))
)