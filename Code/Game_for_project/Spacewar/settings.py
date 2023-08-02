#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 18:52:30 2021

@author: sojanshrestha
"""

#creating the class for different settings of the game
class Settings():
    """A class to store all settings for Alien Invasion."""
    #attributes for settings the screen
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1800
        self.screen_height = 1000
        self.bg_color = (0, 0, 0)
        
        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        
        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 250, 0, 0
        self.bullets_allowed = 10
        
        # Alien force settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 5
        
        #fleet direction: 1 refers to right and viceversa
        self.fleet_direction = 1
        
        #speed settings
        self.speedup_scale = 1.5
        
        #Score settings
        self.score_scale = 1.5
        
        #attributes for initializing the game
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3

        self.alien_speed_factor = 1
        # fleet_direction 
        self.fleet_direction = 1
        
        #scoring
        self.alien_points = 50
        
      #attributes for increasing the speed for each level  
    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
       
        #increaing the point values
        self.alien_points = int(self.alien_points * self.score_scale)
       
        