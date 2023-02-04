import random

import pygame
from settings import *


class Magic:
    def __init__(self, animation_particle):
        self.animation_particle = animation_particle
        self.sounds = {
            'heal': pygame.mixer.Sound('../audio/heal.wav'),
            'flame': pygame.mixer.Sound('../audio/Fire.wav')
        }
        self.sounds['heal'].set_volume(0.6)
        self.sounds['flame'].set_volume(0.25)

    def heal(self, player, mana, cost, groups):
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.energy -= cost
            player.health += mana
            if player.health >= player.attribute['health']:
                player.health = player.attribute['health']
            pos = player.rect.center
            offset_pos = pos + pygame.math.Vector2(0, -60)
            self.animation_particle.create_player_particles('heal', offset_pos, groups)
            self.animation_particle.create_player_particles('aura', pos, groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            self.sounds['flame'].play()
            if player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            elif player.status.split('_')[0] == 'down':
                direction = pygame.math.Vector2(0, 1)
            elif player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            else:
                direction = pygame.math.Vector2(-1, 0)

            for i in range(1, 6):
                if direction.x:
                    offset_x = (direction.x * i) * TILE_SIZE + random.randint(-TILE_SIZE // 6, TILE_SIZE // 6)
                    offset_y = random.randint(-TILE_SIZE // 6, TILE_SIZE // 6)
                    # offset_y = TILE_SIZE//6 * (-1) ** i
                    x = player.rect.centerx + offset_x
                    y = player.rect.centery + offset_y
                    self.animation_particle.create_player_particles('flame', (x, y), groups)
                else:
                    offset_x = random.randint(-32, 32) + random.randint(-TILE_SIZE // 6, TILE_SIZE // 6)
                    offset_y = (direction.y * i) * TILE_SIZE + random.randint(-TILE_SIZE // 6, TILE_SIZE // 6)
                    x = player.rect.centerx + offset_x
                    y = player.rect.centery + offset_y
                    self.animation_particle.create_player_particles('flame', (x, y), groups)
