import pygame
import neat
import sys
import os
import math
import random
from pygame.locals import *
from game.cactus import Cactus
from game.dinosaur import Dinosaur
from game.config import DinoConfig

pygame.init()
clock = pygame.time.Clock()

# Options


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
    DinoConfig.display.fill('white')

    pygame.draw.line(DinoConfig.display, (75, 75, 75), (0, DinoConfig.GROUND_LEVEL), (DinoConfig.WINDOW_SIZE[0], DinoConfig.GROUND_LEVEL), 3)

    for dinosaur in dinosaurs:
        dinosaur.draw(DinoConfig.display)
        if DinoConfig.DRAW_LINES:
            pygame.draw.line(
                DinoConfig.display,
                (50, 200, 75), 
                (dinosaur.rect.right, dinosaur.rect.centery), 
                dinosaur.closest_pipe.rect.midtop,
                2
            )
    for cactus in cacti:
        cactus.draw(DinoConfig.display)

    score_text = DinoConfig.font.render(f'Score: 0', 1, 'black')
    alive_text = DinoConfig.font.render(f'Number alive: {len(dinosaurs)}', 1, 'black')
    generation_text = DinoConfig.font.render(f'Generation: {generation}', 1, 'black')
    DinoConfig.display.blit(score_text, (5, DinoConfig.WINDOW_SIZE[1] - 100))
    DinoConfig.display.blit(alive_text, (5, DinoConfig.WINDOW_SIZE[1] - 40))
    DinoConfig.display.blit(generation_text, (5, DinoConfig.WINDOW_SIZE[1] - 75))
    DinoConfig.screen.blit(DinoConfig.display, (0, 0))
    pygame.display.update()
###sss


def main(genomes, config):
    global cacti, dinosaurs, nets, ge, generation

    cacti = [Cactus(DinoConfig.WINDOW_SIZE[0] + 100, DinoConfig.GROUND_LEVEL - 86, 50, 86, DinoConfig.cactus_img)]
    dinosaurs = []
    nets = []
    ge = []

    scroll_speed = 7
    generation += 1

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinosaurs.append(Dinosaur(100, DinoConfig.GROUND_LEVEL-90, 80, 85, dinosaur_img, cacti))
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
            if cacti[0].x < random.randint(300, DinoConfig.WINDOW_SIZE[0] - 200) + scroll_speed:
                cacti.append(Cactus(DinoConfig.WINDOW_SIZE[0] + 100, DinoConfig.GROUND_LEVEL - 86, 50, 86, DinoConfig.cactus_img, scroll_speed))

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