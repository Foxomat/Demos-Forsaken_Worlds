import pygame, sys
from pygame.locals import *


class Button:
    """Ein Knopf-Objekt."""

    def __init__(self, x, y):
        self.x = x  # x und y position (linke obere ecke)
        self.y = y
        self.width = 100
        self.height = 20
        self.buttonRect = Rect(self.x, self.y, self.width, self.height)
        self.buttonHovered = False

    def drawHitbox(self, surf):
        pygame.draw.rect(surf, (0, 0, 0), self.buttonRect, 1)
        pygame.draw.rect(surf, (180, 0, 0), (self.x + 1, self.y + 1, self.width - 2, self.height - 2), 1)

    def mouseOverButton(self, event):
        if event.type == MOUSEMOTION or event.type == MOUSEBUTTONUP or event.type == MOUSEBUTTONDOWN:
            if self.buttonRect.collidepoint(event.pos):
                self.buttonHovered = True
                return True
            else:
                self.buttonHovered = False
                return False

    def buttonDown(self, event):
        if event.type == MOUSEBUTTONDOWN or event.buttons(0) == 1:
            if self.mouseOverButton(event):
                return True
            else:
                return False

    def buttonPressed(self, event):
        if event.type == MOUSEBUTTONUP and self.mouseOverButton(event):
            return True
        else:
            return False

    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height
        self.buttonRect = Rect(self.x, self.y, self.width, self.height)


#-----------------------------------------------------------------------------------------------------------------------
#-------------------------------extended self-drawing buttons-----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

class DrawButton(Button):
    def __init__(self, x, y, imageOne, imageTwo):
        self.x = x  # x und y position (linke obere ecke)
        self.y = y
        self.imageOne = imageOne + ".gif"
        self.imageOne = pygame.image.load(self.imageOne)
        self.imageTwo = imageTwo + ".gif"
        self.imageTwo = pygame.image.load(self.imageTwo)
        self.width = 100
        self.height = 20
        self.buttonRect = Rect(self.x, self.y, self.width, self.height)
        self.buttonHovered = False

    def drawMouseOverButton(self, surf, event):
        if self.mouseOverButton(event):
            surf.blit(self.imageOne, self.buttonRect)
            return True
        else:
            return False

    def drawButtonDown(self, surf, event):
        if self.buttonDown(event):
            surf.blit(self.imageTwo, self.buttonRect)
            return True
        else:
            return False
