import pygame
from decoration import Sky
from map_data import levels
from support import import_folder


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_movement_speed, path):
        super(Node, self).__init__()
        self.frames = import_folder(path)
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center=pos)

        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_movement_speed / 2),
                                          self.rect.centery - (icon_movement_speed / 2),
                                          icon_movement_speed, icon_movement_speed)

    def animate(self):
        self.frames_index += 0.15
        if self.frames_index >= len(self.frames):
            self.frames_index = 0
        self.image = self.frames[int(self.frames_index)]

    def static_animate(self):
        tint_surf = self.image.copy()
        tint_surf.fill('black', None, pygame.BLEND_RGB_MULT)
        self.image.blit(tint_surf, (0, 0))

    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            # self.animate()  # 是否让未解锁的关卡动起来
            self.static_animate()


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Icon, self).__init__()
        self.pos = pos
        self.image = pygame.image.load('../graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos


class Overworld:
    def __init__(self, start_level, max_level, surface, create_level):

        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # icon movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.icon_movement_speed = 8

        # sprites
        self.nodes = pygame.sprite.Group()
        self.setup_nodes()
        self.icon = pygame.sprite.GroupSingle()
        self.setup_icon()
        self.sky = Sky(8, 'overworld')

    def setup_nodes(self):

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.icon_movement_speed,
                                   node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.icon_movement_speed,
                                   node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def draw_paths(self):
        if self.max_level:
            points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, (196, 145, 109), False, points, 6)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if self.current_level < self.max_level:
                    self.moving = True
                    self.move_direction = self.get_movement_data('next')
                    self.current_level += 1
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if self.current_level > 0:
                    self.moving = True
                    self.move_direction = self.get_movement_data('previous')
                    self.current_level -= 1
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()  # 归一化

    def setup_icon(self):
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def update_icon_pos(self):
        if self.moving:
            self.icon.sprite.pos += self.move_direction * self.icon_movement_speed
            target_node = self.nodes.sprites()[self.current_level]

            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def run(self):
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()

        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
