#  Python Crash Course example 14.3
#  
#  Project 1 - Exercise  14-3 - Expanding Alien Invasion
#
#  Player Ship

import pygame

from pygame.sprite import Sprite


class Ship(Sprite):
    
    
    def __init__(self, ai_settings, screen):
        """initialises the ship and sets its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Start each new ship at the bottom centre of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.bottom - (self.rect.height / 1.5)

        # Store a decimal value for the ship's centre.
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

        # movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def center_ship(self):
        """center the ship on the screen."""
        self.center_x = self.screen_rect.centerx
        self.center_y = self.screen_rect.bottom - (self.rect.height / 1.5)
        

    def update(self):
        """update the ships position based on the movement flags"""
        # update the ship's centre value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center_x -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.center_y -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center_y += self.ai_settings.ship_speed_factor

        # Update rect object from self.center
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

