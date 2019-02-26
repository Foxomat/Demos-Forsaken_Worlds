import pygame, sys
from pygame.locals import *


class Button:
    """Ein Knopf-Objekt."""

    defaultWidth = 100
    defaultHeight = 20

    def __init__(self, x, y, name):
        self.x = x  # x und y position (linke obere ecke)
        self.y = y
        self.name = name  # name des Knopfes
        self.width = 100  # breite und höhe des knopfes
        self.height = 20
        self.color = (180, 180, 180)  # knopf ist grau
        self.font = pygame.font.SysFont('Consolas', 12)  # Schriftart des Knopfes
        self.borderColor = (15, 15, 15)  # randfarbe
        self.fontColor = (0, 0, 0)  # textfarbe
        self.mouseDown = False
        self.mousex = -10
        self.mousey = -10
        self.__update()

    def blit(self, surface):
        self.__update()
        surface.blit(self.surf, (self.x, self.y))

    def __update(self):
        self.surf = pygame.Surface((self.width, self.height))  # aktualisiere Breite/Höhe
        self.surf.fill(self.color)  # aktualisiere Farbe

        if self.buttonPressed():
             # Knopf runtergedrückt Ramen
            pygame.draw.rect(self.surf, self.borderColor, (1, 1, self.width + 2, self.height + 2), 2)
        else:
            pygame.draw.rect(self.surf, self.borderColor, (-1, -1, self.width, self.height), 2)  # normaler Ramen

        self.nameText = self.font.render(self.name, True, self.fontColor)  # was auf dem Knopf steht aktualisieren

        self.nameRect = self.nameText.get_rect()  # Textrechteck aktualisieren
        self.nameRect.centerx = self.surf.get_rect().centerx
        self.nameRect.centery = self.surf.get_rect().centery

        self.surf.blit(self.nameText, self.nameRect)

    def __buttonPressed(self):
        mousex, mousey = self.__getMousePos()
        self.__mouseDownTest()
        surfRect = pygame.Rect(self.x, self.y, self.width, self.height)

        if surfRect.collidepoint(mousex, mousey) and self.mouseDown:
            return True
        else:
            return False

    def __mouseDownTest(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                self.mouseDown = True
            if event.type == MOUSEBUTTONUP:
                self.mouseDown = False
            pygame.event.post(event)


    def __getMousePos(self):

        for event in pygame.event.get():
            if event.type == MOUSEMOTION or event.type == MOUSEBUTTONUP or event.type == MOUSEBUTTONDOWN:
                self.mousex, self.mousey = event.pos
            pygame.event.post(event)
        return self.mousex, self.mousey


    def setSize(self, width, height):
        self.width = width
        self.height = height
        self.__update()

    def setFont(self, fontSize, fontColor = (15, 15, 15), fontStyle = None):

        self.font = pygame.font.SysFont(fontStyle, fontSize)
        self.fontColor = fontColor
        self.__update()

    def setColor(self, color, borderColor = (15, 15, 15)):
        self.color = color
        self.borderColor = borderColor
        self.__update()
