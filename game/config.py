import pygame

class DinoConfig():
    def __init__(self):
        self.WINDOW_SIZE = (1000, 500)  # (Width, Height)
        # DRAW_LINES = True  # (Draw lines between the dinosaur and cactus to see what the AI sees)
        self.GROUND_LEVEL = self.WINDOW_SIZE[1] / 2 + 75

        #screen = pygame.display.set_mode(self.WINDOW_SIZE)
        #display = pygame.Surface(self.WINDOW_SIZE)

        self.ground_rect = pygame.Rect(0, self.GROUND_LEVEL, self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
