#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 15:24:39 2021

@author: sojanshrestha
"""

import pygame.font
#class for recording the score when the bullets hits the alien ship hits the rebel ship
class Score():
    """A class to report scoring information."""
    #parameter for settings the score
    def __init__(self, sw_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        #recording the scores
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.sw_settings = sw_settings
        self.stats = stats
        # Font color and font size for score
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Prepare the initial score image.
        self.prep_score()
        
    #parameter for changing numerical value into string and creating image
    def prep_score(self):
        """Turn the score into a rendered image."""
        
        #rounding up the score if there are decimal values
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.sw_settings.bg_color)
        
        # Displaying the score
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def show_score(self):
        """Draw score to the screen."""
        #showing the screen
        self.screen.blit(self.score_image, self.score_rect)