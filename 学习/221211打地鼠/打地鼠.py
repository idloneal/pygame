import random
import pygame
import sys

from pygame.math import Vector2


class Hamster(object):
    def __init__(self):
        self.hamsters = []
        self.lifetime = 100

    def add_hamster(self, cell_num):
        x = random.randint(0, cell_num - 1)
        y = random.randint(0, cell_num - 1)
        pos = Vector2(x, y)
        hamster_rect = pygame.Rect(pos.x * cell_size, pos.y * cell_size, cell_size, cell_size)
        self.hamsters.append([hamster_rect, self.lifetime])

    def draw_hamster(self, screen):
        if self.hamsters:
            self.delete_hamster()
            for hamster in self.hamsters:
                pygame.draw.ellipse(screen, (140, 16, 14), hamster[0])
                hamster[1] -= 1

    def delete_hamster(self):
        hamster_copy = [hamster for hamster in self.hamsters if hamster[1] > 0]
        self.hamsters = hamster_copy

    def remake_hamster(self):
        self.hamsters.pop()


class BackGround:
    def __init__(self, ):
        self.cell_num = 3
        self.bg_size = (self.cell_num * cell_size, self.cell_num * cell_size + 50)
        self.screen = pygame.display.set_mode(self.bg_size)

    def draw_bg(self):
        self.bg_size = (self.cell_num * cell_size, self.cell_num * cell_size + 20)
        self.screen = pygame.display.set_mode(self.bg_size)
        self.screen.fill((56, 80, 140))


pygame.init()
cell_size = 100
clock = pygame.time.Clock()
bg = BackGround()
hamster = Hamster()
init_score = 0
hamster_num = 1
score = 100
level = 0
level_copy = 1
font = pygame.font.Font(None, 30)
life = 3

while True:
    if life >0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hamster.hamsters:
                    if hamster.hamsters[0][0].collidepoint(pygame.mouse.get_pos()):
                        hamster.remake_hamster()
                        init_score += score
                        hamster_num += 1
                    else:
                        life -= 1
        bg.draw_bg()
        if not hamster.hamsters:
            hamster.add_hamster(bg.cell_num)
        hamster.draw_hamster(bg.screen)

        if hamster_num >= 8:
            if hamster.lifetime >= 30:
                hamster.lifetime -= (0.8**level_copy)*10
            else:
                level_copy += 1
            level += 1
            score *= 1.875
            hamster_num = 0
        if not level_copy % 4:
            bg.cell_num += 1
            level_copy = 1
        font_surface = font.render(('life:%d ' % life + 'level:%d' % level + '  score:%d' % init_score), False, "black")
        font_rect = font_surface.get_rect(midtop=(bg.cell_num * cell_size / 2, bg.cell_num * cell_size))
        bg.screen.blit(font_surface, font_rect)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        bg.draw_bg()
        game_over_font = pygame.font.Font(None, 30)
        game_over_surf = game_over_font.render('GG you score = %d' % init_score, False, "red")
        game_over_rect = game_over_surf.get_rect(center=bg.screen.get_rect().center)
        bg.screen.blit(game_over_surf, game_over_rect)
    pygame.display.update()
    clock.tick(60)
