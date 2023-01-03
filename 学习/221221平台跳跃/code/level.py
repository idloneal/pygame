import pygame.sprite

from tiles import *
from settings import *
from player import Player
from particles import ParticlesEffect
from support import import_csv_layout, import_cut_graphics
from map_data import levels
from enemy import Enemy
from decoration import *


class Level:
    # level setup
    def __init__(self, current_level, surface, create_overworld):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = 0

        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[current_level]
        self.new_max_level = level_data['unlock']

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crate
        crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crates_layout, 'crates')

        # coins
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')

        # foreground plams
        fg_palm_layout = import_csv_layout(level_data['fg_palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg_palms')

        # background plams
        bg_palm_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg_palms')

        # enemy
        enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(enemies_layout, 'enemies')

        # collision
        collision_layout = import_csv_layout(level_data['collision'])
        self.collision_sprites = self.create_tile_group(collision_layout, 'collision')

        # decoration
        self.sky = Sky(7)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 30, level_width)
        self.clouds = Cloud(screen_height * 0.5, level_width, 40)

        # dust particles
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(player_sprite)
                if val == '1':
                    hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    goal_sprite = StaticTile(tile_size, hat_surface, x, y)
                    self.goal.add(goal_sprite)

    @staticmethod
    def create_tile_group(layout, type):
        sprite_group = pygame.sprite.Group()
        sprite = None

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, tile_surface, x, y)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, tile_surface, x, y)

                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    if type == 'coins':
                        if val == '0':
                            sprite = Coins(tile_size, x, y, '../graphics/coins/gold')
                        if val == '1':
                            sprite = Coins(tile_size, x, y, '../graphics/coins/silver')

                    if type == 'fg_palms':
                        if val == '4':
                            sprite = Plams(tile_size, x, y, '../graphics/terrain/palm_large')
                        if val == '8':
                            sprite = Plams(tile_size, x, y, '../graphics/terrain/palm_small')

                    if type == 'bg_palms':
                        sprite = Plams(tile_size, x, y, '../graphics/terrain/palm_bg')

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'collision':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def enemy_collision_constraint(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.collision_sprites, False):
                self.enemies_sprites.sprites()
                enemy.reverse()

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 0)
        else:
            pos -= pygame.math.Vector2(-10, 0)
        jump_particle_sprite = ParticlesEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                self.vertical_movement_collision()
                offset = pygame.math.Vector2(10, 0)
            else:
                offset = pygame.math.Vector2(-10, 0)
            fall_dust_particle = ParticlesEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_weight / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_weight * 0.75 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + \
                             self.crates_sprites.sprites() + \
                             self.fg_palm_sprites.sprites()

        for collidable_sprite in collidable_sprites:
            if collidable_sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = collidable_sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = collidable_sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x > 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x < 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + \
                             self.crates_sprites.sprites() + \
                             self.fg_palm_sprites.sprites()

        for collidable_sprite in collidable_sprites:
            if collidable_sprite.rect.colliderect(player.rect):
                if player.direction.y > player.gravity:
                    player.rect.bottom = collidable_sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = collidable_sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > player.gravity:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def run(self):

        # decoration sky&cloud
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # background palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # crates
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)

        # enemy & collision
        self.collision_sprites.update(self.world_shift)
        self.enemies_sprites.update(self.world_shift)
        self.enemy_collision_constraint()
        self.enemies_sprites.draw(self.display_surface)
        # self.collision_sprites.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)

        # foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)

        self.check_death()
        self.check_win()
        self.scroll_x()
