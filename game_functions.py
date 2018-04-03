#  Python Crash Course example 14.3
#  
#  Project 1 - Exercise  14-3 - Expanding Alien Invasion
#
#  The games main code


# Imports

import sys

import pygame

from bullet import Bullet

from bomb import Bomb

from alien import Alien

from brick import Brick

from time import sleep

from random import choice, sample


# Sounds

pygame.mixer.init()

start_sound = pygame.mixer.Sound('sounds/ping.wav')
bullet_sound = pygame.mixer.Sound('sounds/shot.wav')
bomb_sound = pygame.mixer.Sound('sounds/bomb.wav')
alien_death_sound = pygame.mixer.Sound('sounds/alien_die.wav')
barrier_destroy_sound = pygame.mixer.Sound('sounds/barrier_destroy.wav')
ship_kill_sound = pygame.mixer.Sound('sounds/ship_hit.wav')
new_level_sound = pygame.mixer.Sound('sounds/new_level.wav')


# Code


def check_keydown_events(event, ai_settings, stats, sb, screen, aliens, ship, bullets, bombs, bricks_1, bricks_2, bricks_3):
    """respond to keypresses."""
    # Move the ship to the right
    if event.key == pygame.K_d:
        ship.moving_right = True
    # Move the ship to the left
    elif event.key == pygame.K_a:
        ship.moving_left = True

    # fire bullets
    if event.key == pygame.K_v:
        fire_bullet(ai_settings, screen, ship, bullets)

    # start the game
    if event.key == pygame.K_p:
        start_game(ai_settings, stats, sb, screen, ship, aliens, bullets, bombs, bricks_1, bricks_2, bricks_3)

    # pause and restart the game
    if event.key == pygame.K_SPACE:
        pause_game(stats)

    # quit the game
    if event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_events(event, ship):
    """respond to key release."""
    # stop the ship moving right
    if event.key == pygame.K_d:
        ship.moving_right = False
    # Stop the ship moving left
    elif event.key == pygame.K_a:
        ship.moving_left = False


def check_pause_event(event, stats):
    # pause and restart the game
    if event.key == pygame.K_SPACE:
        pause_game(stats)


def check_events(ai_settings, stats, sb, screen, play_button, pause_button, ship, aliens, bullets, bombs, bricks_1, bricks_2, bricks_3):
    """respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, stats, sb, screen, play_button, pause_button, ship, aliens, bullets, bombs, bricks_1, bricks_2, bricks_3, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, sb, screen, aliens, ship, bullets, bombs, bricks_1, bricks_2, bricks_3)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_pause(stats):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_pause_event(event, stats)



def check_play_button(ai_settings, stats, sb, screen, play_button, pause_button, ship, aliens, bullets, bombs, bricks_1, bricks_2, bricks_3, mouse_x, mouse_y):
    """Start a new game when the player clicks play"""
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

        start_game(ai_settings, stats, sb, screen, ship, aliens, bullets, bombs, bricks_1, bricks_2, bricks_3)





def start_game(ai_settings, stats, sb, screen, ship, aliens, bullets, bombs, bricks_1, bricks_2, bricks_3):
    """Start a new game when the player clicks play"""
        
    if stats.game_active == False and stats.game_paused == False:
        ai_settings.initialise_dynamic_settings()
        # hide the mouse cursor
        pygame.mouse.set_visible(False)
        # reset the game statistics
        stats.reset_stats()
        # start the game
        stats.game_active = True
        pygame.mixer.Sound.play(start_sound)
        sleep(0.5)

        # reset the scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # empty the aliens and bullets lists
        aliens.empty()
        bullets.empty()
        bombs.empty()

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        create_barriers(ai_settings, screen, ship, bricks_1, bricks_2, bricks_3)
        ship.center_ship()


def pause_game(stats):
    if stats.game_active == True and stats.game_paused == False:
        stats.game_active = False
        stats.game_paused = True
    elif stats.game_active == False and stats.game_paused == True:
        stats.game_active = True
        stats.game_paused = False





def fire_bullet(ai_settings, screen, ship, bullets):
    """fire a bullet if the max amount not currently met"""
    # create a bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        pygame.mixer.Sound.play(bullet_sound)

def update_bullets(ai_settings, stats, sb, screen, ship, aliens, bullets, bricks_1, bricks_2, bricks_3):
    """update the position of bullets and get rid of off screen bullets."""
    # update the bullet positions.
    bullets.update()

    # delete bullets that have passed the screen edge
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # delete bullets that have hit an alien
    check_bullet_alien_collisions(ai_settings, stats, sb, screen, ship, aliens, bullets)
    check_bullet_barrier_collisions(ai_settings, screen, ship, bullets, bricks_1, bricks_2, bricks_3)

def check_bullet_alien_collisions(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """respond to a bullet-alien collision"""
    # remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
        pygame.mixer.Sound.play(alien_death_sound)

    if len(aliens) == 0:
        # If the entire fleet of aliens is destroyed, start a new level
        # destroy existing bullets, speed up the game, and create new fleet
        bullets.empty()
        ai_settings.increase_speed()

        #increase level
        stats.level += 1
        pygame.mixer.Sound.play(new_level_sound)
        ai_settings.bombs_allowed += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)





def drop_bomb(ai_settings, screen, ship, aliens, bombs):
    #select a random alien from the list of aliens 
    abp = list(aliens)
    if len(abp) > 0:
        alien_bomb_prepped = choice(abp)
    
    for alien in aliens.copy():
        if alien_bomb_prepped.rect.x == ship.rect.x and len(bombs) < ai_settings.bombs_allowed:
            new_bomb = Bomb(ai_settings, screen, alien_bomb_prepped)
            bombs.add(new_bomb)
            pygame.mixer.Sound.play(bomb_sound)


def update_bombs(ai_settings, stats, sb, screen, ship, aliens, bullets, bombs, bricks_1, bricks_2, bricks_3):
    """update the position of bombs and get rid of off screen bombs."""
    # update the bomb positions.
    bombs.update()

    for bomb in bombs.copy():
        # delete bombs that have passed the screen edge
        if bomb.rect.bottom >= ai_settings.screen_height:
            bombs.remove(bomb)
        # if bomb hits ship, kill the ship
        if pygame.sprite.spritecollideany(ship, bombs):
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, bombs)
        # if bomb hits barrier delete both
        bb_collision = pygame.sprite.groupcollide(bombs, bricks_1, True, True)\
        or pygame.sprite.groupcollide(bombs, bricks_2, True, True)\
        or pygame.sprite.groupcollide(bombs, bricks_3, True, True)

        if bb_collision:
            pygame.mixer.Sound.play(barrier_destroy_sound)




def get_number_aliens_x(ai_settings, alien_width):
    """determine the number of aliens that fit in a row"""
    # find the number of aliens in a row.
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """determine the number of rows of aliens that fit on a screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (1.75 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an Alien and place it in the row"""
    # Create an alien
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width / 2 + 1.55 * alien_width * alien_number
    alien.y = alien.rect.height + 1.25 * alien.rect.height * row_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """create a full fleet of aliens"""
    alien = Alien(ai_settings, screen)
    alien_height = alien.rect.height
    ship_height = ship.rect.height
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship_height, alien_height)

    # Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """respond apropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """drop the fleet and change the fleets direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treet it the same as the ship getting hit
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, bombs)
            break


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, bombs, bricks_1, bricks_2, bricks_3):
    """update the position of all aliens in the fleet"""
    # check for aliens reaching either side of the screen
    check_fleet_edges(ai_settings, aliens)
    # check for aliens reaching the bottom fo the screen
    check_aliens_barrier_collisions(ai_settings, screen, ship, aliens, bricks_1, bricks_2, bricks_3)
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
    drop_bomb(ai_settings, screen, ship, aliens, bombs)
    aliens.update()

    #look for ship - alien collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, bombs)





def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, bombs):
    """respond to the ship being hit by an alien"""
    if stats.ships_left > 0:
        # Decrement number of ships left
        stats.ships_left -= 1
        pygame.mixer.Sound.play(ship_kill_sound)

        # update the scoreboard
        sb.prep_ships()

        # empty the bullets, bombs and aliens lists
        aliens.empty()
        bullets.empty()
        bombs.empty()

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


        # pause the game for a moment
        sleep(0.5)
    else:
        stats.game_active = False
        stats.game_paused = False
        pygame.mouse.set_visible(True)





def create_brick_1(ai_settings, screen, ship, bricks_1, brick_column_number, brick_row_number):
    """Create an Brick and place it in the row"""
    # Create an brick
    brick = Brick(ai_settings, screen)
    brick_width = brick.rect.width
    brick_height = brick.rect.height
    screen_height = ai_settings.screen_height
    screen_width = ai_settings.screen_width
    barrier_width = ai_settings.barrier_width
    barrier_height = ai_settings.barrier_height
    ship_height = ship.rect.height
    
    brick.rect.x = (screen_width / 5) - (barrier_width * brick_width) / 2 + (brick_width * brick_column_number)
    brick.rect.y = screen_height - (ship_height * 1.5 + barrier_height * brick_height) + (brick_height * brick_row_number)
    bricks_1.add(brick)


def create_brick_2(ai_settings, screen, ship, bricks_2, brick_column_number, brick_row_number):
    """Create an Brick and place it in the row"""
    # Create an brick
    brick = Brick(ai_settings, screen)
    brick_width = brick.rect.width
    brick_height = brick.rect.height
    screen_height = ai_settings.screen_height
    screen_width = ai_settings.screen_width
    barrier_width = ai_settings.barrier_width
    barrier_height = ai_settings.barrier_height
    ship_height = ship.rect.height
    
    brick.rect.x = (screen_width / 2) - (barrier_width * brick_width) / 2 + (brick_width * brick_column_number)
    brick.rect.y = screen_height - (ship_height * 1.5 + barrier_height * brick_height) + (brick_height * brick_row_number)
    bricks_2.add(brick)


def create_brick_3(ai_settings, screen, ship, bricks_3, brick_column_number, brick_row_number):
    """Create an Brick and place it in the row"""
    # Create an brick
    brick = Brick(ai_settings, screen)
    brick_width = brick.rect.width
    brick_height = brick.rect.height
    screen_height = ai_settings.screen_height
    screen_width = ai_settings.screen_width
    barrier_width = ai_settings.barrier_width
    barrier_height = ai_settings.barrier_height
    ship_height = ship.rect.height
    
    brick.rect.x = (screen_width - screen_width / 5) - (barrier_width * brick_width) / 2 + (brick_width * brick_column_number)
    brick.rect.y = screen_height - (ship_height * 1.5 + barrier_height * brick_height) + (brick_height * brick_row_number)
    bricks_3.add(brick)


def create_barriers(ai_settings, screen, ship, bricks_1, bricks_2, bricks_3):
    """create a full barrier of bricks"""
    brick = Brick(ai_settings, screen)
    barrier_width = ai_settings.barrier_width
    barrier_height = ai_settings.barrier_height

    # Create the first row of bricks
    for brick_row_number in range(barrier_height):
        for brick_column_number in range(barrier_width):
            create_brick_1(ai_settings, screen, ship, bricks_1, brick_column_number, brick_row_number)
            create_brick_2(ai_settings, screen, ship, bricks_2, brick_column_number, brick_row_number)
            create_brick_3(ai_settings, screen, ship, bricks_3, brick_column_number, brick_row_number)


def check_bullet_barrier_collisions(ai_settings, screen, ship, bullets, bricks_1, bricks_2, bricks_3):
    """respond to a bullet-alien collision"""
    # remove any bullets and aliens that have collided
    bb_collision = pygame.sprite.groupcollide(bullets, bricks_1, True, True)\
    or pygame.sprite.groupcollide(bullets, bricks_2, True, True)\
    or pygame.sprite.groupcollide(bullets, bricks_3, True, True)

#    if bb_collision:
#        pygame.mixer.Sound.play(barrier_destroy_sound)


def check_aliens_barrier_collisions(ai_settings, screen, ship, aliens, bricks_1, bricks_2, bricks_3):
    """respond to a bullet-alien collision"""
    # remove any aliens and aliens that have collided
    ab_collision = pygame.sprite.groupcollide(aliens, bricks_1, True, True)\
    or pygame.sprite.groupcollide(aliens, bricks_2, True, True)\
    or pygame.sprite.groupcollide(aliens, bricks_3, True, True)

    if ab_collision:
        pygame.mixer.Sound.play(barrier_destroy_sound)



    


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        with open('high_score.txt', 'w') as hs:
            hs.write(str(stats.score))
        sb.prep_high_score()





def update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets,
                    bombs, bricks_1, bricks_2, bricks_3, play_button, pause_button, instructions):
    """Update the images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_colour)

    #redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for bomb in bombs.sprites():
        bomb.draw_bomb()

    # Draw the ship
    ship.blitme()
    # Draw the aliens
    aliens.draw(screen)

    # Draw the barriers
    bricks_1.draw(screen)
    bricks_2.draw(screen)
    bricks_3.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the Play button if the game is inactive
    if not stats.game_active and not stats.game_paused:
        play_button.draw_button()
        instructions.draw_instructions()
        instructions.prep_msg()

    # Draw Paused badge
    if stats.game_paused == True:
        pause_button.draw_button()
        instructions.draw_instructions()
        instructions.prep_msg()
        
    # make the most recently drawn screen visible.
    pygame.display.flip()


