import random
from os import listdir

import pygame

from setting import *


def import_frames():
    surface_list = []
    path = '../graphics/plane'
    for image in listdir(path):
        full_path = path + '/' + image
        full_image = pygame.image.load(full_path).convert_alpha()
        surface_list.append(full_image)

    return surface_list


class BG(pygame.sprite.Sprite):

    def __init__(self, groups):
        # noinspection PyTypeChecker
        super(BG, self).__init__(groups)
        bg_image = pygame.image.load('../graphics/environment/background.png').convert_alpha()
        self.ratio = WINDOW_HEIGHT / bg_image.get_rect().height
        width = bg_image.get_rect().width * self.ratio
        image = pygame.transform.scale(bg_image, (width, WINDOW_HEIGHT))
        images = pygame.Surface((width, WINDOW_HEIGHT))
        images.fill('red')

        # double width background
        self.image = pygame.Surface((width * 2, WINDOW_HEIGHT))
        self.image.blit(image, (0, 0))
        self.image.blit(image, (width, 0))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.bg_speed = 300

    def update(self, dt):
        self.pos.x -= self.bg_speed * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.left = round(self.pos.x)


class Ground(BG):
    def __init__(self, groups):
        super(Ground, self).__init__(groups)
        ground_surf = pygame.image.load('../graphics/environment/ground.png').convert_alpha()
        width = ground_surf.get_width() * self.ratio
        height = ground_surf.get_height()
        self.image = pygame.transform.scale(ground_surf, (width, height))
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)

        self.sprite_type = 'ground'

class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super(Plane, self).__init__()
        # image
        self.frame_index = 0
        self.frames = import_frames()
        self.image = self.frames[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

        # rect
        width = WINDOW_WIDTH / 6
        height = WINDOW_HEIGHT / 2
        self.rect = self.image.get_rect(center=(width, height))

        # movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.gravity = 1500
        self.direction = 0

        # audio
        self.jump_sound = pygame.mixer.Sound('../sounds/jump.wav')
        self.jump_sound.set_volume(0.3)

    def animate(self, dt):
        self.frame_index += 30 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.direction = -800
        self.jump_sound.play()

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, (-self.direction * 0.06) + 10, 1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        self.animate(dt)
        self.rotate()
        self.apply_gravity(dt)


class Obstacle(BG):
    def __init__(self, groups):
        super(Obstacle, self).__init__(groups)

        self.sprite_type = 'obstacle'

        direction = random.choice(('up', 'down'))
        surf = pygame.image.load(f'../graphics/obstacles/{random.randint(0, 1)}.png').convert_alpha()

        ratio = random.uniform(1, 1.5)
        scale = pygame.math.Vector2(surf.get_size()) * ratio
        self.image = pygame.transform.scale(surf, scale)

        width = WINDOW_WIDTH + random.randint(0, 30)

        if direction == 'up':
            self.rect = self.image.get_rect(bottomleft=(width * 2, WINDOW_HEIGHT))
        else:
            self.image = pygame.transform.flip(self.image, True, True)
            self.rect = self.image.get_rect(topleft=(width, 0))

        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= self.bg_speed * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()
