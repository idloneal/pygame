import pygame
import sys
import time

from setting import *
from sprites import BG, Ground, Plane, Obstacle


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy bird')
        self.clock = pygame.time.Clock()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # background
        # noinspection PyTypeChecker
        BG(self.all_sprites)
        # noinspection PyTypeChecker
        Ground([self.all_sprites, self.collision_sprites])
        self.plane = Plane()
        self.all_sprites.add(self.plane)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # text
        self.font = pygame.font.Font('../graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0

        # game over
        self.game_over = True

        # game start
        self.menu_surf = pygame.image.load('../graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.start_time = 0

        # audio
        self.bg_sound = pygame.mixer.Sound('../sounds/music.wav')
        self.bg_sound.set_volume(0.3)
        self.bg_sound.play(-1)

    def collisions(self):
        for collisions in self.collision_sprites:
            if pygame.sprite.collide_mask(self.plane, collisions) or self.plane.rect.top < 0:
                self.game_over = True

    def display_score(self):
        if not self.game_over:
            self.score = int((pygame.time.get_ticks()-self.start_time) / 1400)
            y = WINDOW_HEIGHT / 6
        else:
            y = self.menu_rect.bottom + 20

        score_surf = self.font.render(f'{self.score}', False, 'black')
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, y))
        if self.score:
            self.display_surface.blit(score_surf, score_rect)

    def restart(self):
        # restart sprites
        self.plane.kill()
        self.plane = Plane()
        self.all_sprites.add(self.plane)
        for sprite in self.collision_sprites.sprites():
            if sprite.sprite_type == 'obstacle':
                sprite.kill()

        self.start_time = pygame.time.get_ticks()
        self.game_over = False

    def run(self):
        last_time = time.time()
        while True:
            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.restart()

                else:
                    # jump
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.plane.jump()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.plane.jump()

                # obstacle
                if event.type == self.obstacle_timer:
                    # noinspection PyTypeChecker
                    Obstacle([self.all_sprites, self.collision_sprites])

            # game logic
            self.all_sprites.draw(self.display_surface)
            self.display_score()
            if self.game_over:
                    self.display_surface.blit(self.menu_surf, self.menu_rect)
            else:
                self.collisions()
                self.all_sprites.update(dt)

            pygame.display.update()
            self.clock.tick(FRAME)


if __name__ == '__main__':
    game = Game()
    game.run()
