import pygame
import sys
import random


def ball_animation():
    global ball_speed_y, ball_speed_x, player_score, opponent_score, score_time
    # 球速
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # 什么时候翻转
    if ball.top <= 0 or ball.bottom >= bg_size[1]:
        ball_speed_y *= -1

    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= bg_size[0]:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= bg_size[1]:
        player.bottom = bg_size[1]


def opponent_animation():
    if opponent.top + 50 < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom - 50 > ball.y:
        opponent.top -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= bg_size[1]:
        opponent.bottom = bg_size[1]


# noinspection PyTypeChecker
def ball_restart():
    global ball_speed_y, ball_speed_x, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (bg_size[0] / 2, bg_size[1]/2)

    if current_time - score_time < 700:
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three, (bg_size[0]/2 - 10, bg_size[1]/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, light_grey)
        screen.blit(number_two, (bg_size[0]/2 - 10, bg_size[1]/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, light_grey)
        screen.blit(number_one, (bg_size[0]/2 - 10, bg_size[1]/2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        score_time = None

    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= -1


pygame.init()
clock = pygame.time.Clock()

bg_size = (1280, 960)

screen = pygame.display.set_mode(bg_size)

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

ball = pygame.Rect(bg_size[0] / 2 - 15, bg_size[1] / 2 - 15, 30, 30)
player = pygame.Rect(bg_size[0] - 20, bg_size[1] / 2 - 70, 10, 140)
opponent = pygame.Rect(10, bg_size[1] / 2 - 70, 10, 140)

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 10

# Text Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# Score Timer
score_time = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 10
            if event.key == pygame.K_UP:
                player_speed -= 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 10
            if event.key == pygame.K_UP:
                player_speed += 10

    ball_animation()
    player_animation()
    opponent_animation()

    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (bg_size[0] / 2, 0), (bg_size[0] / 2, bg_size[1]))

    if score_time:
        ball_restart()

    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (660, 470))

    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (600, 470))

    pygame.display.flip()
    clock.tick(60)
