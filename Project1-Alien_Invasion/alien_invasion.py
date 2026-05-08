import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        
        self.clock = pygame.time.Clock()#FPS
        self.settings = Settings()


        #self.screen = pygame.display.set_mode((0,0,pygame.FULLSCREEN))
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        # Bildet eine Instanz, um Spielstatistiken zu speichern und eine
        # Anzeigetafel zu erstellen.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # Erstellt eine Instanz zum Speichern der Spielstatistiken.
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.create_fleet()
        # Erstellt die Play-Schaltflaeche
        self.play_button = Button(self, "Play")
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            #Lauscht auf Tastatur- und Mausereignisse
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)
    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Aktualisiert die Geschosspositionen.
        self.bullets.update()
            # Entfernt die verschwunden Geschosse.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()
    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions."""
        # Entfernt alle kollidierten Geschosse und Invasionsschiffe.
        collisions = pygame.sprite.groupcollide(
            self.aliens, self.bullets, True, True)
        if not self.aliens:
            # Zerstort vorhandene Geschosse und erstellt eine neune Flotte.
            self.bullets.empty()
            self.create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
    def create_fleet(self):
        """Create the fleet of aliens"""
        # Ein Alien erzeugen nd weitere hinzufuegen, bis kein Platz mehr.
        # Abstand entspricht einer Alien-Breite
        # Spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_aliens(current_x,current_y)
                current_x += 2 * alien_width
        # Finised a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height
    def _create_aliens(self, x_position, y_position):
        """Create an alien and place it in the row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self._check_fleet_edges()
        self.aliens.update()

        # Prueft auf Kollisionen zwischen Invasoren und dem eigenen Schiff
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Prueft auf Invasoren, die den unteren Bildschirmrand erreichen
        self._check_aliens_bottom()
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Verringert die Anzahl der verbleibenden Schiffe.
            self.stats.ships_left -= 1

            # Entfernt alle verbliebenen Invasionsschiffe und Geschosse
            self.bullets.empty()
            self.aliens.empty()

            # Erstellt eine neue Flotte und zentriert das eigene Schiff
            self.create_fleet()
            self.ship.center_ship()

            # Haelt das Spiel kurz an
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Gleiche Reaktion wie bei einer Kollision mit dem Schiff
                self._ship_hit()
                break
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Setzt die Spieleinstellungen zurueck.
            self.settings.initialize_dynamic_settings()
            # Setzt die Spielstatistiken zurueck.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.stats.game_active = True

            # Entfernt die verbliebenen Invasionsschiffe und Geschosse
            self.aliens.empty()
            self.bullets.empty()

            # Erstellt eine neue Flotte und zentriert das eigene Schiff
            self.create_fleet()
            self.ship.center_ship()

            # Blendet den Mauszeiger aus.
            pygame.mouse.set_visible(False)
    def _start_game(self):
        if not self.stats.game_active:
            self.stats.reset_stats
            self.stats.game_active = True

            self.aliens.empty()
            self.bullets.empty()

            self.create_fleet()
            self.ship.center_ship
    def _update_screen(self):
        """Upadate images (including filling background color) on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Zeichnet die Informationen ueber den Punktestand.
        self.sb.show_score()
        # Zeichnet die Play-Schaltflaeche nur bei inaktivem Spiel.
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()
if __name__ == '__main__':
    #Erstellt eine Spielinstanz und führt das Spiel aus
    ai = AlienInvasion()
    ai.run_game()
