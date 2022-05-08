import pygame
import Params_game as c
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class healthbar(pygame.sprite.Sprite):
    def __init__(self,hp):
        super(healthbar, self).__init__()
        self.max_hp = hp
        self.hp = self.max_hp
        self.original_image = pygame.image.load(os.path.join(dir_path,'Game_imgs','healthbar.png')).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (550, 40))
        self.max_width = self.original_image.get_width()
        self.image = self.original_image
        # self.image = pygame.transform.scale(self.image, (100, 80))

        self.rect = self.image.get_rect()
        self.vel_x = 0
        self.vel_y = 0


    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def decrease_hp(self):

        self.hp -= 1
        try:
            self.image = pygame.transform.scale(self.image, (self.max_width * self.hp // self.max_hp, self.rect.height))
        except ValueError:
            pass
        curr_x = self.rect.x
        curr_y = self.rect.y

        self.rect = self.image.get_rect()
        self.rect.x = curr_x
        self.rect.y = curr_y

