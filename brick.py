#  Python Crash Course example 14.3
#  
#  Project 1 - Exercise  14-3 - Expanding Alien Invasion
#
# Defence Brick


import pygame

from pygame.sprite import Sprite



class Brick(Sprite):

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        self.image = pygame.Surface([ai_settings.brick_width, ai_settings.brick_height])
        self.image.fill(ai_settings.brick_colour)

        # Create a brick rect
        self.rect = self.image.get_rect()
        

        # Store the bricks exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)



    def draw_brick(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.rect)




