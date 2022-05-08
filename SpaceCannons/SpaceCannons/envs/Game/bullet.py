import pygame
import math
import os
import Params_game as C
dir_path = os.path.dirname(os.path.realpath(__file__))
bullet_id_list=[0]

class bullet1(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super(bullet1, self).__init__()
        
       #create bullet
        self.image = pygame.image.load(os.path.join(dir_path,'Game_imgs','blue_bullet_icon.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (23, 57))
        self.image = pygame.transform.rotate(self.image, angle)
        self.mask = pygame.mask.from_surface(self.image)

       # define bullet positions
        self.rect = self.image.get_rect()
        self.center=self.rect.center
        self.vel_x = 0
        self.vel_y = C.bullet_speed
        self.angle = 0

        # Use trigonometry to calculate the velocity.
        self.velocity_x = math.cos(math.radians(-angle)) * self.vel_y
        self.velocity_y = -math.sin(math.radians(-angle)) * self.vel_y
        self.pos = list(pos)

        bull_id=max(bullet_id_list)+1
        self.bullet_id='B1'+str(bull_id)
        bullet_id_list.append(bull_id)

    def update(self,angle,display):
        # display.blit(self.image, self.rect)
        self.pos[1] += self.velocity_x
        self.pos[0] += self.velocity_y
        # Update the position of the rect as well.
        self.rect.center = self.pos
        self.center=self.rect.center
        


class bullet2(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super(bullet2, self).__init__()
       #create bullet
        self.image = pygame.image.load(os.path.join(dir_path,'Game_imgs','blue_bullet_icon.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (23, 57))
        self.image = pygame.transform.rotate(self.image, angle)
        self.mask = pygame.mask.from_surface(self.image)

       # define bullet positions
        self.rect = self.image.get_rect()
        self.vel_x = 0
        self.vel_y = C.bullet_speed
        self.angle = 0

        # Use trigonometry to calculate the velocity.
        self.velocity_x = math.cos(math.radians(-angle)) * self.vel_y
        self.velocity_y = -math.sin(math.radians(-angle)) * self.vel_y
        self.pos = list(pos)

        bull_id=max(bullet_id_list)+1
        self.bullet_id='B2'+str(bull_id)
        bullet_id_list.append(bull_id)

    def update(self,angle,display):

        # display.blit(self.image, self.rect)
        self.pos[1] += self.velocity_x
        self.pos[0] += self.velocity_y
        # Update the position of the rect as well.
        self.rect.center = self.pos
        self.center=self.rect.center
        

