import os
import sys
import pygame
import random
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.tail = 'tail_right'

        # 增加可读性
        self.up = Vector2(0, -1)
        self.down = Vector2(0, 1)
        self.left = Vector2(-1, 0)
        self.right = Vector2(1, 0)

        # 导入图片
        self.IMAGES = {}
        for image in os.listdir('Graphics'):
            name, extension = os.path.splitext(image)
            path = os.path.join('Graphics', image)
            self.IMAGES[name] = pygame.image.load(path).convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            pos_x = int(block.x * cell_size)
            pos_y = int(block.y * cell_size)
            block_rect = pygame.Rect(pos_x, pos_y, cell_size, cell_size)

            # 蛇的图片加载
            if index == 0:  # 蛇头根据下次行进反向改变
                if self.direction == self.up:
                    screen.blit(self.IMAGES['head_up'], block_rect)
                if self.direction == self.down:
                    screen.blit(self.IMAGES['head_down'], block_rect)
                if self.direction == self.left:
                    screen.blit(self.IMAGES['head_left'], block_rect)
                if self.direction == self.right:
                    screen.blit(self.IMAGES['head_right'], block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.IMAGES[self.tail], block_rect)
            else:
                previous_block = self.body[index - 1] - block
                next_block = block - self.body[index + 1]
                bodies = 'body_horizontal'
                if next_block == self.up and previous_block == self.left or \
                        next_block == self.right and previous_block == self.down:
                    bodies = 'body_bl'
                if next_block == self.up and previous_block == self.right or \
                        next_block == self.left and previous_block == self.down:
                    bodies = 'body_br'
                if next_block == self.left and previous_block == self.right or \
                        next_block == self.right and previous_block == self.left:
                    bodies = 'body_horizontal'
                if next_block == self.up and previous_block == self.up or \
                        next_block == self.down and previous_block == self.down:
                    bodies = 'body_vertical'
                if next_block == self.right and previous_block == self.up or \
                        next_block == self.down and previous_block == self.left:
                    bodies = 'body_tl'
                if next_block == self.down and previous_block == self.right or \
                        next_block == self.left and previous_block == self.up:
                    bodies = 'body_tr'
                screen.blit(self.IMAGES[bodies], block_rect)

    def update_tail_graphics(self):
        temp = self.body[-2] - self.body[-1]
        if temp == self.up:
            self.tail = 'tail_up'
        if temp == self.down:
            self.tail = 'tail_down'
        if temp == self.left:
            self.tail = 'tail_left'
        if temp == self.right:
            self.tail = 'tail_right'

    def move_snake(self):
        if not self.new_block:
            self.body.pop(-1)  # 删除最后一个元素
        self.body.insert(0, self.body[0] + self.direction)
        self.new_block = False

    def add_block(self):
        self.new_block = True
        self.crunch_sound.play()

    def reset(self):
        global direction, change_direction
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        direction = 'RIGHT'
        change_direction = 'RIGHT'


class FRUIT:
    def __init__(self):
        self.image = pygame.image.load('Graphics/apple.png').convert_alpha()
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)  # 创造向量

    def draw_fruit(self):
        rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(self.image, rect)

    def randomize(self, snake):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        # 禁止水果出现在身体的位置
        for block in snake.body[1:]:
            if block == self.pos:
                self.randomize(snake)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize(self.snake)
            self.snake.add_block()

    def check_fail(self):
        # 检查是否碰到墙壁
        if not 0 <= self.snake.body[0].x <= cell_number - 1 or \
                not 0 <= self.snake.body[0].y <= cell_number - 1:
            return False

        # 检查是否和身体碰撞
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                return False
            else:
                return True

    def game_over(self):
        score = len(self.snake.body) - 3
        game_over_surf = game_font.render('Press SPACE begin game', True, (56, 74, 12))
        game_over_rect = game_over_surf.get_rect(center=(400, 400))
        if score:
            score_surf = game_font.render('you score:%d' % score, True, (56, 74, 12))
            score_rect = score_surf.get_rect(center=(400, 300))
            screen.blit(score_surf, score_rect)
            game_over_surf = game_font.render('Press SPACE restart game', True, (56, 74, 12))
            game_over_rect = game_over_surf.get_rect(center=(400, 450))
        screen.blit(game_over_surf, game_over_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surf = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number) - 40
        score_y = int(cell_size * cell_number) - 40
        screen_rect = score_surf.get_rect(center=(score_x, score_y))
        apple_rect = self.fruit.image.get_rect(midright=(screen_rect.left, screen_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                              apple_rect.w + screen_rect.w + 10, apple_rect.h)

        pygame.draw.rect(screen, 'black', bg_rect, 2)
        screen.blit(self.fruit.image, apple_rect)
        screen.blit(score_surf, screen_rect)

    def update(self):
        self.snake.move_snake()
        self.check_collision()


def re_direction(temp_direction):
    global direction
    # 判断和上次行动时反向是否相反
    if temp_direction == 'UP' and direction != 'DOWN':
        direction = temp_direction
    if temp_direction == 'DOWN' and direction != 'UP':
        direction = temp_direction
    if temp_direction == 'LEFT' and direction != 'RIGHT':
        direction = temp_direction
    if temp_direction == 'RIGHT' and direction != 'LEFT':
        direction = temp_direction

    if direction == 'UP':
        main_game.snake.direction = Vector2(0, -1)
    if direction == 'DOWN':
        main_game.snake.direction = Vector2(0, 1)
    if direction == 'RIGHT':
        main_game.snake.direction = Vector2(1, 0)
    if direction == 'LEFT':
        main_game.snake.direction = Vector2(-1, 0)


def draw_grass():
    grass_color = (167, 209, 61)

    for col_x in range(0, cell_number, 2):
        for col_y in range(0, cell_number, 2):
            grass_rect = pygame.Rect(col_x * cell_size, col_y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, grass_color, grass_rect)
    for col_x in range(1, cell_number, 2):
        for col_y in range(1, cell_number, 2):
            grass_rect = pygame.Rect(col_x * cell_size, col_y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, grass_color, grass_rect)


pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
cell_size = 40
cell_number = 20
bg_size = (cell_size * cell_number, cell_size * cell_number)
screen = pygame.display.set_mode(bg_size)
clock = pygame.time.Clock()

game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

game_active = False

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, int(1000 / 13))  # 移动速度

direction = 'RIGHT'
change_direction = 'RIGHT'

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    change_direction = 'UP'
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    change_direction = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    change_direction = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    change_direction = 'RIGHT'
            if event.type == SCREEN_UPDATE:
                re_direction(change_direction)
                main_game.update()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    main_game.snake.reset()
    screen.fill(pygame.Color(175, 215, 75))
    draw_grass()
    if game_active:
        main_game.draw_elements()
        game_active = main_game.check_fail()
    else:
        main_game.game_over()
    pygame.display.update()
    clock.tick(60)
