import sys
from random import randint
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from settings import Settings
from ship import Ship
from stars import Star


class AlienInvsion:
    """ Загальний класс, що керує ресурсами та поведімкою гри """

    def __init__(self):
        """ Ініціалізувати гру, створити ресурси гри """
        pygame.init()

        # settings
        self.settings = Settings()

        # screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Створити екземпляр для збереження ігрової статистики
        self.stats = GameStats(self)

        # ship
        self.ship = Ship(self)

        # bullet
        self.bullets = pygame.sprite.Group()

        # aliens
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # stars
        self.stars = pygame.sprite.Group()
        self._create_stars()

        # rains
        # self.rains = pygame.sprite.Group()
        # self._create_rains()

        # Створити кнопку Play
        self.play_button = Button(self, "Play")

    # ----------------------------------------------------------

    def run_game(self):
        """ Розпочати головний цикл гри. """
        while True:

            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_stars()
                # self._update_rains()

            self._update_screen()

    # -----------------------------------------------------------

    def _check_events(self):
        """ Реагувати на натискання клавіш та події миші """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """ Реагувати на натискання клавіш """
        # ship
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # quit
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """ Реагувати коли клавіша не натиснута """
        # ship
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # --------------------------------------------------------------------------

    def _fire_bullet(self):
        """ Створити нову кулю та додати її до до групи куль """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Оновити позицію куль та позбавитися старих куль. """

        # Оновити позиції куль.
        self.bullets.update()

        # Позбавитись куль що зникли
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Реакція на зіткнення куль з прибульцями. """

        # Видалити всі кулі та прибульців, що зіткнулися.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Знищити наяві кулі та створити новий флот
            self.bullets.empty()

            self._create_fleet()

            self.settings.change_background()
            self.settings.change_bullets_speed()
            self.settings.change_ship_speed()
            self.settings.change_alien_speed()

            self._create_stars()

    # -----------------------------------------------------------------------------

    def _create_fleet(self):
        """ Створити флот прибульців """
        # Створити прибульців та визначити кількість прибульців у ряду.
        # Відстань між прибульцями дорівнює ширині одного прибульця.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avialable_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avialable_space_x // (2 * alien_width)

        # Визначити, яка кількусть рядів прибульців поміщаеється на екрані.
        ship_height = self.ship.rect.height
        avialable_space_y = (self.settings.screen_height - (3 * alien_height) - (2 * ship_height))
        number_rows = avialable_space_y // (2 * alien_height)

        # Створити повний флот прибульців
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """ Створити прибульця та поставити його до ряду """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """ Перевірити, чи флот знаходится на краю, тоді оновити позиції всіх прибульців у флоті """
        self._check_fleet_edges()
        self.aliens.update()

        # Шукати зіткнення куль із прибульцями
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print("Ship hit!!!")
            self._ship_hit()

        # Шукати, чи котрийсь із прибульців досяг нижнього краю екрана.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """ Реагує відповідно до того, чи досяг котрийсь зі прибульців краю екрана. """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Спуск всього флоту та зміна його напрямку. """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """ Перевірити, чи не досяг якийсь прибулець нижнього краю екрана. """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Зреагувати так, ніби корабель було підбито
                self._ship_hit()
                break

    def _ship_hit(self):
        """ Реагувати на зіткнення прибульця з кораблем """

        if self.stats.ships_left > 0:
            # Зменшити ships_left.
            self.stats.ships_left -= 1

            # Позбавитися надлишку прибульців та куль
            self.aliens.empty()
            self.bullets.empty()

            # Створити новий флот та відцентрувати корабель.
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False

    # ----------------------------------------------------------------------------------

    def _create_stars(self):
        """ Створити зіркове небо """
        star = Star(self)
        star_width, star_height = star.rect.size
        avialable_space_x = self.settings.screen_width - (2 * star_width)
        number_star_x = avialable_space_x // (2 * star_width)

        # Визначити, яка кількість зірок поміщяєтся на небі.
        ship_height = self.ship.rect.height
        avialable_space_y = (self.settings.screen_height - (3 * star_height) - (5 * ship_height))
        number_rows = avialable_space_y // (2 * star_height)

        # Створити повне зіркове небо
        for row_number in range(number_rows):
            for star_number in range(number_star_x):
                self._create_star(star_number, row_number)

    def _create_star(self, star_number, row_number):
        """ Створити зірку """
        random_width = randint(-10, 100)
        random_height = randint(-500, 50)

        star = Star(self)
        star_width, star_height = star.rect.size

        star.x = star_width + 2 * random_width * star_number
        star.rect.x = star.x

        star.y = star.rect.height + 2 * random_height * row_number
        star.rect.y = star.y

        self.stars.add(star)

    def _update_stars(self):
        """ update stars """
        self.stars.update()
        self._check_stars_bottom()

        # print(len(self.stars))

    def _check_stars_bottom(self):
        """ Перевірити, чи не досяг якийсь прибулець нижнього краю екрана. """
        screen_rect = self.screen.get_rect()
        for star in self.stars.copy():
            if star.rect.bottom >= screen_rect.bottom:
                self.stars.remove(star)
        # if len(self.stars) < 300:
        # print("OK")
        # self._stars_down()

    def _stars_down(self):
        """ Реагувати на зіткнення прибульця з кораблем """

        # self.stars.empty()
        self._create_stars()

    # -------------------------------------------------------------------------------------------------

    # def _create_rains(self):
    #     """ Створити дощове небо """
    #     rain = Rain(self)
    #     rain_width, rain_height = rain.rect.size
    #     avialable_space_x = self.settings.screen_width - (2 * rain_width)
    #     number_rain_x = avialable_space_x // (2 * rain_width)
    #
    #     # Визначити, яка кількість рядів дощу поміщяется на екрані.
    #     ship_height = self.ship.rect.height
    #     avialable_space_y = (self.settings.screen_height - (2 * rain_height) - (5 * ship_height))
    #     number_rows = avialable_space_y // (2 * rain_height)
    #
    #     # Створити повне небо дощу
    #     for row_number in range(number_rows):
    #         for rain_number in range(number_rain_x):
    #             self._create_rain(rain_number, row_number)
    #
    # def _create_rain(self, rain_number, row_number):
    #     """ create rain """
    #     random_width = randint(-10, 50)
    #     random_height = randint(-30, 30)
    #     rain = Rain(self)
    #     rain_width, rain_height = rain.rect.size
    #     rain.x = rain_width + 2 * random_width * rain_number
    #     # rain.x = rain_width + 5 * rain_width * rain_number
    #     # rain.x = random_width
    #     rain.rect.x = rain.x
    #
    #     rain.y = rain.rect.height + 2 * random_height * row_number
    #     # rain.y = rain.rect.height + 3 * rain.rect.height * row_number
    #     rain.rect.y = rain.y
    #
    #     self.rains.add(rain)
    #
    # def _update_rains(self):
    #     """ update rains """
    #     self.rains.update()

    #
    # -------------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------------

    def _update_screen(self):
        """ Оновити збереження на екрані та перемкнутися на новий екран """
        self.screen.fill(self.settings.bg_color)

        # ship
        self.ship.blitme()

        # bullet
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # aliens
        self.aliens.draw(self.screen)

        # stars
        self.stars.draw(self.screen)

        # rains
        # self.rains.draw(self.screen)

        # Намалювати кнопку Play, якщо гра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    # Створити екземпляр гри
    ai = AlienInvsion()
    ai.run_game()
