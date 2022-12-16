import sys
import pygame
import random
from pygame.math import Vector2

class FRUIT:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)  # 创造向量

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.ellipse(screen, (126, 166, 114), fruit_rect)


pygame.init()
cell_size = 40
cell_number = 20
bg_size = (cell_size * cell_number, cell_size * cell_number)
screen = pygame.display.set_mode(bg_size)
clock = pygame.time.Clock()

fruit = FRUIT()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(pygame.Color(175, 215, 75))
    fruit.draw_fruit()
    pygame.display.update()
    clock.tick(60)
