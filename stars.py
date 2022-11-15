import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """ Клас, що представляє одну зірку """

    def __init__(self, ai_game):
        """ Ініціалізувати рпибульця та задати його початкове розташування """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('img/s_ta_r.png')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horisontal position
        self.y = float(self.rect.y)

    def update(self):
        """ update """
        self.y += self.settings.stars_speed
        self.rect.y = self.y



