#  Python Crash Course example 14.3
#  
#  Project 1 - Exercise  14-3 - Expanding Alien Invasion
#
#  The games settings


class Settings():
    """A class to store all of the settings for Alien Invasion."""

    def __init__(self):
        """Initialise the games static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (75, 75, 250)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = 60,60,60
        self.bullets_allowed = 5

        # Bomb settings
        self.bomb_width = 15
        self.bomb_height = 15
        self.bomb_colour = 0,0,0

        #Alien settings
        self.fleet_drop_speed = 10
        # fleet direction of 1 represents right, -1 left
        self.fleet_direction = 1

        # How quickly the game speeds up (difficulty setting)
        self.alien_speedup_scale = 1.2
        self.ship_speedup_scale = 1.05
        self.bullet_speedup_scale = 1
        self.bomb_speedup_scale = 1.05

        # How quickly alien point value increases.
        self.score_scale = 1.5


        # Defence brick settings
        self.brick_width = 10
        self.brick_height = 10
        self.brick_colour = 77,77,77

        # barrier made of bricks settings
        self.barrier_width = 15
        self.barrier_height = 10

        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        """imitialise the settigns that change throughout the game."""
        self.ship_speed_factor = 1.15
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.bomb_speed_factor = 3

        # arm extra bombs
        self.bombs_allowed = 3

        # fleet direction of 1 represents right, -1 left
        self.fleet_direction = 1

        # scoring
        self.alien_points = 10

    def increase_speed(self):
        """Increase the speed settings and alien point value."""
        self.ship_speed_factor *= self.ship_speedup_scale
        self.bullet_speed_factor *= self.bullet_speedup_scale
        self.alien_speed_factor *= self.alien_speedup_scale
        self.bomb_speed_factor *= self.bomb_speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)


