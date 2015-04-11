import random
from numpy.random import choice
from decimal import *

getcontext().prec = 64

def legendary_setup():
	legendary_data_dict = {}
	for s in classes:
		weapon_dict = {}
		weapons_file = open(r'legendary_weapons\legendary_%(weapon)s.txt' % {'weapon' : s.replace(' ','_')})
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
	title_file = open('newspaper_titles.txt')
	title_list = title_file.read().splitlines()
	legendary_data_dict['titles'] = title_list
	return legendary_data_dict

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
	classes = ['ranged','long bladed','shield','magic', 'blunt', 'concealed', 'gadget', 'book']
	weapon_class = random.choice(classes)
	return weapon_class
	
def setup():
	data_dict = {}
	for s in classes:
		weapon_dict = {}
		weapons_file = open(r'weapons\%(weapon)s.txt' % {'weapon' : s.replace(' ','_')})
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

def get_name():
	playername = input("What's your name? ")
	return playername

def isnumeric(n):
        try:
                i = float(n)
        except (ValueError, TypeError):
            return False
        return True

def get_difficulty():
	difficulty = input("Difficulty?(Larger numbers are more difficult, 10 is a standard game) ")
	if not isnumeric(difficulty):
		print('Difficulty must be a number 0 or larger, please try again.')
		difficulty = get_difficulty()
	if float(difficulty) < 0 or difficulty == '' :
		print('Difficulty must be a number 0 or larger, please try again.')
		difficulty = get_difficulty()	
	difficulty = int(round(float(difficulty)+0.1))
	
	return difficulty
 
def intro():
	playername = get_name()
	difficulty = get_difficulty()
	print('Hello ' + playername + '.')
	print('You are playing on difficulty level %(difficulty)i.' % {'difficulty' : difficulty})
	if difficulty == 0:
		print('You are on invincible mode. Your attacks instantly kill, you can not take damage, and all of your stats are maxed.')
	else:
		multiplier = 1.0/(difficulty/10.0)
		enemyrate = difficulty/10.0
		score = enemyrate/multiplier
		print('On this difficulty level, your stats have a multiplier of %(multiplier)s, enemies generate at %(enemyrate)s times the normal rate and your final score will have a difficulty multiplier of %(score)s.' % {'multiplier' : str(round(multiplier,3)), 'enemyrate' : str(round(enemyrate, 3)), 'score' : str(round(score, 3))})
	return "Let's begin!"

def is_class(string):
	if string in ['mage', 'warrior', 'rogue', 'tank', 'engineer', 'ranger']:
		return True
	else:
		return False

def random_weapon(weapon_type='rand', maxlevel=100):

	def weapon_chooser(weapon_class):
		class_dict = data_dict[weapon_class]
		weapons = class_dict['weapons']
		material = class_dict['material']
		rarity = class_dict['rarity']
		rarity_linear = class_dict['rarity_linear']
		weapons_info = class_dict['weapons_info']
		random_weapon = choice(weapons, p=rarity)
		weapon_attributes = {}
		weapon_index = int(weapons.index(random_weapon))
		weapon_material = material[weapon_index]
		if weapon_material == 's':
			weapon_attributes['type'] = 'special ' + weapon_class 
			weapon_attributes['material'] = 'special'
			weapon_attributes['material_stat'] = 1	
		if weapon_material == 'm':
			material = random_material('metal')
			weapon_attributes['material'] = material[0]
			weapon_attributes['material_stat'] = material[1]
			weapon_attributes['type'] = weapon_class
		if weapon_material == 'w':
			material = random_material('wood')
			weapon_attributes['material'] = material[0]
			weapon_attributes['material_stat'] = material[1]
			weapon_attributes['type'] = weapon_class
		weapon_attributes['weapon'] = random_weapon
		weapon_attributes['class'] = weapon_class
		weapon_attributes['skill'] = weapon_class
		weapon_attributes['info'] = weapons_info[weapon_index].replace('%m', material[0])
		weapon_rarity = int(rarity_linear[weapon_index])
		if weapon_material == 's':
			weapon_level = round((10-int(weapon_rarity))**2.09590327429)
		else:
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

def get_first_weapon(player_class):
	beginning_weapons = []
	if player_class == 'mage':
		beginning_weapons.append(random_weapon('magic', 3))
		beginning_weapons.append(random_weapon('book', 3))
		return beginning_weapons[0]['name'] + '\n' + beginning_weapons[1]['name']
	if player_class == 'warrior':
		beginning_weapons.append(random_weapon('long bladed', 3))
		beginning_weapons.append(random_weapon('shield', 3))
		return beginning_weapons[0]['name'] + '\n' + beginning_weapons[1]['name']
	if player_class == 'rogue':
		beginning_weapons.append(random_weapon('concealed', 3))
		beginning_weapons.append(random_weapon('concealed', 3))
		return beginning_weapons[0]['name'] + '\n' + beginning_weapons[1]['name']
	if player_class == 'tank':
		beginning_weapons.append(random_weapon('blunt', 3))
		beginning_weapons.append(random_weapon('shield', 3))
		return beginning_weapons[0]['name'] + '\n' + beginning_weapons[1]['name']
	if player_class == 'engineer':
		beginning_weapons.append(random_weapon('gadget', 3))
		beginning_weapons.append(random_weapon('gadget', 3))
		return beginning_weapons[0]['name'] + '\n' + beginning_weapons[1]['name']
	if player_class == 'ranger':
		beginning_weapons.append(random_weapon('ranged', 3))
		beginning_weapons.append(random_weapon('concealed', 3))
		return beginning_weapons[0]['name'] + '\n' + beginning_weapons[1]['name']
	elif is_class(player_class) != True:
		return get_first_weapon(input('Please enter a valid class. Mage, Warrior, Rogue, Tank, Engineer or Ranger. ').lower())

def material_lister():
	metallic_material_file = open('metallic_materials.txt')
	metallic_materials = metallic_material_file.read().splitlines()
	metallic_material_stats = {}
	wooden_material_file = open('wooden_materials.txt')
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
legendary_data_dict = legendary_setup()
data_dict = setup()
print(intro())
x = 0
while x != 1:
	print(get_first_weapon(input('Please enter your class. Mage, Warrior, Rogue, Tank, Engineer or Ranger. ').lower()))


