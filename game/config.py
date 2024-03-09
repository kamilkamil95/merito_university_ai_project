import pygame

class DinoConfig():
        WINDOW_SIZE = (1000, 500)  # (Width, Height)
        DRAW_LINES = True  # (Draw lines between the dinosaur and cactus to see what the AI sees)
        GROUND_LEVEL = WINDOW_SIZE[1] / 2 + 75
        screen = pygame.display.set_mode(WINDOW_SIZE)
        display = pygame.Surface(WINDOW_SIZE)
        ground_rect = pygame.Rect(0, GROUND_LEVEL, WINDOW_SIZE[0], WINDOW_SIZE[1])


        # screen = None
        # display = None
        dinosaur_img = None
        cactus_img = None
        font = None

        @staticmethod
        def initialize():
            DinoConfig.screen = pygame.display.set_mode(DinoConfig.WINDOW_SIZE)
            DinoConfig.display = pygame.Surface(DinoConfig.WINDOW_SIZE)
            DinoConfig.dinosaur_img = pygame.image.load('data/dinosaur.png').convert_alpha()
            DinoConfig.cactus_img = pygame.image.load('data/cactus.png').convert_alpha()
            DinoConfig.font = pygame.font.Font('data/roboto.ttf', 25)