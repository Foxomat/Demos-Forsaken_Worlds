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
        self.rect = Rect(self.x, self.y, self.width, self.height)  # Hitbox als Rechteck
        self.hovered = False  # Cursor ist über Knopf
        self.left_mouse_down = False  # Knopf ist runtergedrückt
        self.__left_mouse_pressed = False  # Knopf wurde losgelassen -> ausgelöst
        self.right_mouse_down = False  # Knopf ist runtergedrückt
        self.__right_mouse_pressed = False  # Knopf wurde losgelassen -> ausgelöst


#-------------------------------------kleine Implementationshilfe-------------------------------------------------------

    # einzeichnen der Hitbox auf Oberfläche
    def draw_hitbox(self, surf):
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 1)
        pygame.draw.rect(surf, (180, 0, 0), (self.x + 1, self.y + 1, self.width - 2, self.height - 2), 1)


#-----------------------------------------update-Funktionen-------------------------------------------------------------

    # eine Funktion, die ins event-handling kommt, damit Mausdaten aktuell sind
    def update(self, event):
        self.__update_button_hovered(event)
        self.__update_left_mouse_down(event)
        self.__update_left_mouse_pressed(event)

    # updated den self.hovered boolean
    def __update_button_hovered(self, event):
        if event.type == MOUSEMOTION or event.type == MOUSEBUTTONUP or event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.hovered = True
            else:
                self.hovered = False
            return self.hovered

    # updated den self.buttonDown boolean
    def __update_left_mouse_down(self, event):
        if (event.type == MOUSEBUTTONDOWN and event.button == 1) or (event.type == MOUSEMOTION and
                                                                     event.buttons[0] == 1):
            if self.__update_button_hovered(event):
                self.left_mouse_down = True
        else:
            self.left_mouse_down = False
        return self.left_mouse_down

    def __update_right_mouse_down(self, event):
        if (event.type == MOUSEBUTTONDOWN and event.button == 2) or (event.type == MOUSEMOTION and
                                                                     event.buttons[0] == 1):
            if self.__update_button_hovered(event):
                self.left_mouse_down = True
        else:
            self.left_mouse_down = False
        return self.left_mouse_down

    # updated den self.buttonPressed boolean
    def __update_left_mouse_pressed(self, event):
        if event.type == MOUSEBUTTONUP and event.button == 1:
            if self.__update_button_hovered(event):
                self.__left_mouse_pressed = True
        else:
            self.__left_mouse_pressed = False
        return self.__left_mouse_pressed

    def __update_right_mouse_pressed(self, event):
        if event.type == MOUSEBUTTONUP and event.button == 2:
            if self.__update_button_hovered(event):
                self.__left_mouse_pressed = True
        else:
            self.__left_mouse_pressed = False
        return self.__left_mouse_pressed


#-----------------------------------------getter und setter-------------------------------------------------------------


    # gibt zurück, ob der Knopf aktiviert wurde. Der Variablentausch und das False setzen ist notwendig, da sonst wenn
    # kein neues event generiert wird, der knopf immer aktiviert bleibt. Knopf aktivieren soll immer nur 1 tick sein.
    def get_left_mouse_pressed(self):
        placeholder = self.__left_mouse_pressed
        self.__left_mouse_pressed = False
        return placeholder

    def get_right_mouse_pressed(self):
        placeholder = self.__right_mouse_pressed
        self.__right_mouse_pressed = False
        return placeholder

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    # rekalibrierung der Hitbox
    def set_widthHeight(self, width, height):
        self.width = width
        self.height = height
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def set_xy(self, x, y):
        self.x = x
        self.y = y


#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------zweite init (extended klasse)-------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------


# diese Klasse hat Animationen, die der Knopf zeichnet, wenn der curser über ihm ist bzw wenn der knopf runtergedrückt
# ist. Sie werden der Klassse übergeben und sie zeichnet sie selbst.
class DrawButton(Button):
    def __init__(self, x, y, imageOne, imageTwo, imageThree = 0):
        Button.__init__(self, x, y)
        self.imageOne = pygame.image.load(imageOne)  # Bild, das erscheint, wenn der Cursor über dem Knopf ist
        self.imageTwo = pygame.image.load(imageTwo)  # Bild, das erscheint, wenn der Knopf runtergedrückt ist
        if imageThree == 0:
            self.imageThree = pygame.Surface((0, 0))  # kein Standardbild übergeben -> zeichne später leere Surface
        else:
            self.imageThree = pygame.image.load(imageThree)  # Standardbild des Knopfes

#----------------------------------------------draw-Funktionen----------------------------------------------------------

    # eine draw-Funktion für alles, um das Hauptprogramm klein und übersichtlich zu halten
    def draw(self, surf):
        self.__draw_hovered(surf)
        self.__draw_left_mouse_down(surf)
        self.__draw_default(surf)

    # zeichnet das entsprechende Bild, wenn der Cursor über dem Knopf ist
    def __draw_hovered(self, surf):
        if self.hovered and not self.left_mouse_down:
            surf.blit(self.imageOne, self.rect)
            return True
        else:
            return False
    # zeichnet das entsprechende Bild, wenn der Knopf runtergedrückt ist
    def __draw_left_mouse_down(self, surf):
        if self.left_mouse_down:
            surf.blit(self.imageTwo, self.rect)
            return True
        else:
            return False

    # zeichnet das Standardbild des Knopfes, nichts passiert
    def __draw_default(self, surf):
        if self.left_mouse_down or self.hovered:
            return False
        else:
            surf.blit(self.imageThree, self.rect)
