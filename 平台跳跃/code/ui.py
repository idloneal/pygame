import pygame


class UI:
    def __init__(self, surface):
        # setup
        self.display_surface = surface

        # health
        self.health = pygame.image.load('../graphics/ui/health_bar.png')
        health_topleft = (20, 10)
        self.health_rect = self.health.get_rect(topleft=health_topleft)
        self.health_bar_topleft = (health_topleft[0] + 34, health_topleft[1] + 29)
        self.health_bar_max_width = 152
        self.health_bar_height = 4

        # coins
        self.coin = pygame.image.load('../graphics/ui/coin.png')
        coin_pos = (self.health_rect.left + 40, self.health_rect.bottom - 10)
        self.coin_rect = self.coin.get_rect(topleft=coin_pos)

        # font
        self.font = pygame.font.Font('../graphics/ui/ARCADEPI.TTF', 30)

    def show_health(self, current, full):
        self.display_surface.blit(self.health, self.health_rect)
        current_health_ratio = current / full
        current_bar_width = self.health_bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (current_bar_width, self.health_bar_height))
        pygame.draw.rect(self.display_surface,'#dc4949',health_bar_rect)

    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surf = self.font.render(str(amount), False, '#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)
