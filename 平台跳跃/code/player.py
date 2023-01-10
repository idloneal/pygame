import pygame
from support import import_folder
from math import sin


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
        super(Player, self).__init__()
        self.animations = {}
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # dust particles
        self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.jump_num = 0

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # health
        self.change_health = change_health
        self.invincible = False
        self.invincible_frame = 800
        self.hurt_time = 0

    def import_character_assets(self):
        character_path = '../graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        # loop frame
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # 设置矩形在正确位置
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = dust_particle.get_rect(bottomleft=self.rect.bottomleft)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = dust_particle.get_rect(bottomright=self.rect.bottomright)
                flipped_image = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_image, pos)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        else:
            self.direction.x = 0

        if keys[pygame.K_j] or keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = 'idle'
        elif self.direction.x != 0 and self.direction.y == self.gravity or self.direction.y == 0:
            self.status = 'run'
        elif self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > self.gravity:
            self.status = 'fall'
        else:
            self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def get_damage(self):
        if not self.invincible:
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincible_time(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if self.hurt_time + self.invincible_frame <= current_time:
                self.invincible = False

    def invincible_animate(self):
        if self.invincible:
            value = self.wave_value()
            self.image.set_alpha(value)
        else:
            self.image.set_alpha(255)

    @staticmethod
    def wave_value():
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincible_time()
        self.invincible_animate()
