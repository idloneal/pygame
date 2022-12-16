import random
import pygame
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(50, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300 or click[0] and self.rect.bottom == 300:
            self.gravity = -10

    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.bottom += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0

    def animation_state(self):
        if self.rect.bottom == 300:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
        else:
            self.image = self.player_jump

    def update(self):
        self.animation_state()
        self.player_input()
        self.apply_gravity()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_frame2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= ground_speed + 2
        self.destroy()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render('score:%d' % current_time, False, (64, 64, 64))
    score_rect = score_surf.get_rect(midtop=sky_surf.get_rect().midtop)
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group,False):  # 检查精灵与精灵组是否碰撞 碰撞后是否删除
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
pygame.display.set_caption('Runner')  # 标题
clock = pygame.time.Clock()
bg_size = (800, 468)
screen = pygame.display.set_mode(bg_size)
# 一些属性
ground_speed = 5
player_gravity = 0
player_jump_num = 0
game_active = False
score = 0
start_time = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# background image
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
sky_surf = pygame.image.load('graphics/Sky.png').convert_alpha()
sky_rect = sky_surf.get_rect()
sky_rect2 = sky_surf.get_rect(left=sky_rect.right)
ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
ground_rect = ground_surf.get_rect(top=sky_surf.get_rect().bottom)

obstacle_rect_list = []

# 简介画面
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_scaled = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand_scaled.get_rect(center=(400, 234))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))
game_over_surf = test_font.render('Press Space to run', False, (111, 196, 169))
game_over_rect = game_over_surf.get_rect(center=(400, 400))

# event
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == pygame.KEYDOWN:  # 按下空格跳跃
                if event.key == pygame.K_SPACE:
                    if not player_jump_num == 2:
                        player_gravity = -10
                        player_jump_num += 1
            if event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标点击跳跃
                if player_jump_num <= 2:
                    player_gravity = -10
                    player_jump_num += 1
            if event.type == obstacle_timer:  # 随机添加 障碍
                obstacle_group.add(Obstacle(random.choice(['fly', 'snail', 'snail'])))

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over_rect.collidepoint(pygame.mouse.get_pos()):
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # Ground
        sky_rect.left -= 1
        sky_rect2 = sky_surf.get_rect(left=sky_rect.right)
        if sky_rect.right <= 0:
            sky_rect.right = 800
        screen.blit(sky_surf, sky_rect)
        screen.blit(sky_surf, sky_rect2)
        ground_rect.left -= ground_speed
        ground_rect2 = ground_surf.get_rect(left=ground_rect.right, top=sky_surf.get_rect().bottom)
        if ground_rect.right <= 0:
            ground_rect.right = 800
        screen.blit(ground_surf, ground_rect)
        screen.blit(ground_surf, ground_rect2)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # 碰撞检测
        game_active = collision_sprite()

        # score
        score = display_score()
        ground_speed = score // 2 + 5

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_scaled, player_stand_rect)
        obstacle_rect_list.clear()

        score_message = test_font.render(f"Your score:{score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 350))
        screen.blit(game_name, game_name_rect)
        screen.blit(game_over_surf, game_over_rect)
        if score:
            screen.blit(score_message, score_message_rect)
        if game_over_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, '#c0e8ec', game_over_rect, False, 10)
            screen.blit(game_over_surf, game_over_rect)
    pygame.display.update()
    clock.tick(60)
