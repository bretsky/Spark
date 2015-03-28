import random 
from numpy.random import choice
from decimal import *

getcontext().prec = 64

def isnumeric(n):
        try:
                i = float(n)
        except (ValueError, TypeError):
            return False
        return True

def random_legendary_weapon(weapon_type='rand'):

	def weapon_chooser(weapon_class):		
		if weapon_class == 'ranged':
			ranged_weapons_file = open('legendary_ranged.txt')
			ranged_weapons = ranged_weapons_file.read().splitlines()			
			random_weapon = random.choice(ranged_weapons)
			weapon_attributes = {}
			weapon_attributes['weapon'] = random_weapon
			weapon_attributes['type'] = 'legendary ranged' 
			weapon_attributes['material'] = 'special'
			weapon_attributes['material_stat'] = 1
			weapon_attributes['class'] = 'ranged'
			weapon_attributes['skill'] = 'ranged weapon'
			weapon_attributes['level'] = 120
			weapon = weapon_attributes['weapon']
			weapon = ' '.join(word[0].upper() + word[1:] for word in weapon.split())
			weapon_type = weapon_attributes['type']
			weapon_type = ' '.join(word[0].upper() + word[1:] for word in weapon_type.split())
			weapon_skill = weapon_attributes['skill']
			weapon_skill = ' '.join(word[0].upper() + word[1:] for word in weapon_skill.split())
			weapon_name = (weapon + ' (' + weapon_type + ' - No Material Bonus' + ' - Requires Level ' + str(weapon_attributes['level']) + ' ' + weapon_skill + ' Skill' + ')')
			weapon_attributes['name'] = weapon_name
			return weapon_attributes
		if weapon_class == 'long bladed':
			long_bladed_weapons_file = open('legendary_long_bladed.txt')
			long_bladed_weapons = long_bladed_weapons_file.read().splitlines()			
			random_weapon = random.choice(long_bladed_weapons)
			weapon_attributes = {}
			weapon_attributes['weapon'] = random_weapon
			weapon_attributes['type'] = 'legendary long bladed' 
			weapon_attributes['material'] = 'special'
			weapon_attributes['material_stat'] = 1
			weapon_attributes['class'] = 'long bladed'
			weapon_attributes['skill'] = 'long bladed weapon'
			weapon_attributes['level'] = 120
			weapon = weapon_attributes['weapon']
			weapon = ' '.join(word[0].upper() + word[1:] for word in weapon.split())
			weapon_type = weapon_attributes['type']
			weapon_type = ' '.join(word[0].upper() + word[1:] for word in weapon_type.split())
			weapon_skill = weapon_attributes['skill']
			weapon_skill = ' '.join(word[0].upper() + word[1:] for word in weapon_skill.split())
			weapon_name = (weapon + ' (' + weapon_type + ' - No Material Bonus' + ' - Requires Level ' + str(weapon_attributes['level']) + ' ' + weapon_skill + ' Skill' + ')')
			weapon_attributes['name'] = weapon_name
			return weapon_attributes
		if weapon_class == 'shield':
			shield_weapons_file = open('legendary_shields.txt')
			shield_weapons = shield_weapons_file.read().splitlines()			
			random_weapon = random.choice(shield_weapons)
			weapon_attributes = {}
			weapon_attributes['weapon'] = random_weapon
			weapon_attributes['type'] = 'legendary shield' 
			weapon_attributes['material'] = 'special'
			weapon_attributes['material_stat'] = 1
			weapon_attributes['class'] = 'shield'
			weapon_attributes['skill'] = 'shield'
			weapon_attributes['level'] = 120
			weapon = weapon_attributes['weapon']
			weapon = ' '.join(word[0].upper() + word[1:] for word in weapon.split())
			weapon_type = weapon_attributes['type']
			weapon_type = ' '.join(word[0].upper() + word[1:] for word in weapon_type.split())
			weapon_skill = weapon_attributes['skill']
			weapon_skill = ' '.join(word[0].upper() + word[1:] for word in weapon_skill.split())
			weapon_name = (weapon + ' (' + weapon_type + ' - No Material Bonus' + ' - Requires Level ' + str(weapon_attributes['level']) + ' ' + weapon_skill + ' Skill' + ')')
			weapon_attributes['name'] = weapon_name
			return weapon_attributes
		if weapon_class == 'magic':
			magic_weapons_file = open('legendary_magic.txt')
			magic_weapons = magic_weapons_file.read().splitlines()			
			random_weapon = random.choice(magic_weapons)
			weapon_attributes = {}
			weapon_attributes['weapon'] = random_weapon
			weapon_attributes['type'] = 'legendary magic' 
			weapon_attributes['material'] = 'special'
			weapon_attributes['material_stat'] = 1
			weapon_attributes['class'] = 'magic'
			weapon_attributes['skill'] = 'magic weapon'
			weapon_attributes['level'] = 120
			weapon = weapon_attributes['weapon']
			weapon = ' '.join(word[0].upper() + word[1:] for word in weapon.split())
			weapon_type = weapon_attributes['type']
			weapon_type = ' '.join(word[0].upper() + word[1:] for word in weapon_type.split())
			weapon_skill = weapon_attributes['skill']
			weapon_skill = ' '.join(word[0].upper() + word[1:] for word in weapon_skill.split())
			weapon_name = (weapon + ' (' + weapon_type + ' - No Material Bonus' + ' - Requires Level ' + str(weapon_attributes['level']) + ' ' + weapon_skill + ' Skill' + ')')
			weapon_attributes['name'] = weapon_name
			return weapon_attributes
		if weapon_class == 'blunt':
			blunt_weapons_file = open('legendary_blunts.txt')
			blunt_weapons = blunt_weapons_file.read().splitlines()			
			random_weapon = random.choice(blunt_weapons)
			weapon_attributes = {}
			weapon_attributes['weapon'] = random_weapon
			weapon_attributes['type'] = 'legendary blunt' 
			weapon_attributes['material'] = 'special'
			weapon_attributes['material_stat'] = 1
			weapon_attributes['class'] = 'blunt'
			weapon_attributes['skill'] = 'blunt weapon'
			weapon_attributes['level'] = 120
			weapon = weapon_attributes['weapon']
			weapon = ' '.join(word[0].upper() + word[1:] for word in weapon.split())
			weapon_type = weapon_attributes['type']
			weapon_type = ' '.join(word[0].upper() + word[1:] for word in weapon_type.split())
			weapon_skill = weapon_attributes['skill']
			weapon_skill = ' '.join(word[0].upper() + word[1:] for word in weapon_skill.split())
			weapon_name = (weapon + ' (' + weapon_type + ' - No Material Bonus' + ' - Requires Level ' + str(weapon_attributes['level']) + ' ' + weapon_skill + ' Skill' + ')')
			weapon_attributes['name'] = weapon_name
			return weapon_attributes
		if weapon_class == 'concealed':
			concealed_weapons_file = open('legendary_concealed.txt')
			concealed_weapons = concealed_weapons_file.read().splitlines()			
			random_weapon = random.choice(concealed_weapons)
			weapon_attributes = {}
			weapon_attributes['weapon'] = random_weapon
			weapon_attributes['type'] = 'legendary concealed' 
			weapon_attributes['material'] = 'special'
			weapon_attributes['material_stat'] = 1
			weapon_attributes['class'] = 'concealed'
			weapon_attributes['skill'] = 'concealed weapon'
			weapon_attributes['level'] = 120
			weapon = weapon_attributes['weapon']
			weapon = ' '.join(word[0].upper() + word[1:] for word in weapon.split())
			weapon_type = weapon_attributes['type']
			weapon_type = ' '.join(word[0].upper() + word[1:] for word in weapon_type.split())
			weapon_skill = weapon_attributes['skill']
			weapon_skill = ' '.join(word[0].upper() + word[1:] for word in weapon_skill.split())
			weapon_name = (weapon + ' (' + weapon_type + ' - No Material Bonus' + ' - Requires Level ' + str(weapon_attributes['level']) + ' ' + weapon_skill + ' Skill' + ')')
			weapon_attributes['name'] = weapon_name
			return weapon_attributes
		if weapon_class == 'gadget':
			gadget_weapons_file = open('legendary_gadgets.txt')
			gadget_weapons = gadget_weapons_file.read().splitlines()			
			random_weapon = random.choice(gadget_weapons)
			weapon_attributes = {}
			weapon_attributes['weapon'] = random_weapon
			weapon_attributes['type'] = 'legendary gadget' 
			weapon_attributes['material'] = 'special'
			weapon_attributes['material_stat'] = 1
			weapon_attributes['class'] = 'gadget'
			weapon_attributes['skill'] = 'gadget'
			weapon_attributes['level'] = 120
			weapon = weapon_attributes['weapon']
			weapon = ' '.join(word[0].upper() + word[1:] for word in weapon.split())
			weapon_type = weapon_attributes['type']
			weapon_type = ' '.join(word[0].upper() + word[1:] for word in weapon_type.split())
			weapon_skill = weapon_attributes['skill']
			weapon_skill = ' '.join(word[0].upper() + word[1:] for word in weapon_skill.split())
			weapon_name = (weapon + ' (' + weapon_type + ' - No Material Bonus' + ' - Requires Level ' + str(weapon_attributes['level']) + ' ' + weapon_skill + ' Skill' + ')')
			weapon_attributes['name'] = weapon_name
			return weapon_attributes
		if weapon_class == 'book':
			book_weapons_file = open('legendary_books.txt')
			book_weapons = book_weapons_file.read().splitlines()			
			random_weapon = random.choice(book_weapons)
			weapon_attributes = {}
			weapon_attributes['weapon'] = random_weapon
			weapon_attributes['type'] = 'legendary book' 
			weapon_attributes['material'] = 'special'
			weapon_attributes['material_stat'] = 1
			weapon_attributes['class'] = 'book'
			weapon_attributes['skill'] = 'book'
			weapon_attributes['level'] = 120
			weapon = weapon_attributes['weapon']
			weapon = ' '.join(word[0].upper() + word[1:] for word in weapon.split())
			weapon_type = weapon_attributes['type']
			weapon_type = ' '.join(word[0].upper() + word[1:] for word in weapon_type.split())
			weapon_skill = weapon_attributes['skill']
			weapon_skill = ' '.join(word[0].upper() + word[1:] for word in weapon_skill.split())
			weapon_name = (weapon + ' (' + weapon_type + ' - No Material Bonus' + ' - Requires Level ' + str(weapon_attributes['level']) + ' ' + weapon_skill + ' Skill' + ')')
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

print(user_process(input('How many weapons to generate? (Type "end" to close program.) '))
)