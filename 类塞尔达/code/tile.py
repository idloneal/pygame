import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if self.sprite_type == 'invisible':
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(HITBOX_OFFSET[self.sprite_type])
            self.image.set_alpha(0)
        elif self.sprite_type == 'object':
            self.rect = self.image.get_rect(midleft=pos)
            self.hitbox = self.rect.inflate(HITBOX_OFFSET[self.sprite_type])
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(HITBOX_OFFSET[self.sprite_type])
