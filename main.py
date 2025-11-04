"""Asteroids: game bootstrap and main loop.

This module initializes pygame, creates sprite groups for update/draw,
spawns the Player at screen center, and runs the fixed-timestep render loop.
"""


import pygame
from constants import (
    SCREEN_HEIGHT, 
    SCREEN_WIDTH, 
    ASTEROID_KINDS, 
    ASTEROID_MIN_RADIUS, 
    ASTEROID_MAX_RADIUS, 
    ASTEROID_SPAWN_RATE,
)
from player import Player


def main() -> None:
    """Entry point for the Asteroids game.
    
    Responsibilities:
        - Initialize pygame and the display surface.
        - Create sprite groups for updatable and drawable entities.
        - Register Player's containers so it's auto-added to groups on init.
        - Run the main loop: handle events, update, draw, and cap FPS.
    
    """
    pygame.init()
    
    # Create the window/screen surface.
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    
    # Fixed FPS timer
    clock = pygame.time.Clock() 
    dt = 0 # stores seconds elapses per frame
    
    
    
    # Sprite groups:
    #   - updatable: any object that implements .update(dt)
    #   - drawable: any object that implements .draw(scree)
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable) # Set containers on the class 
    
    # Spawn the player at the center of the screen.
    player = Player(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2))
   
   
    
    running = True   
    while running:
        
        # Event handling; Make the window's close button work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        
        updatable.update(dt) # Group update forwards dt to each member's .update(dt)
        
        
        # --- Rendering ---
        # Fill black background 
        screen.fill((0, 0, 0))
        
        
        for sprite in drawable:
            sprite.draw(screen)
        
        
        pygame.display.flip() # Present the frame to the screen
        
        # Limit to 60 FPS and convert delta time from milliseconds to seconds
        dt = clock.tick(60) / 1000
    
    pygame.quit()

if __name__ == "__main__":
    main()
