import os
import pygame

from csv import reader

def import_csv_layout(path):
    layout_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            layout_map.append(list(row))
        return layout_map


def import_folder(path):
    surface_list = []
    for name in os.listdir(path):
        full_path = path + '/' + name
        image_surf = pygame.image.load(full_path).convert_alpha()
        surface_list.append((image_surf))

    return surface_list
