# Textfeld Klasse für Textfelder, in die man Sachen eingeben kann
# by Foxomat

#-----------------------------------------------Imports-----------------------------------------------------------------
import pygame, sys
from pygame.locals import *

#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------------------die Klasse----------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

class TextBox:


#------------------------------------------------init-------------------------------------------------------------------
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
        self.text_size = height - 2
        self.text_color = (0, 0, 0)
        self.bg_color = (180, 180, 230)
        self.inactive_border_color = (50, 50, 110, 130)
        self.active_border_color = (100, 100, 160, 130)
        self.active = False
        self.FONT = pygame.font.Font(None, self.text_size)
        self.text = ''
        self.text_surf = self.FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = (self.rect.x + 5, self.rect.centery)
        self.output_string = ''
        self.output_ready = False

#---------------------------------------------Funktionen----------------------------------------------------------------
    def draw(self, surf):
        pygame.draw.rect(surf, self.bg_color, self.rect)
        if self.active:
            pygame.draw.rect(surf, self.inactive_border_color, self.rect, 2)
        else:
            pygame.draw.rect(surf, self.active_border_color, self.rect, 2)
        surf.blit(self.text_surf, self.text_rect)

    def update(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if self.active:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.output_string = self.text
                    self.output_ready = True
                    self.text = ''
                elif event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.text_surf = self.FONT.render(self.text, True, self.text_color)


#-----------------------------------------getter und setter-------------------------------------------------------------
    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_output_ready(self):
        placeholder = self.output_ready
        self.output_ready = False
        return placeholder

    def get_output(self):
        return self.output_string


    def set_properties(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)

    def set_colors(self, bg, activeborder, inactiveborder, text):
        self.bg_color = bg
        self.active_border_color = activeborder
        self.inactive_border_color = inactiveborder
        self.text_color = text

#-----------------------------------------------------------------------------------------------------------------------
#------------------------------------------extended class---------------------------------------------------------------
class NumberBox(TextBox):
    def __init__(self, x, y, width, height, min=-sys.maxsize, max=sys.maxsize):
        TextBox.__init__(self, x, y, width, height)
        self.min = min
        self.max = max
        self.error = 0

    def draw(self, surf):
        pygame.draw.rect(surf, self.bg_color, self.rect)
        if self.active:
            pygame.draw.rect(surf, self.inactive_border_color, self.rect, 2)
        else:
            pygame.draw.rect(surf, self.active_border_color, self.rect, 2)
        surf.blit(self.text_surf, self.text_rect)

        if self.error > 0:
            font = pygame.font.Font(None, 15)
            text = font.render('enter only ' + str(self.min) + '...' + str(self.max), True, (230, 10, 10))
            surf.blit(text, (self.rect.left, self.rect.bottom + 2))
            self.error -= 1


    def update(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if self.active:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.output_string = self.text
                    self.output_ready = True
                    # self.text = ''
                elif event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    if int(self.text + event.unicode) <= self.max and int(self.text + event.unicode) >= self.min:
                        self.text += event.unicode
                    else:
                        self.error = 250
                elif event.unicode == '-' and self.text == '':
                    self.text += event.unicode
                else:
                    self.error = 300
                self.text_surf = self.FONT.render(self.text, True, self.text_color)

