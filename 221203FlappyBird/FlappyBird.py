import os
import sys
import pygame
import random

import pygame.examples.glcube

bg_size = (288, 512)
FPS = 30

pygame.init()
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

IMAGES = {}
for image in os.listdir('sprites'):
    name, extension = os.path.splitext(image)
    path = os.path.join('sprites', image)
    IMAGES[name] = pygame.image.load(path)

FLOOR_Y = bg_size[1] - IMAGES['floor'].get_height()

AUDIO = {}
for audio in os.listdir('audio'):
    name, extension = os.path.splitext(audio)
    path = os.path.join('audio', audio)
    AUDIO[name] = pygame.mixer.Sound(path)


def menu_window():
    guide_x = (bg_size[0] - IMAGES['guide'].get_width()) / 2
    guide_y = (FLOOR_Y - IMAGES['guide'].get_height()) / 2
    bird_x = bg_size[0] * 0.2
    bird_y = (bg_size[1] - IMAGES['birds'][0].get_height()) / 2
    floor_x = 0
    floor_gap = IMAGES['floor'].get_width() - bg_size[0]

    bird_y_vel = 1
    bird_y_range = [bird_y - 8, bird_y + 8]

    idx = 0
    frames = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        floor_x -= 4
        if floor_x <= -floor_gap:
            floor_x = 0

        bird_y += bird_y_vel
        if bird_y < bird_y_range[0] or bird_y > bird_y_range[1]:
            bird_y_vel *= -1

        idx += 1
        idx %= len(frames)

        screen.blit(IMAGES['bgpic'], (0, 0))
        screen.blit(IMAGES['floor'], (floor_x, FLOOR_Y))
        screen.blit(IMAGES['guide'], (guide_x, guide_y))
        screen.blit(IMAGES['birds'][frames[idx]], (bird_x, bird_y))
        pygame.display.update()
        clock.tick(FPS)


def game_window():
    AUDIO['flap'].play()

    floor_x = 0
    floor_gap = IMAGES['floor'].get_width() - bg_size[0]

    bird = Bird(bg_size[0] * 0.2, bg_size[1] * 0.4)

    distance = 150
    n = 4
    pipes = []
    for i in range(n):
        pipe_y = random.randint(int(bg_size[1]*0.2), int(bg_size[1]*0.8))
        pipe = Pipe(bg_size[0] + i*distance, pipe_y)
        pipes.append(pipe)

    while True:
        flap = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                flap = True
                AUDIO['flap'].play()

        floor_x -= 4
        if floor_x <= -floor_gap:
            floor_x = 0

        bird.update(flap)

        first_pipe = pipes[0]
        if first_pipe.rect.right < 0:
            pipes.remove(first_pipe)
            pipe_y = random.randint(int(bg_size[1] * 0.2), int(bg_size[1] * 0.8))
            new_pipe = Pipe(first_pipe.rect.x + n * distance, pipe_y)
            pipes.append(new_pipe)
            del first_pipe

        for pipe in pipes:
            pipe.update()

        if bird.rect.y > FLOOR_Y or bird.rect.y < 0:
            AUDIO['hit'].play()
            AUDIO['die'].play()
            result = {'bird': bird}
            return result

        screen.blit(IMAGES['bgpic'], (0, 0))
        for pipe in pipes:
            screen.blit(pipe.image, pipe.rect)
        screen.blit(IMAGES['floor'], (floor_x, FLOOR_Y))
        screen.blit(bird.image, bird.rect)
        pygame.display.update()
        clock.tick(FPS)


def end_window(result):
    game_over_x = (bg_size[0] - IMAGES['game-over'].get_width()) / 2
    game_over_y = (FLOOR_Y - IMAGES['game-over'].get_height()) / 2

    bird = result['bird']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        bird.go_die()

        screen.blit(IMAGES['bgpic'], (0, 0))
        screen.blit(IMAGES['floor'], (0, FLOOR_Y))
        screen.blit(IMAGES['game-over'], (game_over_x, game_over_y))
        screen.blit(bird.image, bird.rect)
        pygame.display.update()
        clock.tick(FPS)


def main():
    AUDIO['start'].play()
    IMAGES['bgpic'] = IMAGES[random.choice(['day', 'night'])]
    color = random.choice(['red', 'blue', 'yellow'])
    IMAGES['birds'] = [IMAGES[color + '-up'], IMAGES[color + '-mid'], IMAGES[color + '-down']]
    pipe = IMAGES[random.choice(['green-pipe', 'red-pipe'])]
    IMAGES['pipes'] = [pipe, pygame.transform.flip(pipe, True, False)]
    menu_window()
    result = game_window()
    end_window(result)


class Bird:
    def __init__(self, x, y):
        # 小鸟煽动翅膀规律
        self.frames = [0] * 5 + [1] * 5 + [2] * 5 + [1] * 5
        self.idx = 0
        self.images = IMAGES['birds']
        self.image = IMAGES['birds'][self.frames[self.idx]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # 初始向上速度
        self.y_vel = -10
        # 最大向下速度
        self.max_y_vel = 10
        # 每次变化速度
        self.gravity = 1
        # 初始角度
        self.rotate = 45
        # 最低角度
        self.max_rotate = -20
        # 每次改变角度
        self.rotate_vel = -3
        # 默认向上速度
        self.y_vel_after_flap = -10
        # 默认角度
        self.rotate_after_flap = 45

    def update(self, flap=False):

        if flap:
            self.y_vel = self.y_vel_after_flap
            self.rotate = self.rotate_after_flap

        self.y_vel = min(self.y_vel + self.gravity, self.max_y_vel)
        self.rect.y += self.y_vel
        self.rotate = max(self.rotate + self.rotate_vel, self.max_rotate)

        self.idx += 1
        self.idx %= len(self.frames)
        self.image = self.images[self.frames[self.idx]]
        self.image = pygame.transform.rotate(self.image, self.rotate)

    def go_die(self):
        if self.rect.y < FLOOR_Y:
            self.rect.y += self.max_y_vel
            self.rotate = -90
            self.image = self.images[self.frames[self.idx]]
            self.image = pygame.transform.rotate(self.image, self.rotate)


class Pipe:
    def __init__(self, x, y, upwards=True):
        if upwards:
            self.image = IMAGES['pipes'][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = y
        else:
            self.image = IMAGES['pipes'][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y
        self.x_vel = -4

    def update(self):
        self.rect.x += self.x_vel


if __name__ == '__main__':
    main()
