import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprites_type, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.sprites_type = sprites_type
        self.image = surface
        if self.sprites_type == 'invisible':
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-20, 40)
            self.image.set_alpha(0)
        elif self.sprites_type == 'object':
            self.rect = self.image.get_rect(midleft=pos)
            self.hitbox = self.rect.inflate(0, -80)
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -20)
