#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 14:20:07 2021

@author: sojanshrestha
"""

#class for game statistics which the game is running
class Gamestats():
    """Track statistics for Alien Invasion."""
    #parameter for setting the statistics
    def __init__(self, sw_settings):
        """Initialize statistics."""
        self.sw_settings = sw_settings
        self.reset_stats()
        
        # Starting Alien force in an inactive state.
        self.game_active = False
        
     #parameter for resetting the game when player starts a new game   
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.sw_settings.ship_limit
        self.score = 0