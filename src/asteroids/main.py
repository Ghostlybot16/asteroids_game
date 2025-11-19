"""Asteroids: game bootstrap and main loop.

This module initializes pygame, creates sprite groups for update/draw,
spawns the Player at screen center, and runs the fixed-timestep render loop.
"""


import pygame
from asteroids.constants import (
    SCREEN_HEIGHT, 
    SCREEN_WIDTH, 
    CENTER_SCREEN_WIDTH,
    CENTER_SCREEN_HEIGHT,
    ASTEROID_MIN_RADIUS,
    ASTEROID_KINDS,
    PLAYER_INITIAL_LIVES
)
from asteroids.actors.player import Player
from asteroids.actors.asteroid import Asteroid
from asteroids.actors.shoot import Shot
from asteroids.systems.asteroidfield import AsteroidField


def score_for_asteroid(asteroid: Asteroid) -> int:
    """Return how many points the player gets for destroying an asteroid
    
    - Big asteroids are worth fewer points 
    - Small asteroids are worth more points (harder to hit)
    """
    
    # Make sure the size category stays in a safe range even if the radius is a bit off 
    # Prevents radii like 19.999 / 41.3
    approximate_size_step = int(asteroid.radius // ASTEROID_MIN_RADIUS)
    
    # Clamp asteroid size to always stay between 1 and ASTEROID_KINDS value.
    size_step = max(1, approximate_size_step)
    size_step = min(size_step, ASTEROID_KINDS)
    
    # Convert the size step into points 
    points_per_step = 50
    points = (ASTEROID_KINDS - size_step + 1) * points_per_step
    
    return points


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
    
    # Scoring
    score = 0
    font = pygame.font.Font(None, 48) # Default font, 48px for better visibility
    
    # Player lives 
    lives = PLAYER_INITIAL_LIVES
    
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
    player = Player(CENTER_SCREEN_WIDTH, CENTER_SCREEN_HEIGHT)
    
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
            if player.is_invulnerable: # Skip collision chceks if player is invulnerable
                continue
            
            if asteroid.collision_check(player): # Lose a live after collision with asteroid
                lives -= 1 
                
                if lives <= 0:
                    print("Game Over!")
                    pygame.quit()
                    return

                # Respawn player at center with no velocity and reset rotation
                player.position.update(CENTER_SCREEN_WIDTH, CENTER_SCREEN_HEIGHT)
                player.velocity.update(0, 0)
                player.rotation = 0
                
                # Brief invulnerability after respawn (2 seconds)
                player.make_invulnerable(2.0)
                
                break
        
        for asteroid in asteroids.sprites():  
            for bullet in shots.sprites():
                if asteroid.collision_check(bullet): 
                # If bullet and asteroids collide, delete bullet from screen and split asteroid
                    
                    bullet.kill()
                    
                    # Increase score based on asteroid size BEFORE split 
                    score += score_for_asteroid(asteroid)
                    
                    asteroid.split()
                    break
         
        # --- Rendering ---
        # Fill black background 
        screen.fill((0, 0, 0))
        
        
        for sprite in drawable:
            sprite.draw(screen)
        
        
        # Draw HUD (Score + Lives)
        hud_color = (0, 255, 255)
        
        score_text = font.render(f"Score: {score}", True, hud_color)
        lives_text = font.render(f"Lives: {lives}", True, hud_color)
        
        score_rect = score_text.get_rect()
        lives_rect = lives_text.get_rect()
        
        # Position text lines
        score_rect.topleft = (30, 20) # away from top-left corner
        lives_rect.topleft = (30, score_rect.bottom + 8)
        
        # Create background box around the text 
        padding = 12
        hud_width = max(score_rect.width, lives_rect.width) + padding * 2
        hud_height = (lives_rect.bottom - score_rect.top) + padding * 2
        hud_rect = pygame.Rect(
            score_rect.left - padding, 
            score_rect.top - padding,
            hud_width,
            hud_height, 
        )
        
        # Draw HUD background and border 
        pygame.draw.rect(screen, (20, 20, 20), hud_rect) # dark grey background
        pygame.draw.rect(screen, hud_color, hud_rect, 2) # cyan border
        
        screen.blit(score_text, score_rect)
        screen.blit(lives_text, lives_rect)
        
        
        pygame.display.flip() # Present the frame to the screen
        
        # Limit to 60 FPS and convert delta time from milliseconds to seconds
        dt = clock.tick(60) / 1000
    
    pygame.quit()

if __name__ == "__main__":
    main()
