import random
geo_file = open('geographical_features.txt')
dungeon_attr_file = open('dungeon_attributes.txt')
dungeon_adj_file = open('dungeon_adjectives.txt')
dungeon_word_file = open('dungeon_words.txt')
geo_list = geo_file.read().splitlines()
dungeon_attr_list = dungeon_attr_file.read().splitlines()
dungeon_adj_list = dungeon_adj_file.read().splitlines()
dungeon_word_list = dungeon_word_file.read().splitlines()

def random_dungeon_name():
	num = random.randrange(0,5)
	if num == 0:
		dungeon_name = ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_word_list).split()) + ' ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(geo_list).split())
	elif num == 1:
		dungeon_name = 'The ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_adj_list).split()) + ' ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(geo_list).split())
	elif num == 2:
		dungeon_name = 'The ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(geo_list).split()) + ' of ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_attr_list).split())
	elif num == 3:
		dungeon_name = 'The ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_adj_list).split()) + ' ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(geo_list).split()) + ' of ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_attr_list).split())
	elif num == 4:
		dungeon_name = 'The ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(geo_list).split()) + ' of ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_adj_list).split()) + ' ' + ' '.join(word[0].upper() + word[1:] for word in random.choice(dungeon_attr_list).split())
	return dungeon_name

# while True:
# 	for x in range(int(input('How many dungeons to generate?'))):
# 		print(random_dungeon_name())

