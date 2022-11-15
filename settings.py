class Settings:
    """ Класс для збереження всіх налаштувань гри """

    def __init__(self):
        """ Ініціалізувати нашалтування гри """

        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (13, 33, 79)

        # ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed = 5.5
        self.bullet_width = 3000
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 20

        # alien settings
        self.alien_speed = 0.3
        self.fleet_drop_speed = 10

        # fleet_direction 1 означає напрямок руху праворуч; -1  -- луворуч.
        self.fleet_direction = 1

        # rain settings
        self.rains_speed = 3.0

        # star settings
        self.stars_speed = 3.0

    def change_background(self):
        """ Зміна головного фону  """
        if self.bg_color == (75, 0, 130):
            self.bg_color = (47, 79, 79)
        elif self.bg_color == (47, 79, 79):
            self.bg_color = (0, 0, 0)
        else:
            self.bg_color = (75, 0, 130)

    def change_bullets_speed(self):
        """ Зміна швидкості кулі """
        if self.bullet_speed == 15.5:
            self.bullet_speed = 25.5

        elif self.bullet_speed == 25.5:
            self.bullet_speed = 35.5

        else:
            self.bullet_speed = 15.5

    def change_ship_speed(self):
        """ Зміна швидкості корабля  """
        if self.ship_speed == 5.5:
            self.ship_speed = 10.5

        elif self.ship_speed == 10.5:
            self.ship_speed = 15.5

        else:
            self.ship_speed = 5.5

    def change_alien_speed(self):
        """ Зміна швидкості корабля  """
        if self.alien_speed == 1.3:
            self.alien_speed = 2.3

        elif self.alien_speed == 2.3:
            self.alien_speed = 3.3

        else:
            self.alien_speed = 1.3







