import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_KINDS, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_SPAWN_RATE
from player import Player

def main():
    pygame.init()
    
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pygame.display.set_caption("Asteroids") # Webapp title
    
    clock = pygame.time.Clock()
    dt = 0
    
    player = Player(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2))
    
    
    running = True   
    while running:
        # Make the window's close button work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        player.update(dt)
        
        # Fill black background 
        screen.fill((0, 0, 0))
        
        player.draw(screen)
        
        pygame.display.flip()
        
        # Limit to 60 fps and convert delta time from milliseconds to seconds
        dt = clock.tick(60) / 1000
    
    pygame.quit()

if __name__ == "__main__":
    main()
