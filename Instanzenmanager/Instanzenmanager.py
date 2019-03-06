import pygame, sys, Buttons
from Buttons import *
from pygame.locals import *

# Konstanten
FPS = 60
WINWIDTH = 1200
WINHEIGHT = 750

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def main():
    # pygame zeug einrichten
    pygame.init()
    CLOCK = pygame.time.Clock()

    WINSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Instanzenmanager')

    ikone = pygame.image.load('ikoneEditor.gif')
    pygame.display.set_icon(ikone)


    while True:

        # check for the QUIT event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        WINSURF.fill(WHITE)

        CLOCK.tick()
        pygame.display.update()


if __name__ == '__main__':
    main()
