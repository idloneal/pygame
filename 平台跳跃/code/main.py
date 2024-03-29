import pygame
import sys
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):
        # game attributes
        self.max_level = 3
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        # audio
        self.level_bg_music = pygame.mixer.Sound('../audio/level_music.wav')
        self.level_bg_music.set_volume(0.35)
        self.overworld_bg_music = pygame.mixer.Sound('../audio/overworld_music.wav')
        self.overworld_bg_music.set_volume(0.25)

        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(-1)

        # user interface
        self.ui = UI(screen)

        # game level
        self.level = None

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        # play audio
        self.overworld_bg_music.stop()
        self.level_bg_music.play(-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        # play audio
        self.level_bg_music.stop()
        self.overworld_bg_music.play(-1)

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.cur_health += amount

    def check_death(self):
        # init attributes
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = 0
            self.max_level = 0
            # init map
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            # init audio
            self.level_bg_music.stop()
            self.overworld_bg_music.play(-1)

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_death()


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(60)
