import pygame
import random
import Params_game as C
from Game.star import star

class backG(pygame.sprite.Sprite):
    def __init__(self):
        super(backG,self).__init__()

        self.image = pygame.Surface(C.DISPLAY_SIZE)
        self.col = (0,0,0)
        self.image.fill(self.col)
        self.rect = self.image.get_rect()
        self.stars = pygame.sprite.Group()
        self.timer = random.randrange(1,10)


    def update(self,display):
        self.stars.update()
        #Fix memmory leak
        for starx in self.stars:
            if starx.rect.y >= C.DISPLAY_SIZE[0]:
                self.stars.remove(starx)

        # if self.timer == 0:
        #     new_star = star()
        #     self.stars.add(new_star)
        #     self.timer = random.randrange(1,10)
        self.image.fill(self.col)
        self.stars.draw(self.image)
        self.timer -= 1
        display.blit(self.image, self.rect)
