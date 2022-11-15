class GameStats:
    """ Відстежування статистики гри """

    def __init__(self, ai_game):
        """ Ініціалізація стаитистики. """
        self.settings = ai_game.settings
        self.reset_stats()

        # Start game in an inactive state
        self.game_active = False

        # Розпочати гру в активному стані
        self.game_active = True


    def reset_stats(self):
        """ Ініціалізація статистики, що може змінюватися впродовж гри. """
        self.ships_left = self.settings.ship_limit


