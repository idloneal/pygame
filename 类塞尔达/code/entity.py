import math

import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        # animation
        self.frame_index = 0
        self.frame_speed = 0.15

        # transition
        self.rect = None
        self.hitbox = None
        self.obstacle_sprites = None

        # movement
        self.direction = pygame.math.Vector2()

        # invincibility  timer
        self.invincibility = False
        self.hurt_time = None
        self.invincibility_time = 300

    def move(self, speed):
        if self.direction.magnitude() != 0:  # 计算矢量长
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

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

    @staticmethod
    def wave_value():
        value = math.sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
