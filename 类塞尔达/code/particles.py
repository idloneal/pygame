import pygame
import os
from support import import_folder
from random import  choice

class AnimationParticle:
    def __init__(self):
        self.frames = {}
        total_path = '../graphics/particles/'
        leaf_frames = []
        for file_name in os.listdir(total_path):
            if 'leaf' in file_name and len(file_name) == 5:
                full_path = total_path + file_name
                leaf_frames.append(import_folder(full_path))
                leaf_frames.append(self.flip_images(import_folder(full_path)))
            else:
                if 'flame' == file_name or 'heal' == file_name:
                    full_path = total_path + file_name + '/frames'
                else:
                    full_path = total_path + file_name
                self.frames[file_name] = import_folder(full_path)
        self.frames['leaf'] = leaf_frames

    @staticmethod
    def flip_images(frames):
        new_frames = []
        for frame in frames:
            flip_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flip_frame)

        return new_frames

    def create_grass_particles(self,pos,groups):
        animation_frames = choice(self.frames['leaf'])
        Particle(pos,animation_frames,groups)

    def create_player_particles(self,attack_type,pos,groups):
        animation_frames = self.frames[attack_type]
        Particle(pos,animation_frames,groups)


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super(Particle, self).__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
