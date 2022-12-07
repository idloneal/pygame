import random
import pygame
import sys


class ParticlePrinciple():
    def __init__(self):
        self.particles = []

    def emit(self):  # 移动并创建粒子
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]  # 移动
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2  # 缩小他的半径
                pygame.draw.circle(screen,pygame.Color('White'),particle[0], int(particle[1]))

    def add_particles(self):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1]
        radius = 10
        direction_x = random.randint(-3,3)
        direction_y = random.randint(-3,3)
        particle_circle = [[pos_x,pos_y],radius,[direction_x,direction_y]]  # 给他们一些属性
        self.particles.append(particle_circle)

    def delete_particles(self):
        # 删除半径小于0的圆
        particle_copy = [particle for particle in self.particles if particle[1]>0]  # 三目运算
        self.particles = particle_copy



pygame.init()
bg_size = (800,800)
screen = pygame.display.set_mode(bg_size)
clock = pygame.time.Clock()

particle1 = ParticlePrinciple()

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT,150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == PARTICLE_EVENT:
            particle1.add_particles()
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_RIGHT:

        #     if event.key == pygame.K_LEFT:

    screen.fill((30, 30, 30))
    particle1.emit()
    pygame.display.update()
    clock.tick(60)