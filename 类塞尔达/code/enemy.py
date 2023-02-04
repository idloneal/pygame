import pygame
import os
from settings import *
from entity import Entity
from support import import_folder


class Enemy(Entity):
    def __init__(self, enemy_name, pos, groups,
                 obstacle_sprites,
                 damage_player,
                 death_particles,
                 add_exp):
        super(Enemy, self).__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.animations = {}
        self.import_graphics(enemy_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # rect
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # attribute
        self.enemy_name = enemy_name
        enemy_info = ENEMY_DATA[self.enemy_name]
        self.health = enemy_info['health']
        self.exp = enemy_info['exp']
        self.speed = enemy_info['speed']
        self.attack_damage = enemy_info['damage']
        self.resistance = enemy_info['resistance']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']
        self.attack_type = enemy_info['attack_type']
        self.add_exp = add_exp

        # attack player
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.death_particles = death_particles

        # sounds
        self.death_sound = pygame.mixer.Sound('../audio/death.wav')
        self.death_sound.set_volume(0.1)
        self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')
        self.hit_sound.set_volume(0.1)
        self.attack_sound = pygame.mixer.Sound(enemy_info['attack_sound'])
        self.attack_sound.set_volume(0.25)

    def import_graphics(self, name):
        graphics_path = f'../graphics/monsters/{name}/'
        for tile in os.listdir(graphics_path):
            path = graphics_path + '/' + tile
            self.animations[tile] = import_folder(path)

    def get_player_distance_direction(self, player):
        enemy_pos = pygame.math.Vector2(self.rect.center)
        player_pos = pygame.math.Vector2(player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()

        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return distance, direction

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        self.frame_index += self.frame_speed
        if self.frame_index >= len(self.animations[self.status]):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker
        if self.invincibility:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        # attack time
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        # invincibility time
        if self.invincibility:
            if current_time - self.hurt_time >= self.invincibility_time:
                self.invincibility = False

    def get_damage(self, player, attack_type):
        if not self.invincibility:
            self.hit_sound.play()
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hurt_time = pygame.time.get_ticks()
            self.invincibility = True

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.add_exp(self.exp)
            self.death_particles(self.rect.center, self.enemy_name)
            self.death_sound.play()

    def hit_reaction(self):
        if self.invincibility:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
