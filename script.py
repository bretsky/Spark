import json

enemies = json.load(open('enemies.json', 'r'))

print(enemies)

for enemy in enemies:
	dna = {}
	attributes = {}
	for key in enemies[enemy]:
		if key == "attributes":
			attributes = enemies[enemy][key]
		else:
			dna[key] = enemies[enemy][key]
	enemies[enemy]["dna"] = dna
	for key in attributes:
		enemies[enemy][key] = attributes[key]
	del enemies[enemy]["attributes"]
	for key in dna:
		del enemies[enemy][key]

json.dump(enemies, open('enemies.json', 'w'))