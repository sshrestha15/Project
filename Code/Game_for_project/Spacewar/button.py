#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 14:55:00 2021

@author: sojanshrestha
"""

import pygame.font

#class for play button
class Button():
    #inputting the parameters for the button
    def __init__(self, sw_settings, screen, msg):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (200, 20, 50)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        # Building the button's rect object
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        #centering the button
        self.rect.center = self.screen_rect.center
        # The button message
        self.prep_msg(msg)
       
        #parameter for the  message as an image
    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        #creating the rect for the image
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
       
        #parameter for box for the play button
    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)