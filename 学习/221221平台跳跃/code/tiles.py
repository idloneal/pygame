import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super(Tile, self).__init__()
        self.image = pygame.Surface((size, size))  # 砖块大小
        self.image.fill("grey")
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift  # 地图位移
