#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 21:09:20 2021

@author: sojanshrestha
"""

import pygame
from pygame.sprite import Sprite

#creating the class for the alien force
class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self, sw_settings, screen):
        """Initialize the alien and set its starting position."""
        #setting the position of the alien ship
        super(Alien, self).__init__()
        self.screen = screen
        self.sw_settings = sw_settings
        
        # Load the alien image
        self.image = pygame.image.load('/Users/sojanshrestha/Desktop/CSCE890/game/alien.bmp')
        self.rect = self.image.get_rect()
        
        # Start new alien at the top
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # position of the ship.
        self.x = float(self.rect.x)
        
    def blitme(self):
        """Draw the alien at its current location."""
        #positioning the ship location
        self.screen.blit(self.image, self.rect)
    
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        #checking to see if the alien ship is in the edge of the screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True    
        
    def update(self):
        """Move the alien right or left."""
        #moving the ship
        self.x += (self.sw_settings.alien_speed_factor * self.sw_settings.fleet_direction)
        self.rect.x = self.x    