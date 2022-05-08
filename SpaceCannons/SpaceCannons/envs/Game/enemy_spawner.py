from Game.enemy import Enemy
import pygame
import random
import Params_game as C


class EnemySpawner:
    def __init__(self):
        self.enemy_group = pygame.sprite.Group()
        self.spawn_timer = 3  # time for first enemy
        self.enemy_count=0

    def update(self,game_level):
        self.enemy_group.update()


        if self.spawn_timer == 0:
            self.spawn_enemy(game_level)
            self.spawn_timer = C.spawn_timer #(40,50)
            self.enemy_count+=1
        else:
            self.spawn_timer -= 1

    def spawn_enemy(self,game_level):
        new_enemy = Enemy(game_level)
        self.enemy_group.add(new_enemy)

