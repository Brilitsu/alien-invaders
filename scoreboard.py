#  Python Crash Course example 14.3
#  
#  Project 1 - Exercise  14-3 - Expanding Alien Invasion
#
#  tracking game score


import pygame.font

from pygame.sprite import Group

from ship import Ship


class Scoreboard():
    """A class to report scoring information."""

    def __init__(self, ai_settings, screen, stats):
        """Initialise score keeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for score image
        self.text_colour = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 32)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()




    def prep_score(self):
        """convert the score into a rendered image for display"""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: " + "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_colour, self.ai_settings.bg_colour)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 5
        self.score_rect.top = 5


    def prep_high_score(self):
        """turn the current high score into a rendered image for display."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score: " + "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_colour, self.ai_settings.bg_colour)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def prep_level(self):
        """turn the level into a rendered image"""
        level_str = "Level: " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_colour, self.ai_settings.bg_colour)

        # position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 2


    def prep_ships(self):
        """show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 5 + ship_number * ship.rect.width
            ship.rect.y = 5
            self.ships.add(ship)


    def show_score(self):
        """draw the score, level and number of ships to the screen"""
        # show the score
        self.screen.blit(self.score_image, self.score_rect)
        # show the high score
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # show the level
        self.screen.blit(self.level_image, self.level_rect)
        # draw the ships
        self.ships.draw(self.screen)


