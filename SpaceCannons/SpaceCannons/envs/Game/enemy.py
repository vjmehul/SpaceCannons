import pygame
import Params_game as c
import random
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
eny_id_list=[0]
import numpy as np
import pandas as pd
i=0



class Enemy(pygame.sprite.Sprite):
    def __init__(self,difficulty_weights):
        super(Enemy, self).__init__()

        enemylist = ['dragon3.png','miniboss.png','big_boss.png']
        self.weights = difficulty_weights
        enemy_name = random.choices(enemylist, weights=self.weights, cum_weights=None, k=1)

        if str(enemy_name[0])=='miniboss.png':
            enemy_string=os.path.join(dir_path,'Game_imgs','miniboss2.png')
            self.image = pygame.image.load(enemy_string).convert_alpha()
            self.image = pygame.transform.scale(self.image, (110,95))
            self.rect = self.image.get_rect()
            self.rect.x = random.choice([100,200,300,400,500,640,700])
            self.rect.y = -self.rect.height+50
            self.vel_x = 0
            self.static_hp=c.miniboss_health
            self.hp = self.static_hp   #health value of enemy
            
            self.vel_y = c.enemyspeed

            self.type='miniboss'
            self.mask = pygame.mask.from_surface(self.image)
            self.single_hit_1=0
            self.single_hit_2=0


            eny_id=max(eny_id_list)+1
            self.Enemy_id='E2'+str(eny_id)
            eny_id_list.append(eny_id)
            self.kill_tag=0

        elif str(enemy_name[0])=='dragon3.png':
            enemy_string=os.path.join(dir_path,'Game_imgs','dragon3.png')
            self.image = pygame.image.load(enemy_string).convert_alpha()
            self.image = pygame.transform.scale(self.image, (75,75))
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(0, c.DISPLAY_SIZE[0] - self.rect.width)
            self.rect.y = -self.rect.height  +50
            self.vel_x = 0
            self.static_hp=c.mini_health
            self.hp = self.static_hp   #health value of enemy
            self.vel_y = 2

            self.type='mini'
            self.mask = pygame.mask.from_surface(self.image)
            eny_id=max(eny_id_list)+1
            self.Enemy_id='E1'+str(eny_id)
            eny_id_list.append(eny_id)
            self.single_hit_1=0
            self.single_hit_2=0
            self.kill_tag=0

        elif str(enemy_name[0])=='big_boss.png':
            enemy_string=os.path.join(dir_path,'Game_imgs','big_boss.png')
            self.image = pygame.image.load(enemy_string).convert_alpha()
            self.image = pygame.transform.scale(self.image, (180,150))
            self.rect = self.image.get_rect()
            self.rect.x = 400
            self.rect.y = -self.rect.height+150
            self.vel_x = 0
            self.hp = 100   #health value of enemy
            self.vel_y = 2
            self.score_value = 15
            self.penalty_value = 15
            self.type='BOSS'
            self.mask = pygame.mask.from_surface(self.image)
            self.single_hit_1=0
            self.single_hit_2=0
            self.kill_tag=0
            eny_id=max(eny_id_list)+1
            self.Enemy_id='E3'+str(eny_id)
            eny_id_list.append(eny_id)

        # Explosion Animation
        self.img_b_explosion_01 = pygame.image.load(os.path.join(dir_path,'Game_imgs','Explosion','blue-explosion-1.png')).convert_alpha()
        self.img_b_explosion_01 = pygame.transform.scale(self.img_b_explosion_01, (70, 70))


        self.img_b_explosion_03 = pygame.image.load(os.path.join(dir_path,'Game_imgs','Explosion','blue-explosion-3.png')).convert_alpha()
        self.img_b_explosion_03 = pygame.transform.scale(self.img_b_explosion_03, (70, 70))

        self.img_b_explosion_06 = pygame.image.load(os.path.join(dir_path,'Game_imgs','Explosion','blue-explosion-6.png')).convert_alpha()
        self.img_b_explosion_06 = pygame.transform.scale(self.img_b_explosion_06, (70, 70))

        self.anim_explosion1 = [self.img_b_explosion_01,
                               self.img_b_explosion_03,
                               self.img_b_explosion_06]


        self.anime1_index = 0
        self.max_frame_length = 1
        self.frame_length = self.max_frame_length
        self.is_destroyed = False
        self.is_invincible = False


    def update(self):

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.is_destroyed:
            self.penalty_value = 0
            max_index = len(self.anim_explosion1) - 1
            if self.frame_length ==0:
                self.anime1_index +=1
                if self.anime1_index > max_index:
                    self.kill()
                else:
                    self.image = self.anim_explosion1[self.anime1_index]
                    self.frame_length = self.max_frame_length
            else:
                self.frame_length -= 1

    # explosion
    def get_hit(self):
        reward1=0
        reward2=0
        inter_df=pd.DataFrame(0, index=np.arange(len([1])), columns=['coop_kill_mini',
                                                                     'coop_kill_miniboss',
                                                                     'A1_kill_miniboss',
                                                                     'A2_kill_miniboss',
                                                                     'A1_kill_mini',
                                                                     'A2_kill_mini'])
        coop_kill_miniboss = 0
        coop_kill_mini = 0
        A1_kill_miniboss = 0
        A2_kill_miniboss = 0
        A1_kill_mini=0
        A2_kill_mini=0
        if not self.is_invincible:
            self.hp -= 1
            if self.hp <= 0:
                coop_hit=False
                if self.type=='miniboss':

                    indi_factor_1=self.single_hit_1/self.static_hp
                    indi_factor_2=self.single_hit_2/self.static_hp
                    coop_factor = 1 - abs(indi_factor_1-indi_factor_2)

                    if coop_factor >= c.coop_factor:
                        # ADD COOP BONUS
                        print("Coop+shot")
                        reward1=coop_factor*indi_factor_1*20
                        reward2=coop_factor*indi_factor_2*20
                        self.kill_tag='CC'
                        coop_kill_miniboss = 1

                    else:
                        if indi_factor_1>indi_factor_2:
                            reward1=1
                            self.kill_tag='CD'
                            A1_kill_miniboss = 1
                        if indi_factor_2>indi_factor_1:
                            reward2=1
                            self.kill_tag='DC'
                            A2_kill_miniboss = 1

                if self.type=='mini':
                    if self.single_hit_1==self.single_hit_2:
                        reward1=1
                        reward2=1
                        coop_kill_mini=1
                    if self.single_hit_1 > 2:
                        reward1=1
                        reward2=0
                        A1_kill_mini=1
                    if self.single_hit_2 > 2:
                        reward1=0
                        reward2=1
                        A2_kill_mini=1

                inter_df['coop_kill_mini'].iloc[0]=coop_kill_mini
                inter_df['coop_kill_miniboss'].iloc[0]=coop_kill_miniboss
                inter_df['A1_kill_miniboss'].iloc[0]=A1_kill_miniboss
                inter_df['A2_kill_miniboss'].iloc[0]=A2_kill_miniboss
                inter_df['A1_kill_mini'].iloc[0]=A1_kill_mini
                inter_df['A2_kill_mini'].iloc[0]=A2_kill_mini

                self.is_invincible = True
                self.is_destroyed = True
                self.vel_x = 0
                self.vel_y = 0
                self.rect.x = self.rect.x
                self.rect.y = self.rect.y
                self.image = self.anim_explosion1[self.anime1_index]
        else:
            pass

        return reward1, reward2, inter_df

    def self_distruct(self):
        self.is_destroyed = True
        






