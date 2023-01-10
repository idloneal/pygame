import pygame.transform

from tiles import AnimationTile
import random


class Enemy(AnimationTile):
    def __init__(self, size, x, y):
        super(Enemy, self).__init__(size, x, y, '../graphics/enemy/run')
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))
        self.speed = float(random.choice(['-1', '-2']))

    def move(self):
        self.reverse_image()
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image

    def reverse(self):
        self.speed *= -1

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animation()
        self.move()
