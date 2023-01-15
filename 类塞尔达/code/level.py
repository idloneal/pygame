import pygame
from settings import *
from tile import Tile
from support import import_csv_layout, import_folder
from player import Player
from weapon import Weapon
from debug import debug


class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.Sprite

        # attack sprites
        self.current_attack = None

        # sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
            'floor_block': import_csv_layout('../map/test_map/test_map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/test_map/test_map_Grass.csv'),
            'object': import_csv_layout('../map/test_map/test_map_Objects.csv')
        }
        graphics = {
            'grass': import_folder('../graphics/grass'),
            'object': import_folder('../graphics/objects')
        }

        for type, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if type == 'floor_block':
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'invisible')
                        if type == 'grass':
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass',
                                 graphics['grass'][int(col)])
                        if type == 'object':
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object',
                                 graphics['object'][int(col)])

        self.player = Player((38 * TILE_SIZE, 35 * TILE_SIZE), self.visible_sprites,
                             self.obstacle_sprites, self.create_attack, self.del_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def del_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player)
        debug(self.player.weapon)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super(YSortCameraGroup, self).__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        # create floor
        self.floor_surf = pygame.image.load('../map/create_map/test_map/test_map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # 让人物在中间保持不动地图动
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        # draw floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprites: sprites.rect.centery):  # 以精灵的y坐标进行重新排序
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
