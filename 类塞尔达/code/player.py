import os
import pygame
from support import import_folder
from settings import WEAPON_DATA


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, del_attack):
        super().__init__(groups)
        # image
        self.animations = {}
        self.import_player_assets()
        self.frame_index = 0
        self.frame_speed = 0.1
        self.image = self.animations['down_idle'][self.frame_index]

        # rect
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -30)

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.move_speed = 5
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

    def import_player_assets(self):
        player_assets_path = '../graphics/player/'
        for tile in os.listdir(player_assets_path):
            path = player_assets_path + '/' + tile
            self.animations[tile] = import_folder(path)
        print([i for i in self.animations])

    def input(self):
        keys = pygame.key.get_pressed()

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

        # attack
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_cooldown = list(WEAPON_DATA.values())[self.weapon_index]['cooldown']
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()

        # magic
        if keys[pygame.K_c] and not self.attacking:
            self.attacking = True
            self.attack_cooldown = 800
            self.attack_time = pygame.time.get_ticks()

        # switch weapon
        if keys[pygame.K_z] and self.switch_weapon:
            self.weapon_index -= 1
            if self.weapon_index < 0:
                self.weapon_index = len(WEAPON_DATA.keys()) - 1
            self.weapon_switch_time = pygame.time.get_ticks()
            self.switch_weapon = False
        if keys[pygame.K_x] and self.switch_weapon:
            self.weapon_index += 1
            if self.weapon_index >= len(WEAPON_DATA.keys()):
                self.weapon_index = 0
            self.weapon_switch_time = pygame.time.get_ticks()
            self.switch_weapon = False

    def move(self):
        if self.direction.magnitude() != 0:  # 计算矢量长
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.move_speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.move_speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

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

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldown(self):
        if self.attacking:
            if self.attack_time + self.attack_cooldown <= pygame.time.get_ticks():
                self.attacking = False
                self.del_attack()

        if not self.switch_weapon:
            if self.weapon_switch_time + self.switch_duration_cooldown <= pygame.time.get_ticks():
                self.switch_weapon = True

    def create_weapon(self):
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]

    def update(self):
        self.input()
        self.get_status()
        self.cooldown()
        self.create_weapon()
        self.animate()
        self.move()
