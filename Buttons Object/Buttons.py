# Knopf Klasse für vielfältig einsetzbare Knöpfe mit oder ohne draw Funktion
# by Foxomat

#-----------------------------------------------Imports-----------------------------------------------------------------
import pygame, sys
from pygame.locals import *

#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------------------die Klasse----------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

class Button:
    """Ein Knopf-Objekt."""

#-----------------------------------------------init--------------------------------------------------------------------

    def __init__(self, x, y):
        self.x = x  # x und y position (linke obere ecke)
        self.y = y
        self.width = 20  # standartisierte Knopfgröße
        self.height = 20
        self.buttonRect = Rect(self.x, self.y, self.width, self.height)  # Hitbox als Rechteck
        self.buttonHovered = False  # Cursor ist über Knopf
        self.buttonDown = False  # Knopf ist runtergedrückt
        self.buttonPressed = False  # Knopf wurde losgelassen -> ausgelöst


#-------------------------------------kleine Implementationshilfe-------------------------------------------------------

    # einzeichnen der Hitbox auf Oberfläche
    def drawHitbox(self, surf):
        pygame.draw.rect(surf, (0, 0, 0), self.buttonRect, 1)
        pygame.draw.rect(surf, (180, 0, 0), (self.x + 1, self.y + 1, self.width - 2, self.height - 2), 1)


#-----------------------------------------update-Funktionen-------------------------------------------------------------

    # eine Funktion, die ins event-handling kommt, damit Mausdaten aktuell sind
    def update(self, event):
        self.__updateButtonHovered(event)
        self.__updateButtonDown(event)
        self.__updateButtonPressed(event)

    # updated den self.buttonHovered boolean
    def __updateButtonHovered(self, event):
        if event.type == MOUSEMOTION or event.type == MOUSEBUTTONUP or event.type == MOUSEBUTTONDOWN:
            if self.buttonRect.collidepoint(event.pos):
                self.buttonHovered = True
            else:
                self.buttonHovered = False
            return self.buttonHovered

    # updated den self.buttonDown boolean
    def __updateButtonDown(self, event):
        if event.type == MOUSEBUTTONDOWN or (event.type == MOUSEMOTION and event.buttons[0] == 1):
            if self.__updateButtonHovered(event):
                self.buttonDown = True
        else:
            self.buttonDown = False
        return self.buttonDown

    # updated den self.buttonPressed boolean
    def __updateButtonPressed(self, event):
        if event.type == MOUSEBUTTONUP:
            if self.__updateButtonHovered(event):
                self.buttonPressed = True
        else:
            self.buttonPressed = False
        return self.buttonPressed


#-----------------------------------------getter und setter-------------------------------------------------------------

    # rekalibrierung der Hitbox
    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height
        self.buttonRect = Rect(self.x, self.y, self.width, self.height)

    # klar
    def getButtonHovered(self):
        return self.buttonHovered

    # klar
    def getButtonDown(self):
        return self.buttonDown

    # gibt zurück, ob der Knopf aktiviert wurde. Der Variablentausch und das False setzen ist notwendig, da sonst wenn
    # kein neues event generiert wird, der knopf immer aktiviert bleibt. Knopf aktivieren soll immer nur 1 tick sein.
    def getButtonPressed(self):
        placeholder = self.buttonPressed
        self.buttonPressed = False
        return placeholder



#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------zweite init (extended klasse)-------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------


# diese Klasse hat Animationen, die der Knopf zeichnet, wenn der curser über ihm ist bzw wenn der knopf runtergedrückt
# ist. Sie werden der Klassse übergeben und sie zeichnet sie selbst.
class DrawButton(Button):
    def __init__(self, x, y, imageOne, imageTwo, imageThree = 0):
        self.x = x  # x und y position (linke obere ecke)
        self.y = y
        self.imageOne = pygame.image.load(imageOne)  # Bild, das erscheint, wenn der Cursor über dem Knopf ist
        self.imageTwo = pygame.image.load(imageTwo)  # Bild, das erscheint, wenn der Knopf runtergedrückt ist
        if imageThree == 0:
            self.imageThree = pygame.Surface((0, 0))  # kein Standardbild übergeben -> zeichne später leere Surface
        else:
            self.imageThree = pygame.image.load(imageThree)  # Standardbild des Knopfes

        self.width = 20
        self.height = 20
        self.buttonRect = Rect(self.x, self.y, self.width, self.height)
        self.buttonHovered = False
        self.buttonDown = False
        self.buttonPressed = False


#----------------------------------------------draw-Funktionen----------------------------------------------------------

    # eine draw-Funktion für alles, um das Hauptprogramm klein und übersichtlich zu halten
    def draw(self, surf):
        self.__drawMouseOverButton(surf)
        self.__drawButtonDown(surf)
        self.__drawDefault(surf)

    # zeichnet das entsprechende Bild, wenn der Cursor über dem Knopf ist
    def __drawMouseOverButton(self, surf):
        if self.buttonHovered:
            surf.blit(self.imageOne, self.buttonRect)
            return True
        else:
            return False
    # zeichnet das entsprechende Bild, wenn der Knopf runtergedrückt ist
    def __drawButtonDown(self, surf):
        if self.buttonDown:
            surf.blit(self.imageTwo, self.buttonRect)
            return True
        else:
            return False

    # zeichnet das Standardbild des Knopfes, nichts passiert
    def __drawDefault(self, surf):
        if self.buttonDown or self.buttonHovered:
            return False
        else:
            surf.blit(self.imageThree, self.buttonRect)
