import pygame
import sys


class PLayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((230, 230, 230))
        self.rect = self.image.get_rect(center=(400, 400))
        self.current_health = 200
        self.target_health = 500
        self.maximum_health = 1003
        self.health_bar_length = 430
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_change_speed = 1

    def update(self):
        self.basic_health()
        self.advanced_health()

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.maximum_health:
            self.target_health += amount
        if self.target_health > self.maximum_health:
            self.target_health = self.maximum_health

    def basic_health(self):
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, self.target_health / self.health_ratio, 25))
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, self.health_bar_length, 25), 4)

    def advanced_health(self):
        transition_width = 0
        transition_color = (255, 0, 0)
        bar_rect = 0
        health_bar_rect = 0

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = abs(int((self.target_health - self.current_health) / self.health_ratio))
            transition_color = (0, 255, 0)
            health_bar_rect = pygame.Rect(10, 45, self.current_health / self.health_ratio, 25)  # 计算红色血条
            bar_rect = health_bar_rect.right
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = abs(int((self.target_health - self.current_health) / self.health_ratio))
            transition_color = (255, 255, 0)
            bar_rect = int(self.target_health / self.health_ratio) + 13  # 血条起始位置在10 速度有5消除误差
        if abs(transition_width) < (self.health_change_speed / self.health_ratio):  # 防止transition无法通过加减法到达目标值
            transition_width = 0

        transition_bar_rect = pygame.Rect(bar_rect, 45, transition_width, 25)

        pygame.draw.rect(screen, (255, 0, 0), health_bar_rect)
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen, (255, 255, 255), (10, 45, self.health_bar_length, 25), 4)


pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
player = pygame.sprite.GroupSingle(PLayer())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.sprite.get_health(100)
            if event.key == pygame.K_LEFT:
                player.sprite.get_damage(83)

    screen.fill((30, 30, 30))
    player.draw(screen)
    player.update()
    pygame.display.update()
    clock.tick(60)
