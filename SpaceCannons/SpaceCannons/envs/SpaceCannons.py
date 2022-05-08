from typing import Protocol
from numpy.core.numeric import False_
import pygame
import Params_game as C
from Game.players import Gameplayer1, Gameplayer2
from Game.background import backG
from Game.enemy_spawner import EnemySpawner
from Game.partical_spawner import partical_spawner
import numpy as np
from pygame import display, key
from pygame.surfarray import array3d
from pygame.event import pump
import pandas as pd
from pygame.locals import *
import gym
from gym import spaces
from torch.nn.functional import interpolate
import cv2



class SpaceCannons(gym.Env):
    def __init__(self):
        super(SpaceCannons, self).__init__()
        # os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        pygame.display.init()
        pygame.display.set_caption('DO NOT CLOSE THIS WINDOW--->Experiment in progress by mverma"')
        self.clock = pygame.time.Clock()
        self.history = []
        self.V2=C.V2

        self.screen = display.set_mode(C.DISPLAY_SIZE)
        self.screen.fill((0, 0, 0))

        self.FRAME_COUNT=0
        if self.V2:
            self.action_space = [spaces.Discrete(3),spaces.Discrete(3)]
        else:
            self.action_space = [spaces.Discrete(4),spaces.Discrete(4)]

        self.observation_space = spaces.Box(low=0, high=255, shape=(950,700, 1), dtype=np.uint8)
        self.enemycount=0





        self.enemy_weights = [0,100,0]
        print("PLAYER_HEALTH", C.PLAYER_HEALTH)
        print("bullet_penalty: ", C.bullet_penalty)
        print('enemy_weights: ',self.enemy_weights)
        print('initial setup complete')

        self.V2=C.V2
    def reset(self):
        self.total_bullet_penalty=0
        self.screen.fill((0, 0, 0))

        self.bg = backG()
        self.bg_group = pygame.sprite.Group()
        self.bg_group.add(self.bg)
        
        self.game_level=2

        self.enemy1_kill_count=0
        self.enemy2_kill_count=0

        self.A1_kills =0
        self.A2_kills =0
        self.enemy1_evasive_count=0
        self.enemy2_evasive_count=0

        self.human_positive_reinforcement = False

        self.player1 = Gameplayer1()
        self.player2 = Gameplayer2()

        self.enemy_spawner = EnemySpawner()
        self.partical_spawner = partical_spawner()

        self.sprit_group = pygame.sprite.Group()
        self.sprit_group.add(self.player2)
        self.sprit_group.add(self.player1)

        # self.angle_update1=0
        # self.angle_update2=0

        self.bullet_count_red = 100000
        self.bullet_count_blue = 100000
        self.running = True
        self.cool_down = 100
        image = array3d(display.get_surface())
        return image

    def step(self, action):
        self.FRAME_COUNT+=1

        Demo=action[2]

        flag = False # The flag is essential.

        for event in pygame.event.get():
            # At each frame it loops through all possible events.
            keys = key.get_pressed() # It gets the states of all keyboard keys.

            if Demo==False:
                if event.type == KEYDOWN: # If the type is KEYDOWN (DIFFERENT FROM "HELD").
                    if keys[K_SPACE]: # And if the key is K_SPACE:
                        flag = True # The flag is set to true.

            if Demo==True:
                if event.type == KEYDOWN:

                    if keys[K_LEFT]:
                        action[0]=1
                    elif keys[K_RIGHT]:
                        action[0]=0
                    else:
                        action[0]=2

                    if keys[K_a]:
                        action[1]=1
                    elif keys[K_d]:
                        action[1]=0
                    else:
                        action[1]=2


            if flag == True: # DON'T USE "while flag == true", it'll crash everything. At every frame, it'll check if the flag is true up there. It's important to remember that the KEYDOWN worked ONLY ONCE, and it was enough to set that flag. So, at every frame, THE FLAG is checked, NOT THE KEYDOWN STATE. Every "player movement" while a key is being held MUST be done through flags.
                self.human_positive_reinforcement = True
            else:
                self.human_positive_reinforcement = False

        self.last_shot1=0
        self.last_shot2=0
        # pump()
        done = False

        reward_1 = 0
        reward_2 = 0
        reward_3 = 0
        bullet_penalty_1 = 0
        bullet_penalty_2 = 0
        evasive_count_miniboss=0
        evasive_count_mini=0
        self.total_bullet_penalty=0

        A1_kill_miniboss=0
        A2_kill_miniboss=0
        A1_kill_mini =0
        A2_kill_mini=0
        A2_kill_mini=0
        coop_kill_mini=0
        coop_kill_miniboss=0

        if self.V2:
            if action[0]==0:
                if not self.player1.angle <-70:
                    self.player1.angle -= 5

            if action[0] == 1 :
                if not self.player1.angle >70:
                    self.player1.angle += 5

            if action[1] == 0 :
                if not self.player2.angle <-70:
                    self.player2.angle -= 5

            if action[1] == 1:
                if not self.player2.angle >70:
                    self.player2.angle += 5


            self.player1.shoot(self.player1.angle,self.screen)
            self.player2.shoot(self.player1.angle, self.screen)

        # else:
        #     if action[0]==0:
        #         if not self.player1.angle <-70:
        #             self.player1.angle -= 5

        #     if action[0] == 1:
        #         if not self.player1.angle >70:
        #             self.player1.angle += 5

        #     if action[1] == 0:
        #         if not self.player2.angle <-70:
        #             self.player2.angle -= 5

        #     if action[1] == 1:
        #         if not self.player2.angle >70:
        #             self.player2.angle += 5

        #     # if fire_1:
        #     if action[0] == 2:
        #         self.player1.shoot(self.player1.angle,self.screen)

        #     # if fire_2:
        #     if action[1] == 2:
        #         self.player2.shoot(self.player1.angle, self.screen)


# Collision detection
        collided_1 = pygame.sprite.groupcollide(self.player1.bullets_P1, self.enemy_spawner.enemy_group, False, False,pygame.sprite.collide_mask)
        collided_2 = pygame.sprite.groupcollide(self.player2.bullets_P2, self.enemy_spawner.enemy_group,False, False,pygame.sprite.collide_mask)



        if collided_1 and collided_2:
            if list(collided_1.values())[0][0].Enemy_id == list(collided_2.values())[0][0].Enemy_id and list(collided_2.values())[0][0].type=='mini':
                for bullet1, enemy1 in collided_1.items():
                    for bullet2, enemy2 in collided_2.items():
                        if enemy1[0].Enemy_id == enemy2[0].Enemy_id and enemy1[0].type=='mini' and not enemy1[0].hp <= 0:

                            enemy1[0].single_hit_1+=1
                            enemy1[0].single_hit_2+=1

                            #decrease enemy health
                            if enemy1[0].hp==1:
                                reward_1, reward_2, interdf =enemy1[0].get_hit()

                            if enemy1[0].hp >= 2:
                                reward_1, reward_2, interdf = enemy2[0].get_hit()
                                reward_1, reward_2, interdf = enemy1[0].get_hit()

                            A1_kill_miniboss=interdf['A1_kill_miniboss'][0]
                            A2_kill_miniboss=interdf['A2_kill_miniboss'][0]
                            A1_kill_mini =interdf['A1_kill_mini'][0]
                            A2_kill_mini=interdf['A2_kill_mini'][0]
                            coop_kill_mini=interdf['coop_kill_mini'][0]
                            coop_kill_miniboss=interdf['coop_kill_miniboss'][0]

                            #destroy bullets
                            bullet2.kill()
                            del bullet2
                            bullet1.kill()
                            del bullet1
                            break
                    break

            if list(collided_1.values())[0][0].Enemy_id == list(collided_2.values())[0][0].Enemy_id and list(collided_2.values())[0][0].type=='miniboss':
                for bullet1, enemy1 in collided_1.items():
                    for bullet2, enemy2 in collided_2.items():
                        if enemy1[0].Enemy_id == enemy2[0].Enemy_id and enemy1[0].type=='miniboss' and not enemy1[0].hp <= 0:

                            enemy1[0].single_hit_1+=1
                            enemy1[0].single_hit_2+=1


                            #decrease enemy health
                            if enemy1[0].hp==1:
                                reward_1, reward_2, interdf =enemy1[0].get_hit()

                            if enemy1[0].hp >= 2:
                                reward_1, reward_2, interdf = enemy2[0].get_hit()
                                reward_1, reward_2, interdf = enemy1[0].get_hit()

                            A1_kill_miniboss=interdf['A1_kill_miniboss'][0]
                            A2_kill_miniboss=interdf['A2_kill_miniboss'][0]
                            A1_kill_mini =interdf['A1_kill_mini'][0]
                            A2_kill_mini=interdf['A2_kill_mini'][0]
                            coop_kill_mini=interdf['coop_kill_mini'][0]
                            coop_kill_miniboss=interdf['coop_kill_miniboss'][0]

                            #destroy bullets
                            bullet2.kill()
                            del bullet2
                            bullet1.kill()
                            del bullet1
                            break
                    break

        if collided_1:
            for bullet1, enemy1 in collided_1.items():
                # # creating statistics for the killed  enemy
                if  not enemy1[0].hp <= 0:
                    enemy1[0].single_hit_1 +=1
                    #hit the enemy
                    reward_1, reward_2,interdf = enemy1[0].get_hit()

                    A1_kill_miniboss=interdf['A1_kill_miniboss'][0]
                    A2_kill_miniboss=interdf['A2_kill_miniboss'][0]
                    A1_kill_mini =interdf['A1_kill_mini'][0]
                    A2_kill_mini=interdf['A2_kill_mini'][0]
                    coop_kill_mini=interdf['coop_kill_mini'][0]
                    coop_kill_miniboss=interdf['coop_kill_miniboss'][0]

                    #destroy bullets
                    bullet1.kill()
                    del bullet1


        if collided_2:
            for bullet2, enemy2 in collided_2.items():
                if  not enemy2[0].hp <= 0:
                    enemy2[0].single_hit_2 +=1
                    #hit the enemy
                    reward_1, reward_2,interdf = enemy2[0].get_hit()

                    A1_kill_miniboss=interdf['A1_kill_miniboss'][0]
                    A2_kill_miniboss=interdf['A2_kill_miniboss'][0]
                    A1_kill_mini =interdf['A1_kill_mini'][0]
                    A2_kill_mini=interdf['A2_kill_mini'][0]
                    coop_kill_mini=interdf['coop_kill_mini'][0]
                    coop_kill_miniboss=int(interdf['coop_kill_miniboss'][0])

                    #destroy bullets
                    bullet2.kill()
                    del bullet2



        for enemy in self.enemy_spawner.enemy_group:
            if enemy.rect.y > 585:

                if enemy.type=='mini':
                    evasive_count_mini=1
                    self.player1.get_hit()
                    reward_3 += C.mini_evade_penalty

                if enemy.type=='miniboss':
                    evasive_count_miniboss=1
                    self.player1.get_hit()
                    reward_3 += C.miniboss_evade_penalty
                enemy.kill()


        if self.player1.health <= 0 or self.player2.health <= 0:
            running = False
            done = True

        for bullet in self.player1.bullets_P1:
            if  bullet.center[1] <= 7 or bullet.center[0] <=4 or bullet.center[0]>=950:
                if self.V2 == False:
                    bullet_penalty_1 += C.bullet_penalty
                    self.total_bullet_penalty += C.bullet_penalty
                bullet.kill()

        for bullet in self.player2.bullets_P2:
            if  bullet.center[1] <= 7 or bullet.center[0] <=4 or bullet.center[0]>=950:
                if self.V2 == False:
                    bullet_penalty_2 += C.bullet_penalty
                    self.total_bullet_penalty += C.bullet_penalty
                bullet.kill()

        agent1_reward = reward_1 + reward_3 - bullet_penalty_1
        agent2_reward = reward_2 + reward_3 - bullet_penalty_2

        global_reward = [agent1_reward,agent2_reward]
        # print(global_reward)

        self.player1.hud.score.update_score(agent1_reward+agent2_reward)


        image = array3d(self.screen)
        # image = pygame.PixelArray(pygame.display.get_surface())
        image=cv2.transpose(image)
        # cv2.imshow("OpenCV Image Reading2", image)
        # cv2.waitKey(30) #is r

        info={'A1_kill_miniboss':A1_kill_miniboss,
              'A2_kill_miniboss':A2_kill_miniboss,
              'A1_kill_mini':A1_kill_mini,
              'A2_kill_mini':A2_kill_mini,


              'evasive_count_miniboss':evasive_count_miniboss,
              'evasive_count_mini':evasive_count_mini,


              'coop_kill_mini':coop_kill_mini,
              'coop_kill_miniboss':coop_kill_miniboss,


              "A1_kills":A1_kill_miniboss+A1_kill_mini,
              "A2_kills":A2_kill_miniboss+A2_kill_mini,


              'Tot_Bullet_penalty':self.total_bullet_penalty,
              'Tot_bullet_penalty_1':bullet_penalty_1,
              'Tot_bullet_penalty_2':bullet_penalty_2,
              'Positive_feed': self.human_positive_reinforcement,
              'action':action}



        self.render(self.enemy_weights)

        if coop_kill_miniboss == 1:
            print(global_reward)
        return image, global_reward, done, info


    def render(self,enemy_weights):
        clock = pygame.time.Clock()

         # updates all the objects
        self.bg_group.update(self.screen)
        self.bg_group.draw(self.screen)
        self.sprit_group.update(self.screen)
        self.enemy_spawner.update(enemy_weights)
        self.partical_spawner.update()


        self.enemy_spawner.enemy_group.draw(self.screen)
        self.partical_spawner.partical_group.draw(self.screen)
        self.player1.hud.healthbar_group.draw(self.screen)
        self.player1.hud_group.draw(self.screen)
        self.player1.hud.score_group.draw(self.screen)
        self.player1.bullets_P1.draw(self.screen)
        self.player2.bullets_P2.draw(self.screen)
        pygame.display.update()
        # clock.tick(30)

    def get_screen(self):
        return array3d(display.get_surface())