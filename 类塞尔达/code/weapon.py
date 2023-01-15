import pygame
from pygame.math import Vector2
# from settings import WEAPON_DATA


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.direction = self.player.status.split('_')[0]

        # image
        path = f'../graphics/weapons/{self.player.weapon}/{self.direction}.png'
        self.image = pygame.image.load(path).convert_alpha()
        if self.direction == 'up':
            self.rect = self.image.get_rect(midbottom=self.player.rect.midtop + Vector2(-12, 0))
        elif self.direction == 'down':
            self.rect = self.image.get_rect(midtop=self.player.rect.midbottom + Vector2(16, 0))
        elif self.direction == 'left':
            self.rect = self.image.get_rect(midright=self.player.rect.midleft + Vector2(0, 16))
        elif self.direction == 'right':
            self.rect = self.image.get_rect(midleft=self.player.rect.midright + Vector2(0, 16))


    def movement(self):
        if self.direction == 'up':
            self.rect = self.image.get_rect(midbottom=self.player.rect.midtop + Vector2(-12, 0))
        elif self.direction == 'down':
            self.rect = self.image.get_rect(midtop=self.player.rect.midbottom + Vector2(16, 0))
        elif self.direction == 'left':
            self.rect = self.image.get_rect(midright=self.player.rect.midleft + Vector2(0, 16))
        elif self.direction == 'right':
            self.rect = self.image.get_rect(midleft=self.player.rect.midright + Vector2(0, 16))

    def update(self):
        self.movement()
