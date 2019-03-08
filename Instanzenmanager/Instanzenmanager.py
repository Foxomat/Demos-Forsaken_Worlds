# Programm mit graficher Oberfläche zum erstellen von Instanzen für DEMOS
# by Foxomat

#-----------------------------------------------Imports-----------------------------------------------------------------
import pygame, sys, Buttons
from Buttons import *
from pygame.locals import *

#----------------------------------------------Konstanten---------------------------------------------------------------
FPS = 60
WINWIDTH = 1200
WINHEIGHT = 750

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (200, 20, 20)

#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------------------Main-Methode--------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

def main():

#----------------------------------Pygame-abhängige Konstanten und Zeugs------------------------------------------------
    global WINSURF  # Standard Display Surface
    global modeSwitch  # Knopf zum ändern von FRACTALMODE
    global FRACTALMODE  # Modus zum bearbeiten von Fractalmaps an/aus (sonst Instanzenmaps)

    # klar
    pygame.init()
    CLOCK = pygame.time.Clock()
    WINSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    # kosmetisches Gedöns
    ikone = pygame.image.load('ikoneEditor.gif')
    pygame.display.set_caption('Instanzenmanager')
    pygame.display.set_icon(ikone)

    # grundsätzliches Zeug
    FRACTALMODE = True
    fontObj = pygame.font.Font(None, 25)

    # Buttons
    modeSwitch = Buttons.DrawButton(30, 55, 'ButtonUnpressed.bmp', 'ButtonPressed.bmp', 'ButtonUnpressed.bmp')
    modeSwitch.setWidthHeight(20, 20)

    # Button Beschriftungen
    modeSwitchTxtSurf = fontObj.render("Fractal Mode: on", True, BLACK)
    modeSwitchTxtRect = modeSwitchTxtSurf.get_rect()
    modeSwitchTxtRect.topleft = (modeSwitch.getX(), modeSwitch.getY())
    modeSwitchTxtRect.x = modeSwitchTxtRect.x + modeSwitch.getWidth() + 15

    ButtonNameList = [modeSwitchTxtSurf, modeSwitchTxtRect]

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------Main-Loop---------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
    while True:

#------------------------------------------Fractal-Mode-Loop------------------------------------------------------------
        fracButtonsDict = {}
        for i in range(0, 32):
            for j in range(0, 32):
                key = (i, j)
                value = Buttons.Button(505 + j*20, 55 + i*20)
                fracButtonsDict[key] = value

        while FRACTALMODE:
            drawBackground()  # Hintergrund, der immer gezeichnet wird

            doEventHnadling(fracButtonsDict)  # event Handling

            drawMenuButtons()  # zeichnet alle Menüknöpfe

            ButtonNameList = updateMenuButtonNames(ButtonNameList, fontObj)
            drawMenuButtonNames(ButtonNameList)

            drawFractalGrid()  # zeichnet 32x32 Raster für Fractalmaps

            if modeSwitch.getButtonPressed():  # Check, ob FRACTALMODE aus sein soll
                FRACTALMODE = False

            CLOCK.tick()
            pygame.display.update()

        del fracButtonsDict

#------------------------------------------Instanz-Mode-Loop------------------------------------------------------------

        while not FRACTALMODE:
            drawBackground()  # Hintergrund, der immer gezeichnet wird

            doEventHnadling()  # event Handling

            drawMenuButtons()  # zeichnet alle Menüknöpfe

            ButtonNameList = updateMenuButtonNames(ButtonNameList, fontObj)
            drawMenuButtonNames(ButtonNameList)

            if modeSwitch.getButtonPressed():  # Check, ob FRACTALMODE an sein soll
                FRACTALMODE = True

            CLOCK.tick()
            pygame.display.update()



#-----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------extra Methoden-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------


#-------------------------------------------update-Funktionen-----------------------------------------------------------
def updateMenuButtons(event):  # updatet die Knöpfe links
    modeSwitch.update(event)

def updateMenuButtonNames(namelist, font):  # updatet die Bezeichnungen der Knöpfe links
    if FRACTALMODE:
        modeSwitchTxtSurf = font.render("Fractal Mode: on", True, BLACK)
    else:
        modeSwitchTxtSurf = font.render("Fractal Mode: off", True, BLACK)

    namelist = [modeSwitchTxtSurf, namelist[1]]
    return namelist

def updateFracButtons(fracDict, event):  # updatet die Knöpfe des Fractalmap-Rasters
    for i in range(0, 32):
        for j in range(0, 32):
            fracDict[(i, j)].update(event)



#--------------------------------------------draw-Funktionen------------------------------------------------------------
def drawBackground():  # zeichnet den Hintergrund, der immer da ist
    WINSURF.fill(WHITE)
    pygame.draw.line(WINSURF, BLACK, (450, 0), (450, 750), 6)

    if FRACTALMODE:
        pygame.draw.rect(WINSURF, RED, (modeSwitch.getX()-3, modeSwitch.getY()-3, modeSwitch.getWidth()+5,
                                        modeSwitch.getHeight()+5), 2)

def drawMenuButtons():  # zeichnet die Knöpfe links
    modeSwitch.draw(WINSURF)

def drawMenuButtonNames(namelist):  # zeichnet die Bezeichnungen der Knöpfe links
    for i in range(0, len(namelist), 2):
        WINSURF.blit(namelist[i], namelist[i+1])

def drawFractalGrid():  # zeichnet das Raster für den Fraktalmodus
    pygame.draw.rect(WINSURF, BLACK, (505, 55, 640, 640), 2)
    for i in range(1, 32):
        pygame.draw.line(WINSURF, BLACK, (505 + 20 * i, 55), (505 + 20 * i, 695))
    for i in range(1, 32):
        pygame.draw.line(WINSURF, BLACK, (505, 55 + i * 20), (1145, 55 + i * 20))



#---------------------------------------------andere Funktionen---------------------------------------------------------
def doEventHnadling(fracDict = None):  # durchführung des normalen event-handlings
    for event in pygame.event.get():
        if event.type == QUIT:  # normaler QUIT event check
            pygame.quit()
            sys.exit()
        updateMenuButtons(event)  # alle Menüknöpfe werden geupdated
        if FRACTALMODE:
            updateFracButtons(fracDict, event)


#-----------------------------------------------Abschluss---------------------------------------------------------------
if __name__ == '__main__':
    main()
