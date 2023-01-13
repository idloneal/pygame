import pygame
from os import listdir
from csv import reader
from settings import TILE_SIZE


def import_folder(path):
    surface_list = []

    for image in listdir(path):
        full_path = path + '/' + image
        full_image = pygame.image.load(full_path).convert_alpha()
        surface_list.append(full_image)

    return surface_list


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_num_y = int(surface.get_size()[1] / TILE_SIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            new_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))  # 切割图片
            cut_tiles.append(new_surf)
    return cut_tiles
