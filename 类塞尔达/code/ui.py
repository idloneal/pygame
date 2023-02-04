import pygame
from settings import *


class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # weapon full image
        self.weapon_graphics = []
        for weapon_index in range(len(WEAPON_DATA.items())):
            weapon = pygame.image.load(list(WEAPON_DATA.values())[weapon_index]['graphics']).convert_alpha()
            self.weapon_graphics.append(weapon)

        # magic full image
        self.magic_graphics = []
        for magic in MAGIC_DATA.values():
            magic = pygame.image.load(magic['graphics']).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_health, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # current bar
        radio = current / max_health
        current_width = bg_rect.width * radio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # draw  bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
        self.display_surface.blit(text_surf, text_rect)

    def selection_box(self, left, top, switch):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if switch:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 2)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def show_weapon(self, weapon_index, switch):
        bg_rect = self.selection_box(10, 600, switch)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def show_magic(self, magic_index, switch):
        bg_rect = self.selection_box(95, 630, switch)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.attribute['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.attribute['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)
        self.show_weapon(player.weapon_index, not player.switch_weapon)
        self.show_magic(player.magic_index, not player.can_switch_magic)
