import pygame
import sys
from settings import *
from level import Level

pygame.init()
screen = pygame.display.set_mode((screen_weight, screen_height))
clock = pygame.time.Clock()
level = Level(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    level.run()

    pygame.display.update()
    clock.tick(60)
