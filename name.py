import random

MALE = 0
FEMALE = 1

files = (("names/male.txt", "names/male_dist.txt"), ("names/female.txt", "names/female_dist.txt"))

def p_choice(n, p, total):
	r = random.randrange(total)
	x = -1
	while x < r:
		i = random.randrange(0, len(n))
		x += float(p[i])
	return n[i]

def random_name():
	gender = random.choice((MALE, FEMALE))
	return p_choice(open(files[gender][0], "r").read().splitlines(), open(files[gender][1], "r").read().splitlines(), 1)
