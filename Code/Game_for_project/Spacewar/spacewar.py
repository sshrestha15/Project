#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 18:47:24 2021

@author: sojanshrestha
"""

import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from gamestats import Gamestats
from score import Score
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf

#attribute for running the game
def run_game():
    
# Initialize game and create a screen object.
    pygame.init()
    sw_settings = Settings()
    screen = pygame.display.set_mode((sw_settings.screen_width, sw_settings.screen_height))
    pygame.display.set_caption("Space War")
    
    # Make the Play button.
    play_button = Button(sw_settings, screen, "Play")
    
    #store game statistics
    stats = Gamestats(sw_settings)
    sb = Score(sw_settings, screen, stats)
    
    # Make a ship.
    ship = Ship(sw_settings, screen)
    # Make a group to store bullets and aliens.
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(sw_settings, screen,ship, aliens)
        
# Start the main loop for the game.
    while True:
        gf.check_events(sw_settings, screen, stats, play_button, ship, aliens, bullets)
        #start the loop for the game
        if stats.game_active:
            ship.update()
            gf.update_bullets(sw_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(sw_settings, stats, screen, ship, aliens, bullets)  
            
        gf.update_screen(sw_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        
run_game()



#https://www.pinterest.com/pin/111534528250050496/
#https://line.17qq.com/articles/qgsgnkgnky.html
#Mathhes, Eric. Python Crash Course: a hands-on, project-based introduction to programming, 2nd Edition. San Fransciso, No Strach Press , 2019.  
