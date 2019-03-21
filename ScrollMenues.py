# Scroll Menü Klasse - klick auf titel -> feld mit auswahlmöglichkeiten öffnet sich -> runter scrollen möglich
# by Foxomat

#-----------------------------------------------Imports-----------------------------------------------------------------
import pygame
from pygame.locals import *

#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------------------die Klasse----------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

class ScrollMenu:
    """Ein Scroll-Menü-Objekt."""

#--------------------------------------------------init-----------------------------------------------------------------

    def __init__(self, title, title_rect):  # title_rect ist rect object
        self.active = False  # bool, ob scroll-menü angeklickt
        self.rect = title_rect  # rect um das Titelfeld
        self.selection = title + '...'  # was anfangs im rect steht (wird später unwiderruflich durch die Auswahl ersetzt)

        self.scrolldown = 0
        self.entry_area_size = 5
        self.entry_list = []  # liste von Auswahlmöglichkeiten als Liste von Listen der art [entry, button-objekt]
        self.entry_surf = pygame.Surface((self.rect.width, self.rect.height))  # surface, auf der alle entries ab-
        self.WIN_blit_rect = Rect(self.rect.x, self.rect.y + self.rect.height + 1,               # gebildet werden
                                  self.rect.width, self.rect.height * self.entry_area_size)  # rect unterhalb des
                                                                                        # Titelfeldes, das
                                                                                # 5x so hoch ist (5 entries platz hat)


#-------------------------------------------------Funktionen------------------------------------------------------------
    # Funktion zum hinzufürgen von entries
    def add(self, entry):
        rect = Rect(0, 0, self.rect.width, self.rect.height)

        self.entry_list.append([entry, rect, False])
        self.entry_list.sort()  # entries alphabetisch ordnen

        # größe von self.entry_surf anpassen, damit alle entries draufpassen
        self.entry_surf = pygame.Surface((self.rect.width, self.rect.height * len(self.entry_list)))

    # Funktion zum entfernen von entries
    def delete(self, entry):
        for i in range(0, len(self.entry_list)):  # checkt jeden entry auf übereinstimmung
            if self.entry_list[i][0] == entry:
                del self.entry_list[i]  # wenn gefunden dann löschen
                self.entry_surf = pygame.Surface((self.rect.width, self.rect.height * len(self.entry_list)))  # wie oben
                return True
        print("error: entry_list does not contain item \"" + entry + "\".")  # entry nicht gefunden
        return False


#------------------------------------------------draw-Funktionen--------------------------------------------------------

    # Methode zum Zeichnen des ganzen Objekts
    def draw(self, surf):
        self.__draw_title_box(surf)  # Zeichnet Titelfeld
        self.__draw_selection(surf)  # schreibt titel bzw Auswahl

        if self.active:  # wenn angeklickt, dann entries anzeigen
            self.__draw_entry_list(surf)
            self.__draw_entry_borders(surf)

    # Funktion zum Zeichnen des Titelfelds
    def __draw_title_box(self, surf):
        pygame.draw.rect(surf, (255, 255, 255), self.rect)  # weißer Hintergrund

        # Pfeil am rechten ende der Box (angepasst an Grüße
        p1 = (self.rect.right - int(self.rect.width/20), self.rect.top + int(self.rect.height/6))
        p2 = (p1[0] - int(self.rect.height/1.5), p1[1])
        p3 = ((p1[0]+p2[0])/2, self.rect.bottom - int(self.rect.height/6))
        pygame.draw.polygon(surf, (0, 0, 0), (p1, p2, p3))

        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)  # Ramen um Titelfeld

    # Funktion, die anfänglichen titel schreibt
    def __draw_selection(self, surf):
        font = pygame.font.Font(None, int(1.3 * self.rect.height))  # schriftgröße angepasst an Boxhöhe
        title_surf = font.render(self.selection, True, (0, 0, 0))
        text_rect = Rect(self.rect.x+4, self.rect.y+self.rect.height/16, self.rect.width-4, self.rect.height-4)
        surf.blit(title_surf, text_rect)

    # Funktionen zum Zeichnen der Liste der entries (max 5 uf einmal) unterm titelfeld
    def __draw_entry_list(self, surf):
        # Oberfläche zum "ausschneiden" von 5 entries
        WIN_blit_surf = pygame.Surface((self.rect.width, self.rect.height * self.entry_area_size))
        font = pygame.font.Font(None, int(1.3 * self.rect.height))
        self.entry_surf.fill((255, 255, 255))  # hintergrund weiß

        for i in range(0, len(self.entry_list)):  # für jeden Listeneintrag:
            entry = font.render(self.entry_list[i][0], True, (0, 0, 0))
            text_rect = Rect(4, i *self.rect.height + self.rect.height / 16,  # rect zum blitten für jeden entry
                             self.rect.width - 4, self.rect.height - 4)
            rect = (0, i*self.rect.height, self.rect.width, self.rect.height)  # rect für Ramen um jeden entry

            self.entry_surf.blit(entry, text_rect)  # entry string blitten
            pygame.draw.rect(self.entry_surf, (0, 0, 0), rect, 1)  # ramen um entry

        WIN_blit_surf.blit(self.entry_surf, (0, self.scrolldown))  # 5 entries "ausschneiden"
        surf.blit(WIN_blit_surf, self.WIN_blit_rect)  # 5 entries auf win surf blitten

    def __draw_entry_borders(self, surf):
        for i in range(0, len(self.entry_list)):
            if self.entry_list[i][2]:
                pygame.draw.rect(surf, (50, 150, 200), self.entry_list[i][1], 4)

#--------------------------------------------------update-Funktionen----------------------------------------------------

    # große Methode zum updaten
    def update(self, event):
        if self.active:
            self.__update_selection(event)
            self.__update_rects(event)
            self.__update_entry_area(event)

        self.__update_active(event)

    # updatet den self.active bool bei klick auf titelfeld bzw daneben
    def __update_active(self, event):
        if event.type == MOUSEBUTTONUP and (event.button in (1, 2, 3)):
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

    # updatet die entry rects
    def __update_rects(self, event):
        for i in range(0, len(self.entry_list)):
            # update rect pos
            self.entry_list[i][1].y = i * self.rect.height + self.scrolldown
            self.entry_list[i][1].y += self.rect.y + self.rect.height
            self.entry_list[i][1].x = self.rect.x

            # update rect hovered
            if event.type == MOUSEMOTION or event.type == MOUSEBUTTONUP or event.type == MOUSEBUTTONDOWN:
                if self.WIN_blit_rect.collidepoint(event.pos) and self.entry_list[i][1].collidepoint(event.pos):
                    self.entry_list[i][2] = True
                else:
                    self.entry_list[i][2] = False

    # updatet die zu zeigenden entries (den ausschnitt)
    def __update_entry_area(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 4:
            if self.scrolldown < 0:
                self.scrolldown += self.rect.height

        max_scrolldown = (self.rect.height)*len(self.entry_list)  # größe aller entries untereinander
        max_scrolldown -= (self.rect.height) * self.entry_area_size  # abzüglich der größe des sichtfensters
        max_scrolldown = -max_scrolldown  # ins negative kehren (scroll nach unten bewegt ausschneidesurface nach oben
        if event.type == MOUSEBUTTONDOWN and event.button == 5:
            if self.scrolldown > max_scrolldown:
                self.scrolldown -= self.rect.height

    def __update_selection(self, event):
        if event.type == MOUSEBUTTONUP and event.button == 1:
            for i in range(0, len(self.entry_list)):
                if self.entry_list[i][2]:
                    self.selection = self.entry_list[i][0]
                    return
