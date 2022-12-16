import sys
import pygame
import random
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            pos_x = int(block.x * cell_size)
            pos_y = int(block.y * cell_size)
            block_rect = pygame.Rect(pos_x, pos_y, cell_size, cell_size)
            pygame.draw.rect(screen, (133, 111, 122), block_rect)

    def move_snake(self):
        if not self.new_block:
            self.body.pop(-1)  # 删除最后一个元素
        self.body.insert(0, self.body[0] + self.direction)
        self.new_block = False

    def add_block(self):
        self.new_block = True


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
        for block in snake.body:
            if block == self.pos:
                self.randomize(snake)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize(self.snake)
            self.snake.add_block()

    def check_fail(self):
        # 检查是否碰到墙壁
        if not 0 <= self.snake.body[0].x <= cell_number - 1 or \
                not 0 <= self.snake.body[0].y <= cell_number - 1:
            self.game_over()

        # 检查是否和身体碰撞
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        print(len(self.snake.body))

def changeDricetion(change_direction):
    global direction
    # 判断和上次行动时反向是否相反
    if change_direction == 'UP' and direction != 'DOWN':
        direction = change_direction
    if change_direction == 'DOWN' and direction != 'UP':
        direction = change_direction
    if change_direction == 'LEFT' and direction != 'RIGHT':
        direction = change_direction
    if change_direction == 'RIGHT' and direction != 'LEFT':
        direction = change_direction


    if direction == 'UP':
        main_game.snake.direction = Vector2(0, -1)
    if direction == 'DOWN':
        main_game.snake.direction = Vector2(0, 1)
    if direction == 'RIGHT':
        main_game.snake.direction = Vector2(1, 0)
    if direction == 'LEFT':
        main_game.snake.direction = Vector2(-1, 0)


pygame.init()
cell_size = 40
cell_number = 20
bg_size = (cell_size * cell_number, cell_size * cell_number)
screen = pygame.display.set_mode(bg_size)
clock = pygame.time.Clock()

level = 1
snake_speed = int(1000 / (level+2))

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, snake_speed)  # 移动速度

direction = 'RIGHT'
change_direction = 'RIGHT'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.type == pygame.K_w:
                change_direction = 'UP'
            if event.key == pygame.K_DOWN or event.type == pygame.K_s:
                change_direction = 'DOWN'
            if event.key == pygame.K_LEFT or event.type == pygame.K_a:
                change_direction = 'LEFT'
            if event.key == pygame.K_RIGHT or event.type == pygame.K_d:
                change_direction = 'RIGHT'
        if event.type == SCREEN_UPDATE:
            changeDricetion(change_direction)
            main_game.update()


    screen.fill(pygame.Color(175, 215, 75))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
