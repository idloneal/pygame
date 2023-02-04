import pygame
from settings import *


class Upgrade:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.attribute)
        self.attribute_name = list(player.attribute.keys())
        self.max_values = list(player.max_attribute.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # setup size
        self.height = self.display_surface.get_height() * 0.8
        self.width = self.display_surface.get_width() // 6
        self.item_list = []
        self.create_items()

        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.selection_time_cooldown = 300
        self.can_selection = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_selection:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_number - 1:
                self.selection_index += 1
                self.can_selection = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_selection = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_selection = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        if not self.can_selection:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= self.selection_time_cooldown:
                self.can_selection = True

    def create_items(self):
        for index in (range(self.attribute_number)):
            box_width = SCREEN_WIDTH // self.attribute_number
            left = index * box_width + (box_width - self.width) / 2

            top = (SCREEN_HEIGHT - self.height) / 2
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            # get attribute
            name = self.attribute_name[index]
            # value = list(self.player.attribute.values())[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)


class Item:
    def __init__(self, left, top, w, h, index, font):
        self.rect = pygame.Rect(left, top, w, h)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        # 当选择在这个框的时候改变颜色
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))

        # cost
        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20))

        # draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value):
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR
        current_color = BAR_COLOR_SELECTED
        bar_width = 40

        # level bar
        full_height = bottom[1] - top[1]
        relative_height = (value / max_value) * full_height
        offset_top = bottom - pygame.math.Vector2(0, relative_height)

        pygame.draw.line(surface, color, top, bottom, bar_width)
        pygame.draw.line(surface, current_color, offset_top, bottom, bar_width)

    def trigger(self, player):
        attribute_name = list(player.attribute.keys())[self.index]
        need_cost = player.upgrade_cost[attribute_name]

        if player.exp >= need_cost and player.attribute[attribute_name] < player.max_attribute[attribute_name]:
            player.exp -= need_cost
            if attribute_name == 'move_speed':
                player.attribute[attribute_name] += 0.5
            else:
                player.attribute[attribute_name] *= 1.2
            player.upgrade_cost[attribute_name] *= 1.4

        if player.attribute[attribute_name] > player.max_attribute[attribute_name]:
            player.attribute[attribute_name] = player.max_attribute[attribute_name]

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        self.display_names(surface, name, cost, selection_num == self.index)
        self.display_bar(surface, value, max_value)
