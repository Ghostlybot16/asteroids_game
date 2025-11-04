import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_KINDS, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_SPAWN_RATE

def main():
    pygame.init()
    
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    
    
    running = True   
    while running:
        # Make the window's close button work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Fill black background 
        screen.fill((0, 0, 0))
        pygame.display.flip()
    
    pygame.quit()


    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
