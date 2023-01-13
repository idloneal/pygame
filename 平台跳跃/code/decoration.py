import random

import pygame
from settings import VERTICAL_TITLE_NUMBER, TILE_SIZE, SCREEN_WIDTH
from tiles import AnimationTile, StaticTile
from support import import_folder


class Sky:
    def __init__(self, horizon, style='level'):
        self.top = pygame.image.load('../graphics/decoration/sky/sky_top.png')
        self.bottom = pygame.image.load('../graphics/decoration/sky/sky_bottom.png')
        self.middle = pygame.image.load('../graphics/decoration/sky/sky_middle.png')
        self.horizon = horizon

        # stretch
        self.top = pygame.transform.scale(self.top, (SCREEN_WIDTH, TILE_SIZE))
        self.bottom = pygame.transform.scale(self.bottom, (SCREEN_WIDTH, TILE_SIZE))
        self.middle = pygame.transform.scale(self.middle, (SCREEN_WIDTH, TILE_SIZE))

        # style
        self.style = style
        if self.style == 'overworld':
            palms_surf = import_folder('../graphics/overworld/palms')
            self.palms = []

            for surface in [random.choice(palms_surf) for _ in range(20)]:
                x = random.randint(0, SCREEN_WIDTH)
                y = (self.horizon * TILE_SIZE) + random.randint(50, 100)
                rect = surface.get_rect(midbottom=(x, y))
                self.palms.append((surface, rect))

            clouds_surf = import_folder('../graphics/overworld/clouds')
            self.clouds = []

            for surface in [random.choice(clouds_surf) for _ in range(8)]:
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(100, self.horizon * TILE_SIZE - 100)
                rect = surface.get_rect(midbottom=(x, y))
                self.clouds.append((surface, rect))

    def draw(self, surface):
        for row in range(VERTICAL_TITLE_NUMBER):
            y = row * TILE_SIZE
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            if row == self.horizon:
                surface.blit(self.middle, (0, y))
            if row > self.horizon:
                surface.blit(self.bottom, (0, y))

        if self.style == 'overworld':
            for palm in self.palms:
                surface.blit(palm[0], palm[1])
            for cloud in self.clouds:
                surface.blit(cloud[0], cloud[1])


class Water:
    def __init__(self, top, level_width):
        water_start = -SCREEN_WIDTH / 2
        water_tile_width = 192  # 水的宽度
        tile_x_amount = int((level_width + SCREEN_WIDTH) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimationTile(192, x, y, '../graphics/decoration/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, x_shift):
        self.water_sprites.draw(surface)
        self.water_sprites.update(x_shift)


class Cloud:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surf_list = import_folder('../graphics/decoration/clouds')
        min_x = -SCREEN_WIDTH / 2
        max_x = level_width + SCREEN_WIDTH / 2
        min_y = 0
        max_y = horizon
        self.cloud_sprite = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = random.choice(cloud_surf_list)
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
            spite = StaticTile(0, cloud, x, y)
            self.cloud_sprite.add(spite)

    def draw(self, surface, x_shift):
        self.cloud_sprite.draw(surface)
        self.cloud_sprite.update(x_shift)
