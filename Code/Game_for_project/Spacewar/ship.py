#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 18:53:53 2021

@author: sojanshrestha
"""

import pygame

class Ship():
    def __init__(self, sw_settings, screen):
        """Initialize the ship and set its starting position."""
        self.screen = screen
        self.sw_settings = sw_settings
    
        # Load the ship image and get its rect.
        self.image = pygame.image.load('/Users/sojanshrestha/Desktop/CSCE890/game/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Starting each new ship at the bottom and center
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        #decimal value for the ship's center.
        self.center = float(self.rect.centerx)
        
        # Movement of the ship
        self.moving_right = False
        self.moving_left = False
        
        
        
    def update(self):
        """Update the ship's position based on the movement flags."""
        
        # Updating the ship center value
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.sw_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.sw_settings.ship_speed_factor
            
        # Updating rect object
        self.rect.centerx = self.center
    
    def blitme(self):
        """Draw the ship at its current location."""
        #current location of the ship
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """Center the ship on the screen."""
        #positioning the ship
        self.center = self.screen_rect.centerx