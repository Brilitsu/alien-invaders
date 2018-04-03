#  Python Crash Course example 14.3
#  
#  Project 1 - Exercise  14-3 - Expanding Alien Invasion
#
# Instructions


import pygame.font


class Instructions():

    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # Set the dimensions and properties of the instructions box
        self.rect_width, self.rect_height = 190, 140
        self.instructions_colour = (0, 255, 0)
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 28)

        self.msg = "P:  Play\nA:  Left\nD:  Right\nV:  Fire\nSpace:  (un)Pause\nEscape:  Quit"

    
        # Build the instructions rect object and center it
        self.rect = pygame.Rect(0,0, self.rect_width, self.rect_height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 100

        #The instructions message needs to be prepped only once
#        self.prep_msg()


    def prep_msg(self):
    
        self.width, self.height = self.ai_settings.screen_width, self.ai_settings.screen_height
    
        # create a new list for each line of text
        self.words = [self.word.split(' ') for self.word in self.msg.splitlines()]
        # set the width of a space character
        self.space = self.font.size(' ')[0]
        # position the instructions text
        self.pos = self.screen_rect.centerx - 85, self.screen_rect.centery + 170
        self.word_x, self.word_y = self.pos
    
        for self.line in self.words:
            for self.word in self.line:
                self.msg_image = self.font.render(self.word, 0, self.text_colour, self.instructions_colour)
                self.word_width, self.word_height = self.msg_image.get_size()
                if self.word_x + self.word_width >= self.width:
                    # Reset the word x
                    self.word_x = self.pos[0]
                    # Start on new row
                    self.word_y += self.word_height
                    # draw that word to the screen
                self.screen.blit(self.msg_image, (self.word_x, self.word_y))
                # add a space and render the next word
                self.word_x += self.word_width + self.space
                # Reset the word x position
            self.word_x = self.pos[0]
            # Start on new row
            self.word_y += self.word_height


    def draw_instructions(self):
        # Draw a blank button and then draw the message over
        self.screen.fill(self.instructions_colour, self.rect)


