import pygame
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('ship.png').convert_alpha()
        self.rect = self.image.get_rect(center=(400, 400))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.mouse.get_pos():
            self.rect.center = pygame.mouse.get_pos()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        self.image = pygame.image.load('alpha.png').convert_alpha()
        self.rect = self.image.get_rect(center=(400, 400))
        self.mask = pygame.mask.from_surface(self.image)
        # self.image = self.mask.to_surface()
        # self.image.set_colorkey((0,0,0))


# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

# group setup
player = pygame.sprite.GroupSingle(Player())
obstacle = pygame.sprite.GroupSingle(Obstacle())

new_obstacle_surf = obstacle.sprite.mask.to_surface()
new_obstacle_surf.set_colorkey((0, 0, 0))
new_obstacle_rect = obstacle.sprite.rect

# 用颜色填充
surf_w, surf_h = new_obstacle_surf.get_size()
for x in range(surf_w):
    for y in range(surf_h):
        if new_obstacle_surf.get_at((x, y))[0] != 0:
            new_obstacle_surf.set_at((x, y), 'orange')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_RIGHT:

        #     if event.key == pygame.K_LEFT:

    screen.fill('grey')

    # update and draw
    player.update()
    player.draw(screen)

    # 做一个轮廓
    # offset = 4
    # screen.blit(new_obstacle_surf, (new_obstacle_rect[0] + offset, new_obstacle_rect[0]))
    # screen.blit(new_obstacle_surf, (new_obstacle_rect[0] - offset, new_obstacle_rect[0]))
    # screen.blit(new_obstacle_surf, (new_obstacle_rect[0] + offset, new_obstacle_rect[0] - offset))  # topright
    # screen.blit(new_obstacle_surf, (new_obstacle_rect[0] - offset, new_obstacle_rect[0] - offset))  # topleft
    # screen.blit(new_obstacle_surf, (new_obstacle_rect[0] + offset, new_obstacle_rect[0] + offset))  # bottomright
    # screen.blit(new_obstacle_surf, (new_obstacle_rect[0] - offset, new_obstacle_rect[0] + offset))  # bottomleft
    obstacle.draw(screen)

    # collision
    # if pygame.sprite.spritecollide(player.sprite, obstacle, False):
    #     # noinspection PyTypeChecker
    #     if pygame.sprite.spritecollide(player.sprite, obstacle, False, pygame.sprite.collide_mask):
    #         player.sprite.image.set_alpha(0)
    #     else:
    #         player.sprite.image.set_alpha(255)

    # area collision 没有精灵组的情况下也能实现
    offset_x = obstacle.sprite.rect.x - player.sprite.rect.x
    offset_y = obstacle.sprite.rect.y - player.sprite.rect.y
    # 返回元组
    # if player.sprite.mask.overlap(obstacle.sprite.mask, (offset_x, offset_y)):
    #     print(player.sprite.mask.overlap(obstacle.sprite.mask, (offset_x, offset_y)))

    # 返回区域大小
    # if player.sprite.mask.overlap_area(obstacle.sprite.mask, (offset_x, offset_y)) >= 1000:
    #     print(player.sprite.mask.overlap_area(obstacle.sprite.mask, (offset_x, offset_y)))

    # 检测轮廓位置
    # for point in obstacle.sprite.mask.outline():
    #     x = point[0]+obstacle.sprite.rect.left
    #     y = point[1]+obstacle.sprite.rect.top
    #     pygame.draw.circle(screen,'red',(x,y),3)

    # new  surf color
    if player.sprite.mask.overlap(obstacle.sprite.mask, (offset_x, offset_y)):
        new_mask = player.sprite.mask.overlap_mask(obstacle.sprite.mask, (offset_x, offset_y))
        new_surf = new_mask.to_surface()
        new_surf.set_colorkey((0, 0, 0))

        surf_w, surf_h = new_surf.get_size()
        for x in range(surf_w):
            for y in range(surf_h):
                if new_surf.get_at((x, y))[0] != 0:
                    new_surf.set_at((x, y), 'orange')

        screen.blit(new_surf, player.sprite.rect)

    pygame.display.update()
    clock.tick(60)
