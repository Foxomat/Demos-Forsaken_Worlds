#Demsonstration und Implementierung der Scroll-Menü-Klasse
# by Foxomat

#-----------------------------------------------Imports-----------------------------------------------------------------
import pygame, sys, ScrollMenues
from pygame.locals import *

#----------------------------------------------Konstanten---------------------------------------------------------------
FPS = 60
WINWIDTH = 1200
WINHEIGHT = 750

#-----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------Main-Funktion--------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

def main():

#---------------------------------------------pygame-zeugs--------------------------------------------------------------
    pygame.init()
    CLOCK = pygame.time.Clock()
    WINSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

#----------------------------------------scoller-initialisierung--------------------------------------------------------

    test = ScrollMenues.ScrollMenu('Lieblingstier', Rect(50, 50, 350, 45))
    test.add('Ratte')
    test.add('Katze')
    test.add('Hund')
    test.add('Maus')
    test.add('Tiger')
    test.add('Adler')
    test.add('Aal')
    test.add('Hai')
    test.add('Zebra')
    test.delete('Ratte')

#--------------------------------------------"game"-loop----------------------------------------------------------------

    while True:
        WINSURF.fill((255, 255, 255))  # Hinterrund weiß

        # event Handling
        for event in pygame.event.get():
            if event.type == QUIT:  # normaler quit event check
                pygame.quit()
                sys.exit()
            test.update(event)

        test.draw(WINSURF)

        CLOCK.tick()
        pygame.display.update()  # normales pygame zeug


#-----------------------------------------------Abschluss---------------------------------------------------------------

if __name__ == '__main__':  # für die main-Funktion. muss man da immer am ende hinschreiben
    main()
