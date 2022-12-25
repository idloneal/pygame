import pygame
from support import import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super(Tile, self).__init__()
        self.image = pygame.Surface((size, size))  # 砖块大小
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x_shift):
        self.rect.x += x_shift  # 地图位移


class StaticTile(Tile):
    def __init__(self, size, surface, x, y):
        super(StaticTile, self).__init__(size, x, y)
        self.image = surface


class Crate(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, pygame.image.load('../graphics/terrain/crate.png').convert_alpha(), x, y)
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class AnimationTile(Tile):
    def __init__(self, size, x, y, path):
        super(AnimationTile, self).__init__(size, x, y)
        self.frames = import_folder(path)
        self.frames_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.frames_index]

    def animation(self):
        self.frames_index += self.animation_speed
        if self.frames_index >= len(self.frames):
            self.frames_index = 0
        self.image = self.frames[int(self.frames_index)]

    def update(self, x_shift):
        self.animation()
        self.rect.x += x_shift


class Coins(AnimationTile):
    def __init__(self, size, x, y, path):
        super(Coins, self).__init__(size, x, y, path)
        offset_x = x + (size / 2)
        offset_y = y + (size / 2)
        self.rect = self.image.get_rect(center=(offset_x, offset_y))


class Plams(AnimationTile):
    def __init__(self, size, x, y, path):
        super(Plams, self).__init__(size, x, y, path)
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))
