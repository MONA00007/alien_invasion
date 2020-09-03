import sys
import pygame


def run_blue():

    pygame.init()
    screen = pygame.display.set_mode((900, 600))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 255))
        pygame.display.flip()


run_blue()
