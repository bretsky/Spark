import pygame
pygame.init()

GameGo = True
spark_animation = []
for i in range(96):
	spark = pygame.image.load('intro\spark (%(number)i).gif' % {'number' : i+1})
	spark_animation.append(spark)
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Spark")

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
framerate = pygame.time.Clock()

index = 0
while GameGo:
	framerate.tick(24)
	screen.blit(background, (0,0))
	screen.blit(spark_animation[index], (384, 312))
	index+= 1
	if index == 96:
		index = 0
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GameGo = False