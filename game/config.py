import pygame

class DinoConfig():
        WINDOW_SIZE = (1000, 500)  # (Width, Height)
        DRAW_LINES = True  # (Draw lines between the dinosaur and cactus to see what the AI sees)
        GROUND_LEVEL = WINDOW_SIZE[1] / 2 + 75
        screen = pygame.display.set_mode(WINDOW_SIZE)
        display = pygame.Surface(WINDOW_SIZE)
        ground_rect = pygame.Rect(0, GROUND_LEVEL, WINDOW_SIZE[0], WINDOW_SIZE[1])
        dinosaur_img = pygame.image.load('data/dinosaur.png').convert_alpha()
        cactus_img = pygame.image.load('data/cactus.png').convert_alpha()
        font = pygame.font.Font('data/roboto.ttf', 25)