#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 18:54:46 2021

@author: sojanshrestha
"""

import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
    
#different functionality for running the agme
#moving the ship left and right with directional keys and space bar for bullets
def check_keydown_events(event, sw_settings, screen, ship, bullets):
    """Respond to keypresses."""   
    
    if event.key == pygame.K_RIGHT:
        # Moveing the ship to the right.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Creating a new bullet
        if len(bullets) < sw_settings.bullets_allowed:
            new_bullet = Bullet(sw_settings, screen, ship)
            bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()
        
#responding to directional keys              
def check_keyup_events(event, ship):
    """Respond to key releases."""         
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
            
#checking how the key responds       
def check_events(sw_settings, screen, stats, play_button, ship,aliens, bullets):
    """Respond to keypresses and mouse events."""
    # Watch for keyboard and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, sw_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(sw_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)

#Responding to the play button            
def check_play_button(sw_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    #clicking mouse on the play button
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        
        # Reset the game settings.
        sw_settings.initialize_dynamic_settings()
        
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
            
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True
        
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        
        # Create a new fleet
        create_fleet(sw_settings, screen, ship, aliens)
        ship.center_ship()
               
#Updating the bullets after it fires       
def update_bullets(sw_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    # Removing the bullets that disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(sw_settings, screen, stats, sb, ship, aliens, bullets)

#checking if the bullet collided with the alien ship    
def check_bullet_alien_collisions(sw_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Removing any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += sw_settings.alien_points * len(aliens)
            sb.prep_score()
        
    if len(aliens) == 0:
        # Destroying the  existing bullets and creating a new fleet.
        bullets.empty()
        sw_settings.increase_speed()
        create_fleet(sw_settings, screen, ship, aliens)

#Updating the screen for ships and bullets          
def update_screen(sw_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen."""          
    # Redrawing the screen when it passes through the loop.
    screen.fill(sw_settings.bg_color)
    
    # Redrawing all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    #score information
    sb.show_score()
    
    # Drawing the play button when the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
        
    # Most recent screen.
    pygame.display.flip()
 
 
#Finding the number of aliens ship that can fit in the screen    
def get_number_aliens_x(sw_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    #horizontal space that is available for alien ships in x-coordinate
    available_space_x = sw_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x 

#Finding the number of rows  for aliens ship that can fit in the row      
def get_number_rows(sw_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    #vertical space available in the y-coordinate
    available_space_y = (sw_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

#creating aliens  
def create_alien(sw_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(sw_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
 
#creating the fleet   
def create_fleet(sw_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Creating an alien in a row
    alien = Alien(sw_settings, screen)
    number_aliens_x = get_number_aliens_x(sw_settings, alien.rect.width)
    number_rows = get_number_rows(sw_settings, ship.rect.height, alien.rect.height)
    # Creating the loop for fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(sw_settings, screen, aliens, alien_number,row_number)        
        
#Checking if the aliens ship reached any edges so that the fleet will move down       
def check_fleet_edges(sw_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    #Loop to check if the fleet reaches edge
    for alien in aliens.sprites():
        if alien.check_edges():
            #changing the direction of the fleet when it reaches the edge
            change_fleet_direction(sw_settings, aliens)
            break

#Changing the direction of the fleet
def change_fleet_direction(sw_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    #loop to check if the fleet hit the edges
    for alien in aliens.sprites():
        #if true, it needs to drop down
        alien.rect.y += sw_settings.fleet_drop_speed
    sw_settings.fleet_direction *= -1
    
#attributes when alien ship hits the ship    
def ship_hit(sw_settings, stats, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    #checking if there is al least one ship
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        # Emptying the remaining aliens and bullets.
        aliens.empty()
        bullets.empty()
        
        # Create a new fleet
        create_fleet(sw_settings, screen, ship, aliens)
        ship.center_ship()
        
        # Pausing when the ships collide
        sleep(1) 
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

#attributes to check for alien ship is at the bottoms    
def check_aliens_bottom(sw_settings, stats, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    #loop to check if the ship shit the bottom
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(sw_settings, stats, screen, ship, aliens, bullets)
            break

#updating the alien fleet and changing the position of the fleet   
def update_aliens(sw_settings, stats, screen, ship, aliens, bullets):
    """Check if the fleet is at an edge, and then update the postions of all aliens in the fleet."""
    #checking to see if the fleet is in the edge
    check_fleet_edges(sw_settings, aliens)
    aliens.update()   
    
    #checking foe the collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(sw_settings, stats, screen, ship, aliens, bullets)
   #checking if the ship hit the bottom
    check_aliens_bottom(sw_settings, stats, screen, ship, aliens, bullets)

    

        