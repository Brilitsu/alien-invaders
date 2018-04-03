#  Python Crash Course example 14.3
#  
#  Project 1 - Exercise  14-3 - Expanding Alien Invasion
#
#  Bomb


import pygame
from pygame.sprite import Sprite


class Bomb(Sprite):
    """A class to manage bombs fired from the alien"""

    def __init__(self, ai_settings, screen, alien):
        """Create a bomb object at the aliens current lcation"""
        super().__init__()
        self.screen = screen
        
        # Create a bomb rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bomb_width, ai_settings.bomb_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.bottom = alien.rect.bottom

        # Store the bombs position as a decimal value.
        self.y = float(self.rect.y)

        self.colour = ai_settings.bomb_colour
        self.speed_factor = ai_settings.bomb_speed_factor


    def update(self):
        """move the bomb down the screen."""
        # Update the decimal postion of the bomb
        self.y += self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_bomb(self):
        """Draw the bomb to the screen."""
        pygame.draw.rect(self.screen, self.colour, self.rect)

