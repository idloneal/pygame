import pygame
import sys


class ParticlePrinciple():
    def __init__(self):
        self.particles = []

    def particles(self):  # 移动并创建粒子
        pass

    def add_particles(self):
        pos_x = bg_size[0]/2
        pos_y = bg_size[1]/2

    def delete_particles(self):
        pass



pygame.init()
bg_size = (800,800)
screen = pygame.display.set_mode(bg_size)
clock = pygame.time.Clock()

particle1 = ParticlePrinciple()

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT,40)

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
    pygame.display.update()
    clock.tick(60)