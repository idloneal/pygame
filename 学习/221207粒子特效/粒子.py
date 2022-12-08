import random
import pygame
import sys


class ParticlePrinciple:
    def __init__(self):
        self.particles = []

    def emit(self):  # 移动并创建粒子
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]  # 移动
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2  # 缩小他的半径
                pygame.draw.circle(screen, pygame.Color('White'), particle[0], int(particle[1]))

    def add_particles(self):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1]
        radius = 10
        direction_x = random.randint(-3, 3)
        direction_y = random.randint(-3, 3)
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]  # 给他们一些属性
        self.particles.append(particle_circle)

    def delete_particles(self):
        # 删除半径小于0的圆
        particle_copy = [particle for particle in self.particles if particle[1] > 0]  # 三目运算
        self.particles = particle_copy


class ParticleNyan:
    def __init__(self):
        self.particles = []
        self.size = 8
        self.nyna_cat = nyan_surface_image.get_rect(center=pygame.mouse.get_pos())

    def emit(self):  # 移动并创建粒子
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0].x -= 2
                pygame.draw.rect(screen, particle[1], particle[0])

        self.draw_nyancat()

    def add_particles(self, offset, particles_color):
        pos_x = self.nyna_cat.left
        pos_y = pygame.mouse.get_pos()[1] + offset
        particle_rect = pygame.Rect(int(pos_x - self.size / 2), int(pos_y - self.size / 2), self.size, self.size)
        self.particles.append((particle_rect, particles_color))

    def delete_particles(self):
        # 删除半径小于0的圆
        particle_copy = [particle for particle in self.particles if particle[0].x > 0]  # 三目运算
        self.particles = particle_copy

    def draw_nyancat(self):
        self.nyna_cat = nyan_surface_image.get_rect(center=pygame.mouse.get_pos())
        screen.blit(nyan_surface_image, self.nyna_cat)


class ParticleStar:
    def __init__(self):
        self.particles = []
        self.surface = pygame.image.load("star.png").convert_alpha()
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    def emit(self):  # 移动并创建粒子
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0].x += particle[1]  # 移动
                particle[0].y += particle[2]
                particle[3] -= 0.2  # 缩小他的半径
                screen.blit(self.surface, particle[0])

    def add_particles(self):
        pos_x = pygame.mouse.get_pos()[0] - self.width / 2
        pos_y = pygame.mouse.get_pos()[1] - self.height / 2
        direction_x = random.randint(-3, 3)
        direction_y = random.randint(-3, 3)
        lifetime = random.randint(4, 10)
        particle_rect = pygame.Rect(pos_x, pos_y, self.width, self.height)
        self.particles.append([particle_rect, direction_x, direction_y, lifetime])

    def delete_particles(self):
        # 删除半径小于0的圆
        particle_copy = [particle for particle in self.particles if particle[3] > 0]  # 三目运算
        self.particles = particle_copy


class NyanStar:
    def __init__(self):
        self.particles = []

    def emit(self):  # 移动并创建粒子
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]  # 移动
                particle[0][0] += particle[2][1]
                particle[1] -= 0.3  # 缩小他的半径
                particles_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                pygame.draw.circle(screen, pygame.Color(particles_color), particle[0], int(particle[1]))

    def add_particles(self):
        star_range = (random.randint(-300, 300), random.randint(-150, 150))  # 星星生成的范围
        pos_x = pygame.mouse.get_pos()[0] + star_range[0]
        pos_y = pygame.mouse.get_pos()[1] + star_range[1]
        radius = 6
        direction_x = random.randint(-3, 3)
        direction_y = random.randint(-3, 3)
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]  # 给他们一些属性
        self.particles.append(particle_circle)
        particle_circle = [[pos_x, pos_y], radius, [-direction_x, -direction_y]]
        self.particles.append(particle_circle)
        particle_circle = [[pos_x, pos_y], radius, [-direction_x, direction_y]]  # 给他们一些属性
        self.particles.append(particle_circle)
        particle_circle = [[pos_x, pos_y], radius, [direction_x, -direction_y]]
        self.particles.append(particle_circle)

    def delete_particles(self):
        # 删除半径小于0的圆
        particle_copy = [particle for particle in self.particles if particle[1] > 0]  # 三目运算
        self.particles = particle_copy


pygame.mixer.init()  # 音乐模块初始化
sound = pygame.mixer.Sound('Nyan_Cat_loop.wav')
sound.set_volume(0.2)
sound.play(-1)

pygame.init()
bg_size = (1800, 800)
screen = pygame.display.set_mode(bg_size)
clock = pygame.time.Clock()

nyan_surface_image = pygame.image.load('nyan_cat.png').convert_alpha()
nyan_surface_image = pygame.transform.scale(nyan_surface_image,
                                            (nyan_surface_image.get_width() / 9.5 * 2,
                                             nyan_surface_image.get_height() / 9.5 * 2))

particle1 = ParticlePrinciple()
particle2 = ParticleNyan()
particle3 = ParticleStar()
nyan_star = NyanStar()

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 1)

PARTICLE_STAR_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(PARTICLE_STAR_EVENT, 20)

screen_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(screen_EVENT, 2000)

color = (30, 30, 30)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == PARTICLE_EVENT:
            # particle1.add_particles()
            particle2.add_particles(-19, pygame.Color(255, 1, 1))
            particle2.add_particles(-11, pygame.Color(252, 156, 0))
            particle2.add_particles(-3, pygame.Color(255, 255, 0))
            particle2.add_particles(5, pygame.Color(50, 255, 0))
            particle2.add_particles(13, pygame.Color(0, 152, 255))
            particle2.add_particles(21, pygame.Color(103, 52, 255))
            # particle3.add_particles()
        if event.type == PARTICLE_STAR_EVENT:
            nyan_star.add_particles()
        if event.type == screen_EVENT:
            color = (random.randint(0, 125), random.randint(0, 128), random.randint(0, 127))

    screen.fill(color)
    particle1.emit()
    particle2.emit()
    particle3.emit()
    nyan_star.emit()
    pygame.display.update()
    clock.tick(144)
