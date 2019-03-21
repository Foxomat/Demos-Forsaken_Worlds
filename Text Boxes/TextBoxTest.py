#Demsonstration und Implementierung der Textfeld-Klasse
# by Foxomat

#-----------------------------------------------Imports-----------------------------------------------------------------
import pygame, sys, TextBoxes
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

#-------------------------------------------Box-initialisierung---------------------------------------------------------
    test = TextBoxes.TextBox(50, 50, 100, 20)
    zahl = TextBoxes.NumberBox(50, 100, 50, 40)

#--------------------------------------------"game"-loop----------------------------------------------------------------
    while True:
        WINSURF.fill((255, 255, 255))  # Hinterrund weiß

        # event Handling
        for event in pygame.event.get():
            if event.type == QUIT:  # normaler quit event check
                pygame.quit()
                sys.exit()

            test.update(event)
            zahl.update(event)

        test.draw(WINSURF)
        zahl.draw(WINSURF)

        if zahl.get_output_ready():
            print(zahl.get_output())

        CLOCK.tick()
        pygame.display.update()  # normales pygame zeug

if __name__ == '__main__':  # für die main-Funktion. muss man da immer am ende hinschreiben
    main()
