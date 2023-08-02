#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 20:26:16 2021

@author: sojanshrestha
"""

import pygame
from pygame.sprite import Sprite

#creating bullet class to store bullets
class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    #parameter for creating bullet
    def __init__(self, sw_settings, screen, ship):
        """Create a bullet object at the ship's current position."""
        #calling super() from sprite to inherit the features for bullet
        super(Bullet, self).__init__()
        self.screen = screen
        
        # Create a bullet rect and then set its position.
        self.rect = pygame.Rect(0, 0, sw_settings.bullet_width, sw_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # Storing the bullet's position
        self.y = float(self.rect.y)
        
        ##speed and color of bullets
        self.color = sw_settings.bullet_color
        self.speed_factor = sw_settings.bullet_speed_factor
     
        #attributes for updating the bullet position
    def update(self):
        """Move the bullet up the screen."""
        
        #updating the position of the bullet while substracting the the amount of stored bullets                                                              
        self.y -= self.speed_factor
        # Updating the position.
        self.rect.y = self.y
    
    #attributes for drawing the bullet
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)