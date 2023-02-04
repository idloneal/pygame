import random
import pygame
from settings import *
from tile import Tile
from support import import_csv_layout, import_folder
from player import Player
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationParticle
from magic import Magic
from upgrade import Upgrade


class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.Sprite

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_particle = AnimationParticle()
        self.player_magic = Magic(self.animation_particle)

    def create_map(self):
        layouts = {
            'floor_block': import_csv_layout('../map/test_map/test_map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/test_map/test_map_Grass.csv'),
            'object': import_csv_layout('../map/test_map/test_map_Objects.csv'),
            'entities': import_csv_layout('../map/test_map/test_map_Entities.csv'),
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
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                 'grass',
                                 graphics['grass'][int(col)])
                        if type == 'object':
                            Tile((x, y),
                                 [self.visible_sprites, self.obstacle_sprites],
                                 'object',
                                 graphics['object'][int(col)])
                        if type == 'entities':
                            if col == '394':
                                self.player = Player((x, y),
                                                     [self.visible_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.del_attack,
                                                     self.create_magic,
                                                     self.del_magic)
                            else:
                                if col == '390':
                                    enemy_name = 'bamboo'
                                elif col == '391':
                                    enemy_name = 'spirit'
                                elif col == '392':
                                    enemy_name = 'raccoon'
                                else:
                                    enemy_name = 'squid'
                                Enemy(enemy_name,
                                      (x, y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player,
                                      self.death_particles,
                                      self.add_exp
                                      )

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def del_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, mana, cost):
        if style == 'heal':
            self.player_magic.heal(self.player, mana, cost, [self.visible_sprites])
        elif style == 'flame':
            self.player_magic.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def del_magic(self):
        # if self.current_magic:
        #     self.current_magic.kill()
        # self.current_magic = None
        pass

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprite = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprite:
                    for target_sprite in collision_sprite:
                        if target_sprite.sprite_type == 'grass':
                            # kill grass particles
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(random.randint(3, 6)):
                                self.animation_particle.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if not self.player.invincibility:
            self.player.health -= amount
            self.player.invincibility = True
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_particle.create_player_particles(attack_type, self.player.rect.center,
                                                            [self.visible_sprites])

    def death_particles(self, pos, particle_type):
        self.animation_particle.create_player_particles(particle_type, pos, [self.visible_sprites])

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()


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

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
