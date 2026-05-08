import pygame.font

class Button:
    """Eine Klasse fuer die Buttons im Spiel"""

    def __init__(self, rs_spiel, msg):
        """Initialize button attributes"""
        self.screen = rs_spiel.screen
        self.screen_rect = rs_spiel.screen.get_rect()

        # Legt die Abmessungen und Eigenschaften der Schaltflaeche fest.
        self.width, self.height = 200, 50
        self.button_color = (0,135,0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Erstellt das rect-Object der Schaltflaeche und zentriert es.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Der Schaltflaechentext muss nur einmal eingerichtet werden.
        self._prep_msg(msg)
    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    def draw_button(self):
        """Zeichnet eine leere Schaltflaeche und dann den Text"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)