#Demsonstration und Implementierung der Knopf-Klasse
# by Foxomat

#-----------------------------------------------Imports-----------------------------------------------------------------
import pygame, sys, Buttons
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
    Sound = pygame.mixer.Sound('pickup.wav')  # sound für später

#-----------------------------------------knopf-initialisierung---------------------------------------------------------

    test = Buttons.DrawButton(500, 300, "ikone.gif", "ikoneEditor.gif", "ikoneEditor.gif")
    test.set_widthHeight(30, 30)  # mit Hitbox-größenänderung

    test2 = Buttons.Button(700, 300)
    test2.set_widthHeight(30, 30)

#--------------------------------------------"game"-loop----------------------------------------------------------------

    while True:
        WINSURF.fill((255, 255, 255))  # Hinterrund weiß
        test.draw_hitbox(WINSURF)  # Anzeigen der Hitboxen der Knöpfe
        test2.draw_hitbox(WINSURF)

        # event Handling
        for event in pygame.event.get():
            if event.type == QUIT:  # normaler quit event check
                pygame.quit()
                sys.exit()

            test.update(event)  # update-Funktion für knöpfe; muss immer im event handling stehen
            test2.update(event)

        test.draw(WINSURF)  # draw heißt, zeichne deinen momentanen zustand (cursor drüber oder gedrückt oder nix)

        if test.get_left_mouse_pressed():
            Sound.play()  # das Wichtigste: irgendwas passiert wennn der Knopf gedrückt wird

        if test2.get_left_mouse_pressed():
            print("ok")

        CLOCK.tick()
        pygame.display.update()  # normales pygame zeug


#-----------------------------------------------Abschluss---------------------------------------------------------------

if __name__ == '__main__':  # für die main-Funktion. muss man da immer am ende hinschreiben
    main()
