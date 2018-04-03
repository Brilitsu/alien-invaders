#  Python Crash Course example 14.3
#  
#  Project 1 - Exercise  14-3 - Expanding Alien Invasion
#
#  The games launch code


# Import modules

import pygame

from settings import Settings

import game_functions as gf

from ship import Ship

from pygame.sprite import Group

from game_stats import GameStats

from scoreboard import Scoreboard

from button import Button

from instructions import Instructions

# Code


def run_game():
    # Initialise  pygame, settings and screen object.
    pygame.init()
    pygame.mixer.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button
    play_button = Button(ai_settings, screen, "Ready Player 1?")

    pause_button = Button(ai_settings, screen, "Paused")

    instructions = Instructions(ai_settings, screen)

    # Make a ship
    ship = Ship(ai_settings, screen)
    # Make a group to store bullets in
    bullets = Group()

    # Make a group to store aliens in
    aliens = Group()
    # Create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    bombs = Group()

    # Make a group to store bricks in
    bricks_1 = Group()
    bricks_2 = Group()
    bricks_3 = Group()
    # Create a barrier of bricks
    gf.create_barriers(ai_settings, screen, ship, bricks_1, bricks_2, bricks_3)
    

    # create an instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)


    # Start the main loop for the game.
    while True:
        
        # Watch for keybaord and mouse events.
        gf.check_events(ai_settings, stats, sb, screen, play_button, pause_button, ship, aliens, bullets, bombs, bricks_1, bricks_2, bricks_3)

        if stats.game_paused:
            gf.check_pause(stats)
            

        if stats.game_active:
            # Update the ship position
            ship.update()
            # update the ship bullets
            gf.update_bullets(ai_settings,stats, sb, screen, ship, aliens, bullets, bricks_1, bricks_2, bricks_3)

            # update the aliens position
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, bombs, bricks_1, bricks_2, bricks_3)

            gf.update_bombs(ai_settings, stats, sb, screen, ship, aliens, bullets, bombs, bricks_1, bricks_2, bricks_3)
       
        # Redraw the screen during each pass through the loop and,
        # make the most recently drawn screen visible.
        gf.update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, bombs, bricks_1, bricks_2, bricks_3, play_button, pause_button, instructions)

run_game()

