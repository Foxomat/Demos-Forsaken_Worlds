# Programm mit graficher Oberfläche zum erstellen von Instanzen für DEMOS
# by Foxomat

#-----------------------------------------------Imports-----------------------------------------------------------------
import pygame, sys, Buttons, TextBoxes
from pygame.locals import *

#----------------------------------------------Konstanten---------------------------------------------------------------
WINWIDTH = 1200
WINHEIGHT = 750

# Farben
BLACK = (0, 0, 0)  # Schwarz und weiß weden beim dark mode/theme getauscht
WHITE = (248, 248, 248)
GREY = (200, 200, 200)
RED = (230, 20, 20)

COLOR_n6 = (32, 0, 255)
COLOR_n5 = (0, 64, 255)
COLOR_n4 = (0, 128, 255)
COLOR_n3 = (0, 192, 255)
COLOR_n2 = (0, 255, 255)
COLOR_n1 = (0, 230, 115)
COLOR_0 = (0, 255, 0)
COLOR_1 = (168, 255, 0)
COLOR_2 = (255, 255, 0)
COLOR_3 = (255, 192, 16)
COLOR_4 = (255, 128, 12)
COLOR_5 = (255, 64, 8)
COLOR_6 = (255, 0, 0)
COLOR_7 = (255, 0, 85)
COLOR_8 = (255, 0, 170)
COLOR_9 = (216, 0, 255)

#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------------------Main-Methode--------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

def main():

#---------------------------------(Pygame-abhängige) Variablen und Zeugs------------------------------------------------
    global WINSURF  # Standard Display Surface
    global MENUBUTTON_FONT  # Schriftart

    global fractal_mode_button  # Knopf zum ändern von FRACTALMODE
    global FRACTALMODE  # Modus zum bearbeiten von Fractalmaps an/aus (sonst Instanzenmaps)
    global dark_theme_button  # Knopf für dunkles Thema
    global DARKMODE  # Modus für dunkles Thema als bool
    global height_select_textbox
    global drawing_height


    # klar
    pygame.init()
    CLOCK = pygame.time.Clock()
    WINSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    # kosmetisches Gedöns
    pygame.display.set_caption('Instanzenmanager')
    pygame.display.set_icon(pygame.image.load('ikoneEditor.gif'))

    # grundsätzliches Zeug
    FRACTALMODE = False  # siehe globals
    DARKMODE = False  # siehe globals
    drawing_height = 0
    MENUBUTTON_FONT = pygame.font.Font(None, 25)  # siehe globals


    # Buttons und Text Boxes
    # siehe globals
    fractal_mode_button = Buttons.DrawButton(25, 55, 'ButtonUnpressed.png', 'ButtonPressed.bmp', 'ButtonUnpressed.png')
    # siehe globals
    dark_theme_button = Buttons.DrawButton(25, 85, 'ButtonUnpressed.png', 'ButtonPressed.png', 'ButtonUnpressed.png')

    height_select_textbox = TextBoxes.NumberBox(395, 55, 30, 25, -64, 63)

    # Beschriftungen
    fractal_mode_txt_surf = MENUBUTTON_FONT.render("Fractal Editing", True, BLACK)  # Text surface
    fractal_mode_txt_rect = fractal_mode_txt_surf.get_rect()  # text rect zum blitten
    fractal_mode_txt_rect.topleft = (fractal_mode_button.get_x() + fractal_mode_button.get_width() + 15,
                                     fractal_mode_button.get_y())  #text rect kommt neben den zu beschriftenden Knopf

    dark_theme_txt_surf = MENUBUTTON_FONT.render("Dark Theme", True, BLACK)
    dark_theme_txt_rect = dark_theme_txt_surf.get_rect()
    dark_theme_txt_rect.topleft = (dark_theme_button.get_x() + dark_theme_button.get_width() + 15,
                                  dark_theme_button.get_y())


    height_select_txt_surf = MENUBUTTON_FONT.render("drawing height:", True, BLACK)
    height_select_txt_rect = height_select_txt_surf.get_rect()
    height_select_txt_rect.topright = (height_select_textbox.get_x() - 15, height_select_textbox.get_y())

    #Liste, in der alle surfaces und rects der Menüknöpfe sind, zum einfachen Blitten in einer Funktion
    Menu_Label_Dict = {('menu', 'surf', 0): fractal_mode_txt_surf, ('menu', 'rect', 0): fractal_mode_txt_rect,
                       ('menu', 'surf', 1): dark_theme_txt_surf,    ('menu', 'rect', 1): dark_theme_txt_rect,
                       ('frac', 'surf', 0): height_select_txt_surf, ('frac', 'rect', 0): height_select_txt_rect}

    # Dictionary, das die Knöpfe des Fractalrasters enthält, außerdem speichert es den Höhenwert pro Kästchen
    fracButtonsDict = {}
    for i in range(0, 32):
        for j in range(0, 32):
            value = Buttons.Button(505 + j*20, 55 + i*20)
            fracButtonsDict[(i, j, 'buttons')] = value  # Knopf Objekt
            fracButtonsDict[(i, j, 'height')] = '0'  # Höhe


#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------Main-Loop---------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
    while True:

#------------------------------------------Fractal-Mode-Loop------------------------------------------------------------
        while FRACTALMODE:
            drawBackground()  # Hintergrund, der immer gezeichnet wird (+rote Knopfumrandungen)

            doEventHnadling(fracButtonsDict)  # event Handling

            drawMenuButtonsAndBoxes()  # zeichnet alle Menüknöpfe (allgemein und fractal/instance)
            drawMenuLabels(Menu_Label_Dict)  # zeichnet die Beschriftungen für die Menüknöpfe

            drawFractalGrid()  # zeichnet 32x32 Raster für Fractalmaps

            drawFractalMap(fracButtonsDict)  # zeichnet und updatet Höhennummer ((x, y, 1) im Dict), zeichnet Farbe

            applyMenuOptions()  # setzt die Auswahl in den Menüknöpfen um


            CLOCK.tick()
            pygame.display.update()

#------------------------------------------Instanz-Mode-Loop------------------------------------------------------------

        while not FRACTALMODE:
            drawBackground()  # Hintergrund, der immer gezeichnet wird (+rote Knopfumrandungen)

            doEventHnadling()  # event Handling

            drawMenuButtonsAndBoxes()  # zeichnet alle Menüknöpfe und Textfelder
            drawMenuLabels(Menu_Label_Dict)  # zeichnet die Beschriftungen für die Menüknöpfe

            applyMenuOptions()  # setzt die Auswahl in den Menüknöpfen um


            CLOCK.tick()
            pygame.display.update()


#-----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------extra Methoden-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------


#-------------------------------------------generelle Funktionen--------------------------------------------------------
def doEventHnadling(fracDict = None):  # durchführung des normalen event-handlings
    for event in pygame.event.get():
        if event.type == QUIT:  # normaler QUIT event check
            pygame.quit()
            sys.exit()

        updateMenuButtonsAndBoxes(event)  # alle Menüknöpfe werden geupdated
        if FRACTALMODE:
            updateFracDict(fracDict, event)

def applyMenuOptions():
    global FRACTALMODE, DARKMODE, WHITE, BLACK, drawing_height  # globals müssen "aufgerufen werden", um in Funktionen
                                                # bearbeitet zu werden

    if fractal_mode_button.get_leftButtonPressed():  # Check, ob FRACTALMODE umgeschaltet werden soll
        FRACTALMODE = not FRACTALMODE

    if dark_theme_button.get_leftButtonPressed():  # Check, ob DARKMODE umgeschaltet werden soll
        DARKMODE = not DARKMODE
        placeholder = WHITE  # BLACK und WHITE werden durch Dreieckstausch getauscht
        WHITE = BLACK
        BLACK = placeholder

    if height_select_textbox.get_output_ready():
        drawing_height = height_select_textbox.get_output()


#-------------------------------------------update-Funktionen-----------------------------------------------------------
def updateMenuButtonsAndBoxes(event):  # updatet die Knöpfe links
    fractal_mode_button.update(event)
    dark_theme_button.update(event)

    if FRACTALMODE:
        height_select_textbox.update(event)

def updateFracDict(fracDict, event):  # updatet die Knöpfe des Fractalmap-Rasters
    for i in range(0, 32):
        for j in range(0, 32):
            fracDict[(j, i, 'buttons')].update(event)
            if fracDict[(j, i, 'buttons')].get_leftButtonDown():  # wenn Rasterknopf gedrückt:
                fracDict[(j, i, 'height')] = drawing_height



#--------------------------------------------draw-Funktionen------------------------------------------------------------
def drawBackground():  # zeichnet den Hintergrund, der immer da ist (+rote Knopfumrandungen)
    WINSURF.fill(WHITE)  # Hintergrundfarbe

    # Strukturlinien
    pygame.draw.line(WINSURF, BLACK, (0, 0), (WINWIDTH, 0))  # linie ganz oben
    pygame.draw.line(WINSURF, BLACK, (450, 0), (450, WINHEIGHT), 4)  # mittlere senkrechte Trennlinie
    pygame.draw.line(WINSURF, BLACK, (0, 45), (450,45))  # waagerechte Trennlinie oberhalb des Menüs
    pygame.draw.line(WINSURF, BLACK, (200, 45), (200, WINHEIGHT))  # senkrechte Trennlinie im Menü

    HEADLINE_FONT = pygame.font.Font(None, 45)
    HEADLINE_SURF = HEADLINE_FONT.render("MENU", True, BLACK)
    HEADLINE_RECT = HEADLINE_SURF.get_rect()
    HEADLINE_RECT.topleft = (60, 10)
    WINSURF.blit(HEADLINE_SURF, HEADLINE_RECT)

    # rote Knopfumrandung als Teil des Hintergrunds
    if DARKMODE:  # dark theme Umrandung
        pygame.draw.rect(WINSURF, RED, (dark_theme_button.get_x() - 3, dark_theme_button.get_y() - 3, dark_theme_button.get_width() + 5,
                                        dark_theme_button.get_height() + 5), 2)

    if FRACTALMODE:  # fractal editing Umrandung
        pygame.draw.rect(WINSURF, RED, (fractal_mode_button.get_x() - 3, fractal_mode_button.get_y() - 3, fractal_mode_button.get_width() + 5,
                                        fractal_mode_button.get_height() + 5), 2)

def drawMenuButtonsAndBoxes():  # zeichnet die Knöpfe links
    fractal_mode_button.draw(WINSURF)
    dark_theme_button.draw(WINSURF)

    if FRACTALMODE:
        height_select_textbox.draw(WINSURF)

def drawMenuLabels(labeldict):  # zeichnet die Bezeichnungen der Knöpfe links
    labeldict[('menu', 'surf', 0)] = MENUBUTTON_FONT.render("Fractal Editing", True, BLACK)  # updatet text surface objekte in der Liste wegen
    labeldict[('menu', 'surf', 1)] = MENUBUTTON_FONT.render("Dark Theme", True, BLACK)       # dark theme (BLACK-WHITE wechsel)
    for i in range(0, 2):  # Bezeichnungen hinschreiben
        WINSURF.blit(labeldict[('menu', 'surf', i)], labeldict[('menu', 'rect', i)])

    if FRACTALMODE:
        labeldict[('frac', 'surf', 0)] = MENUBUTTON_FONT.render("drawing height:", True, BLACK)
        for i in range(0, 1):
            WINSURF.blit(labeldict[('frac', 'surf', i)], labeldict[('frac', 'rect', i)])

def drawFractalGrid():  # zeichnet das Raster für den Fraktalmodus
    pygame.draw.rect(WINSURF, BLACK, (505, 55, 640, 640), 2)  # Kasten rundrum
    for i in range(1, 32):
        pygame.draw.line(WINSURF, BLACK, (505 + 20 * i, 55), (505 + 20 * i, 695))  # vertikale Linien
        pygame.draw.line(WINSURF, BLACK, (505, 55 + i * 20), (1145, 55 + i * 20))  # horizontale Linien

def drawFractalMap(fracDict):  # zeichnet und updatet Höhennummer ((x, y, 1) im Dict), malt Farbe im Raster
    font = pygame.font.Font(None, 30)  # Schrift für Höhenangabe

    for i in range(0, 32):
        for j in range(0, 32):  # höhenfarben malen
            if fracDict[(j, i, 'height')] == 'w':
                pygame.draw.rect(WINSURF, BLACK, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == 'p':
                pygame.draw.rect(WINSURF, WHITE, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '-6':
                pygame.draw.rect(WINSURF, COLOR_n6, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '-5':
                pygame.draw.rect(WINSURF, COLOR_n5, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '-4':
                pygame.draw.rect(WINSURF, COLOR_n4, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '-3':
                pygame.draw.rect(WINSURF, COLOR_n3, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '-2':
                pygame.draw.rect(WINSURF, COLOR_n2, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '-1':
                pygame.draw.rect(WINSURF, COLOR_n1, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '0':
                pygame.draw.rect(WINSURF, COLOR_0, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '1':
                pygame.draw.rect(WINSURF, COLOR_1, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '2':
                pygame.draw.rect(WINSURF, COLOR_2, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '3':
                pygame.draw.rect(WINSURF, COLOR_3, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '4':
                pygame.draw.rect(WINSURF, COLOR_4, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '5':
                pygame.draw.rect(WINSURF, COLOR_5, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '6':
                pygame.draw.rect(WINSURF, COLOR_6, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '7':
                pygame.draw.rect(WINSURF, COLOR_7, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '8':
                pygame.draw.rect(WINSURF, COLOR_8, (506 + i * 20, 56 + j * 20, 19, 19))
            if fracDict[(j, i, 'height')] == '9':
                pygame.draw.rect(WINSURF, COLOR_9, (506 + i * 20, 56 + j * 20, 19, 19))


            if fracDict[(j, i, 'buttons')].get_buttonHovered():  # wenn Cursor über Rasterknopf:
                DrawSurf = font.render(str(fracDict[(j, i, 'height')]), True, RED)  # Höhenzahl in rot
                DrawRect = DrawSurf.get_rect()  # Höhenzahl Textrect
                DrawRect.topleft = (505 + i*20, 57 + j*20)  # Textrect anpassung an Kästchen
                WINSURF.blit(DrawSurf, DrawRect)  # anzeigen der Höhenzahl

#-----------------------------------------------Abschluss---------------------------------------------------------------
if __name__ == '__main__':
    main()
