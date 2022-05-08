import pygame
import random



class star(pygame.sprite.Sprite):
    def __init__(self):
        super(star, self).__init__()

        self.width = random.randrange(1,4)
        self.height = self.width
        self.size = (self.width, self.height)
        self.image = pygame.Surface(self.size)
        self.color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
        self.image.fill(self.color)
        self.rect= self.image.get_rect()
        self.rect.x= random.randrange(0,950)
        self.velocity_x = 0
        self.velocity_y = random.randrange(4,20)

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y


