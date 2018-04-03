







from settings import Settings
import pygame
import pygame.font
pygame.init()


ai_settings = Settings()
bg_colour = ai_settings.bg_colour
screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))


msg = "P:  Play\nA:  Left\nD:  Right\nV:  Fire\nSpace:  (un)Pause\nEscape:  Quit"


def instruction_text(ai_settings, screen, msg):
    screen = screen
    screen_rect = screen.get_rect()

    # Set the dimensions and properties of the instructions box
    width, height = 325, 280
    instructions_colour = (0, 255, 0)
    text_colour = (255, 255, 255)
    font = pygame.font.SysFont(None, 28)
    
    # Build the instructions rect object and center it
    rect = pygame.Rect(0,0, width, height)
    rect.centerx = screen_rect.centerx
    rect.bottom = screen_rect.bottom - 100

    #The instructions message needs to be prepped only once
    screen.fill(instructions_colour, rect)
    prep_msg(ai_settings,screen, msg)


def prep_msg(ai_settings,screen, msg):
    screen = screen
    screen_rect = screen.get_rect()
    
    width, height = ai_settings.screen_width, ai_settings.screen_height
    instructions_colour = (0, 255, 0)
    text_colour = (255, 255, 255)
    font = pygame.font.SysFont(None, 28)
    
    # create a new list for each line of text
    words = [word.split(' ') for word in msg.splitlines()]
    # set the width of a space character
    space = font.size(' ')[0]
    # position the instructions text
    pos = screen_rect.center# x, screen_rect.bottom - 100
    word_x, word_y = pos
    
    for line in words:
        for word in line:
            msg_image = font.render(word, 0, text_colour, instructions_colour)
            word_width, word_height = msg_image.get_size()
            if word_x + word_width >= width:
                # Reset the word x
                word_x = pos[0]
                # Start on new row
                word_y += word_height
                # draw that word to the screen
            screen.blit(msg_image, (word_x, word_y))
            # add a space and render the next word
            word_x += word_width + space
            # Reset the word x position
        word_x = pos[0]
        # Start on new row
        word_y += word_height








while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(bg_colour)
    instruction_text(ai_settings, screen, msg)
    pygame.display.update()










