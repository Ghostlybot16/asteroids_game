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
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shoot import Shot


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
    dt = 0 # stores seconds elapsed per frame
    
    
    
    # Sprite groups:
    #   - updatable: any object that implements .update(dt)
    #   - drawable: any object that implements .draw(screen)
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    # Set contianers on classes
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    
    # Spawn the player at the center of the screen.
    player = Player(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2))
    
    # Spawn asteroid field 
    asteroid_field = AsteroidField()
   
   
    
    running = True   
    while running:
        
        # Event handling; Make the window's close button work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        
        updatable.update(dt) # Group update forwards dt to each member's .update(dt)
        
        for asteroid in asteroids:
            if asteroid.collision_check(player):
                print("Game Over!")
                pygame.quit()
                return
        
        for asteroid in asteroids.sprites():
            for bullet in shots.sprites():
                if bullet.collision_check(asteroid): # If bullet and asteroids collide, remove both objects from display
                    bullet.kill()
                    asteroid.kill()
                    break
         
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
