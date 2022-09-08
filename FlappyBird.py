import pygame, sys, time
from pygame.locals import *

pygame.init()

#set up the window
SCREEN = pygame.display.set_mode((500, 750))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

#colors
BLACK = (0, 0, 0)

#images
BACKGROUND = pygame.image.load('flappy_bird_background.jpg')

#main loop
while True:
	SCREEN.blit(BACKGROUND, (0, 0))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	
	pygame.display.update()
	clock.tick(45)