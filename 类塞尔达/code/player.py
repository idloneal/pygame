import os
import pygame

from support import import_folder
from settings import *
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups,
                 obstacle_sprites,
                 create_attack,
                 del_attack,
                 create_magic,
                 del_magic):
        super().__init__(groups)
        # image
        self.animations = {}
        self.import_player_assets()
        self.image = self.animations['down_idle'][self.frame_index]

        # rect
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(HITBOX_OFFSET['player'])

        # movement
        self.status = 'down'

        # obstacle
        self.obstacle_sprites = obstacle_sprites

        # attack
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # weapon
        self.create_attack = create_attack
        self.del_attack = del_attack
        self.weapon_index = 0
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
        self.switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magic
        self.create_magic = create_magic
        self.del_magic = del_magic
        self.magic_index = 0
        self.magic = list(MAGIC_DATA.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # attribute
        self.attribute = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 10, 'move_speed': 4}
        self.max_attribute = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 60, 'move_speed': 8}
        self.upgrade_cost = {'health': 100, 'energy': 50, 'attack': 100, 'magic': 50, 'move_speed': 100}
        self.health = self.attribute['health']
        self.energy = self.attribute['energy']
        self.exp = 0
        self.move_speed = self.attribute['move_speed']

        # sound
        self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.15)

    def import_player_assets(self):
        player_assets_path = '../graphics/player/'
        for tile in os.listdir(player_assets_path):
            path = player_assets_path + '/' + tile
            self.animations[tile] = import_folder(path)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            # vertical move
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
            else:
                self.direction.y = 0

            # horizontal move
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = +1
            else:
                self.direction.x = 0
        else:
            self.direction = pygame.math.Vector2(0, 0)

        # attack
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_cooldown = list(WEAPON_DATA.values())[self.weapon_index]['cooldown']
            self.attack_time = pygame.time.get_ticks()
            self.weapon_attack_sound.play()
            self.create_attack()

        # magic
        if keys[pygame.K_c] and not self.attacking:
            self.attacking = True
            self.attack_cooldown = 800
            self.attack_time = pygame.time.get_ticks()
            style = list(MAGIC_DATA.keys())[self.magic_index]
            mana = list(MAGIC_DATA.values())[self.magic_index]['mana'] + self.attribute['magic']
            cost = list(MAGIC_DATA.values())[self.magic_index]['cost']
            self.create_magic(style, mana, cost)

        # switch weapon
        if keys[pygame.K_z] and self.switch_weapon:
            self.weapon_index += 1
            if self.weapon_index > len(WEAPON_DATA.keys()) - 1:
                self.weapon_index = 0
            self.weapon_switch_time = pygame.time.get_ticks()
            self.switch_weapon = False

        # switch magic
        if keys[pygame.K_x] and self.can_switch_magic:
            self.magic_index += 1
            if self.magic_index > len(MAGIC_DATA.keys()) - 1:
                self.magic_index = 0
            self.magic_switch_time = pygame.time.get_ticks()
            self.can_switch_magic = False

    def get_status(self):
        # move
        if not self.attacking:
            if self.direction.x > 0:
                self.status = 'right'
            if self.direction.x < 0:
                self.status = 'left'
            if self.direction.y > 0:
                self.status = 'down'
            if self.direction.y < 0:
                self.status = 'up'

        # idle
        if 'idle' not in self.status and 'attack' not in self.status:
            if not self.direction.x and not self.direction.y:
                self.status = self.status + '_idle'

        # attack
        if 'attack' not in self.status:
            if self.attacking:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if not self.attacking:
                self.status = self.status.replace('_attack', '')

    def animate(self):
        self.frame_index += self.frame_speed
        if self.frame_index >= len(self.animations[self.status]):
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
        if self.attacking:
            if self.attack_time + self.attack_cooldown <= current_time:
                self.attacking = False
                self.del_attack()

        # switch weapon timer
        if not self.switch_weapon:
            if self.weapon_switch_time + self.switch_duration_cooldown <= current_time:
                self.switch_weapon = True

        # switch magic timer
        if not self.can_switch_magic:
            if self.magic_switch_time + self.switch_duration_cooldown <= current_time:
                self.can_switch_magic = True

        # invincibility time
        if self.invincibility:
            if current_time - self.hurt_time >= self.invincibility_time:
                self.invincibility = False

    def create_weapon(self):
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]

    def get_full_weapon_damage(self):
        base_damage = self.attribute['attack']
        weapon_damage = WEAPON_DATA[self.weapon]['damage']

        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.attribute['magic']
        spell_damage = MAGIC_DATA[self.magic]['mana'] * 2

        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.attribute.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy <= self.attribute['energy']:
            self.energy += 0.001 * self.attribute['magic']
        else:
            self.energy = self.attribute['energy']

    def update(self):
        self.input()
        self.get_status()
        self.cooldown()
        self.create_weapon()
        self.animate()
        self.move(self.attribute['move_speed'])
        self.energy_recovery()
