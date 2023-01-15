import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos,groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/player/down_idle/idle_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -30)

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.move_speed = 5

        # obstacle
        self.obstacle_sprites = obstacle_sprites

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

    def move(self):
        if self.direction.magnitude() != 0:  # 计算矢量长
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.move_speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.move_speed
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

    def update(self):
        self.input()
        self.move()
