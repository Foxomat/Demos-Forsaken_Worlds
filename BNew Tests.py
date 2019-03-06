import pygame, sys, Buttons
from pygame.locals import *

# Konstanten
FPS = 60
WINWIDTH = 1200
WINHEIGHT = 750

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def main():
    pygame.init()
    CLOCK = pygame.time.Clock()

    WINSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    test = Buttons.DrawButton(50, 50, "ikone", "ikoneEditor")


    while True:
        WINSURF.fill(WHITE)
        test.drawHitbox(WINSURF)

        # check for the QUIT event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            test.drawMouseOverButton(WINSURF, event)
        test.drawMouseOverButton(WINSURF)

        CLOCK.tick()
        pygame.display.update()



if __name__ == '__main__':
    main()
