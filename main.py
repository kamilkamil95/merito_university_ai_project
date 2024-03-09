import pygame
import neat
import sys
import os
import math
import random
from pygame.locals import *
from game.cactus import Cactus
from game.dinosaur import Dinosaur

pygame.init()
clock = pygame.time.Clock()
# options
# Options
WINDOW_SIZE = (1000, 500) # (Width, Height)
DRAW_LINES = True # (Draw lines between the dinosaur and cactus to see what the AI sees)

screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)

GROUND_LEVEL = WINDOW_SIZE[1]/2 + 75
ground_rect = pygame.Rect(0, GROUND_LEVEL, WINDOW_SIZE[0], WINDOW_SIZE[1])

dinosaur_img = pygame.image.load('data/dinosaur.png').convert_alpha()
cactus_img = pygame.image.load('data/cactus.png').convert_alpha()
font = pygame.font.Font('data/roboto.ttf', 25)

generation = 0




def get_distance(first_pos, second_pos):
    # Distance formula
    dx = first_pos[0] - second_pos[0]
    dy = first_pos[1] - second_pos[1]
    return math.sqrt(dx**2 + dy**2)

def remove_dinosaur(index):
    # 'Kills' the dinosaur and its corresponding genome and nn
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)

def draw():
    display.fill('white')

    pygame.draw.line(display, (75, 75, 75), (0, GROUND_LEVEL), (WINDOW_SIZE[0], GROUND_LEVEL), 3)

    for dinosaur in dinosaurs:
        dinosaur.draw(display)
        if DRAW_LINES:
            pygame.draw.line(
                display, 
                (50, 200, 75), 
                (dinosaur.rect.right, dinosaur.rect.centery), 
                dinosaur.closest_pipe.rect.midtop,
                2
            )
    for cactus in cacti:
        cactus.draw(display)

    score_text = font.render(f'Score: 0', 1, 'black')
    alive_text = font.render(f'Number alive: {len(dinosaurs)}', 1, 'black')
    generation_text = font.render(f'Generation: {generation}', 1, 'black')
    display.blit(score_text, (5, WINDOW_SIZE[1] - 100))
    display.blit(alive_text, (5, WINDOW_SIZE[1] - 40))
    display.blit(generation_text, (5, WINDOW_SIZE[1] - 75))
    screen.blit(display, (0, 0))
    pygame.display.update()
###sss
def main(genomes, config):
    global cacti, dinosaurs, nets, ge, generation

    cacti = [Cactus(WINDOW_SIZE[0] + 100, GROUND_LEVEL - 86, 50, 86, cactus_img)]

    dinosaurs = []
    nets = []
    ge = []

    scroll_speed = 7
    generation += 1

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinosaurs.append(Dinosaur(100, GROUND_LEVEL-90, 80, 85, dinosaur_img, cacti))
        g.fitness = 0
        ge.append(g)

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Break if all the dinosaurs die
        if len(dinosaurs) <= 0:
            break

        # Adding new cactus
        if len(cacti) <= 1:
            if cacti[0].x < random.randint(300, WINDOW_SIZE[0] - 200) + scroll_speed:
                cacti.append(Cactus(WINDOW_SIZE[0] + 100, GROUND_LEVEL - 86, 50, 86, cactus_img, scroll_speed))

        for cactus in cacti:
            cactus.update()
            if cactus.x < -100:
                cacti.remove(cactus)
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(cactus.rect):
                    ge[i].fitness -= 3
                    remove_dinosaur(i)

        for i, dinosaur in enumerate(dinosaurs):
            dinosaur.update()
            # Check if the dinosaur passed a cactus
            # Getting the closest cactus by finding the leftmost cactus that is to the right of the dinosaur
            dinosaur.closest_pipe = [cactus for cactus in cacti if cactus.rect.x > dinosaur.x - dinosaur.width][0]
            # Checking if the dinosaur passed a cactus by comparing it to the closest cactus in the last frame and seeing if there is a change
            if dinosaur.closest_pipe != dinosaur.last_closest_pipe:
                ge[i].fitness += 1
                for cactus in cacti:
                    # Increace speed everytime a cactus is passed
                    cactus.scroll_speed += 0.05
                    scroll_speed += 0.05 
            dinosaur.last_closest_pipe = dinosaur.closest_pipe

            # Giving all dinsoaurs a little fitness for staying alive
            ge[i].fitness += 0.05

            output = nets[i].activate(
                (
                    dinosaur.y,
                    get_distance((dinosaur.x, dinosaur.y), dinosaur.closest_pipe.rect.midtop)
                )
            )

            if output[0] > 0.5:
                dinosaur.jump()

        draw()

# Setup the NEAT nn
def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)