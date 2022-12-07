import pygame
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/link.png").convert_alpha()  # 使用 convert 可以转换格式，提高 blit 的速度
        # 其中 convert_alpha相对于convert，保留了图像的Alpha 通道信息，可以认为是保留了透明的部分，实现了透明转换
        self.rect = self.image.get_rect(center=(400, 400))
        self.health = 5
        self.max_health = 16

    def get_damage(self):
        if self.health > 0:
            self.health -= 1

    def get_health(self):
        if self.health < self.max_health:
            self.health += 1

    def full_hearts(self):
        for heart in range(self.health):
            screen.blit(full_heart, (heart * 50, 0))

    # def empty_hearts(self):  # 用满的血覆盖空的
    #     for heart in range(self.max_health):
    #         screen.blit(empty_heart, (heart * 50, 40))
    #     for heart in range(self.health):
    #         screen.blit(full_heart, (heart * 50, 40))
    #
    # def half_hearts(self):  # 用半血覆盖空血 半心和满心交替 覆盖空血
    #     for heart in range(int(self.max_health / 2)):
    #         screen.blit(empty_heart, (heart * 50, 80))
    #     for heart in range(self.health):
    #         screen.blit(half_heart, ((heart // 2) * 50, 80))
    #         screen.blit(full_heart, (((heart-1) // 2) * 50, 80))

    def empty_hearts(self):  # 低于目前血量的显示满心 否则显示空心
        for heart in range(self.max_health):
            if heart < self.health:
                screen.blit(full_heart, (heart * 50, 40))
            else:
                screen.blit(empty_heart, (heart * 50, 40))

    def half_hearts(self):  # 高于目前血量显示空心 低于目前血量一半的整数显示满心
        for heart in range(self.max_health):
            if heart > self.health:
                screen.blit(empty_heart, ((heart // 2) * 50, 80))
            elif heart < self.health:   # 这样做如果是奇数血量 则会空出当前一格
                screen.blit(full_heart, (((heart-1) // 2) * 50, 80))
            if self.health % 2 == 1:  # 如果有半血 则在当前位置生成一个半心
                screen.blit(half_heart, ((self.health // 2) * 50, 80))



    def update(self):
        self.full_hearts()
        self.empty_hearts()
        self.half_hearts()


pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
link = pygame.sprite.GroupSingle(Player())  # 容器只保存一个精灵。添加新精灵时,旧精灵将被移除

full_heart = pygame.image.load('sprites/full_heart.png').convert_alpha()
half_heart = pygame.image.load('sprites/half_heart.png').convert_alpha()
empty_heart = pygame.image.load('sprites/empty_heart.png').convert_alpha()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                link.sprite.get_health()
            if event.key == pygame.K_LEFT:
                link.sprite.get_damage()

    screen.fill((30, 30, 30))
    link.draw(screen)
    link.update()
    pygame.display.update()
    clock.tick(60)
