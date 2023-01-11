import pygame.sprite
from tiles import Tile, StaticTile, Coins, Crate, Plams
from settings import tile_size, screen_height, screen_weight
from player import Player
from particles import ParticlesEffect
from support import import_csv_layout, import_cut_graphics
from map_data import levels
from enemy import Enemy
from decoration import Sky, Water, Cloud


class Level:
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # audio
        self.coin_sound = pygame.mixer.Sound('../audio/effects/coin.wav')
        self.coin_sound.set_volume(0.2)
        self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.wav')
        self.stomp_sound.set_volume(0.3)

        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[current_level]
        self.new_max_level = level_data['unlock']

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        # user interface
        self.change_coins = change_coins

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

        # explosion particles
        self.explosion_sprites = pygame.sprite.Group()

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles, change_health)
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
                            sprite = Coins(tile_size, x, y, '../graphics/coins/gold', 3)
                        if val == '1':
                            sprite = Coins(tile_size, x, y, '../graphics/coins/silver', 1)

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
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + \
                             self.crates_sprites.sprites() + \
                             self.fg_palm_sprites.sprites()

        for collidable_sprite in collidable_sprites:
            if collidable_sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = collidable_sprite.rect.right
                    # player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = collidable_sprite.rect.left
                    # player.on_right = True
                    self.current_x = player.rect.right

        # 左右碰撞时重置矩形
        # if player.on_left and (player.rect.left < self.current_x or player.direction.x > 0):
        #     player.on_left = False
        # if player.on_right and (player.rect.right > self.current_x or player.direction.x < 0):
        #     player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + \
                             self.crates_sprites.sprites() + \
                             self.fg_palm_sprites.sprites()

        for collidable_sprite in collidable_sprites:
            if collidable_sprite.rect.colliderect(player.collision_rect):
                if player.direction.y >= player.gravity:
                    player.collision_rect.bottom = collidable_sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = collidable_sprite.rect.bottom
                    player.direction.y = 1  # 撞到顶的时候让y为零 就会马上降落
                    # player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > player.gravity:
            player.on_ground = False
        # 检测天花板碰撞时重置矩形
        # if player.on_ceiling and player.direction.y > 0:
        #     player.on_ceiling = False

    def check_fall_map(self):
        if self.player.sprite.rect.top > screen_height:
            self.player.sprite.change_health(-10)
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coins_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)

        if collided_coins:
            # 一次碰撞多个硬币就一个声音
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)
                # 一次碰撞几个硬币就几个声音
                # self.coin_sound.play()

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemies_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_half_half = (enemy.rect.centery + enemy.rect.top) / 2
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom

                # jump kill
                if enemy_top <= player_bottom <= enemy_half_half and self.player.sprite.status == 'fall':  # 是否踩到了敌人的上半部分
                    enemy.kill()
                    explosion_sprite = ParticlesEffect(enemy.rect.center, 'enemy_explosion')
                    explosion_sprite.rect = explosion_sprite.image.get_rect(center=enemy.rect.center)
                    self.explosion_sprites.add(explosion_sprite)
                    self.player.sprite.jump()
                    self.stomp_sound.play()

                # knife kill
                # elif self.player.sprite.facing_right and self.player.sprite.rect.right - 10 <= enemy.rect.left:
                #     enemy.kill()
                #     explosion_sprite = ParticlesEffect(enemy.rect.center, 'enemy_explosion')
                #     explosion_sprite.rect = explosion_sprite.image.get_rect(center=enemy.rect.center)
                #     self.explosion_sprites.add(explosion_sprite)
                # elif not self.player.sprite.facing_right and self.player.sprite.rect.left + 10 >= enemy.rect.right:
                #     enemy.kill()
                #     explosion_sprite = ParticlesEffect(enemy.rect.center, 'enemy_explosion')
                #     explosion_sprite.rect = explosion_sprite.image.get_rect(center=enemy.rect.center)
                #     self.explosion_sprites.add(explosion_sprite)
                elif self.player.sprite.facing_right and self.player.sprite.rect.left + 50 >= enemy.rect.left or \
                        not self.player.sprite.facing_right and self.player.sprite.rect.right - 50 <= enemy.rect.right:
                    self.player.sprite.get_damage()

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
        # check enemy collision
        # self.collision_sprites.draw(self.display_surface)

        # explosion particles
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

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

        # player collision
        self.check_coins_collisions()
        self.check_enemy_collisions()

        self.check_fall_map()
        self.check_win()
        self.scroll_x()
