import pygame
from game.config import DinoConfig
class Dinosaur(DinoConfig):
    def __init__(self, x, y, width, height, img, cacti): #img must be a pygame surface object
        super().__init__()  # Wywołanie konstruktora klasy nadrzędnej
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = pygame.transform.scale(img, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.vertical_momentum = 0
        self.onGround = False
        self.last_closest_pipe = cacti[0] # Setting the closest cactus to the leftmost cactus by default

    def update(self):
        self.x, self.y = self.rect.x, self.rect.y # Updating position atributes
        self.movement()

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

    def jump(self):
        if self.onGround:
            self.vertical_momentum = -11

    def movement(self):
        self.rect.y += self.vertical_momentum

        if self.rect.colliderect(self.ground_rect):
            self.onGround = True
        else:
            self.onGround = False

        if self.onGround:
            self.rect.bottom = self.ground_rect.top + 1 # Adding 1 so that the dinosaur continues to collide with the rect, instead of shaking up and down
            # Prevent from falling through the ground
            self.vertical_momentum = 0
        else:
            # Add gravity
            self.vertical_momentum += 0.5

        # Cap gravity
        if self.vertical_momentum >= 40:
            self.vertical_momentum = 40
