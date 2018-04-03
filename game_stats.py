#  Python Crash Course example 14.3
#  
#  Project 1 - Exercise  14-3 - Expanding Alien Invasion
#
#  tracking game stats



class GameStats():
    """tracks the statistics for alien invasion."""
    def __init__(self, ai_settings):
        """initialise stats collection"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # keep track of the highest score
        with open('high_score.txt') as hs:
            persistent_hs = hs.read()
            self.high_score = int(persistent_hs)

        # Start Alien Invasion in an active state
        self.game_active = False
        self.game_paused = False

    def reset_stats(self):
        """initialise those statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        
