import pygame
from Game.partical import partical
import random


class partical_spawner:
    def __init__(self):
        self.partical_group = pygame.sprite.Group()

    def update(self):
        self.partical_group.update()


    def spawn_particals(self, pos):
        random_number = random.randrange(1,3)
        for num_partical in range(random_number):
            new_partical = partical()
            new_partical.rect.x=pos[0]
            new_partical.rect.y=pos[1]
            self.partical_group.add(new_partical)
