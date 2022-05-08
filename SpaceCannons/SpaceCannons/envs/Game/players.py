from numpy.lib.type_check import imag
import pygame
import Params_game as C
from Game.bullet import bullet1
from Game.bullet import bullet2
from Game.hud import HUD
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

SHOT_DELAY = 100



class Gameplayer1(pygame.sprite.Sprite):

    def __init__(self):
        super(Gameplayer1, self).__init__()
        self.image = pygame.image.load(os.path.join(dir_path,'Game_imgs','player2.2.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 1100))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = C.P1_pos_x
        self.rect.y = C.P1_pos_y
        self.angle = 0


        # Bullet
        self.bullets_P1 = pygame.sprite.Group()
        self.bullet_lifetime = pygame.time.get_ticks() + 2000


        self.max_hp = C.PLAYER_HEALTH
        self.health = self.max_hp
        ##  HUD
        self.hud = HUD(self.health)
        self.hud_group = pygame.sprite.Group()
        self.hud_group.add(self.hud)
        self.last_shot1=0


    def update(self,display):
        rend=True
        

        #hud UPDATE
        self.hud_group.update()

        imagex = pygame.transform.rotozoom(self.image, self.angle,1)
        self.rect = imagex.get_rect(center=self.rect.center)
        if rend == True:
            display.blit(imagex, self.rect)
            
        self.bullets_P1.update(self.angle,display)


    def shoot(self,angle,display):

        new_bullet = bullet1(self.rect.center, self.angle)
        new_bullet.rect.x = self.rect.x + (self.rect.width //2 -1)
        new_bullet.rect.y = self.rect.y
        self.bullets_P1.add(new_bullet)
        self.bullets_P1.update(self.angle,display)


    def get_hit(self):
        self.health -=1
        self.hud.healthbar.decrease_hp()



class Gameplayer2(pygame.sprite.Sprite):

    def __init__(self):
        super(Gameplayer2, self).__init__()
        self.image = pygame.image.load(os.path.join(dir_path,'Game_imgs','player2.2.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60,1100))
        self.rect = self.image.get_rect()
        self.rect.x = C.P2_pos_x
        self.rect.y = C.P2_pos_y
        self.angle = 0
        self.health = C.PLAYER_HEALTH
        self.last_shot2=0
         #bullet
        self.bullets_P2 = pygame.sprite.Group()


    def update(self,display):
        rend=True
        now = pygame.time.get_ticks()
        imagex = pygame.transform.rotozoom(self.image, self.angle,1)
        self.rect = imagex.get_rect(center=self.rect.center)
        if rend==True:
            display.blit(imagex, self.rect)
        self.bullets_P2.update(self.angle,display)
    def shoot(self,angle,display):

        new_bullet = bullet2(self.rect.center, self.angle)
        new_bullet.rect.x = self.rect.x + (self.rect.width //2 -1)
        new_bullet.rect.y = self.rect.y

        self.bullets_P2.add(new_bullet)
        self.bullets_P2.update(self.angle,display)

    def get_hit(self, enemy_type):
        self.health -= 1
