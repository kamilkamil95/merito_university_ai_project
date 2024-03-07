import pygame
from pygame.locals import *
from game.config import DinoConfig

class Cactus(DinoConfig):
    def __init__(self, x, y, width, height, img, scroll_speed = 7):
        super().__init__()  # Wywołanie konstruktora klasy nadrzędnej
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scroll_speed = scroll_speed
        self.img = pygame.transform.scale(img, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        self.x -= self.scroll_speed # Moves cactus to the left
        self.rect.x, self.rect.y = self.x, self.y # Update position atributes

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))