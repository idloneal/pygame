import os
import pygame

def import_folder(path):
    surface_list = []
    for image in os.listdir(path):
        full_path = path + '/' + image
        image_full = pygame.image.load(full_path).convert_alpha()
        surface_list.append(image_full)

    return surface_list