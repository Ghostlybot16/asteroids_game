import pygame 

from asteroids.constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    CENTER_SCREEN_WIDTH,
    CENTER_SCREEN_HEIGHT,
    ASTEROID_MIN_RADIUS,
    ASTEROID_KINDS,
    PLAYER_INITIAL_LIVES,
)
from asteroids.actors.player import Player
from asteroids.actors.asteroid import Asteroid
from asteroids.actors.shot import Shot
from asteroids.systems.asteroidfield import AsteroidField


class Game:
    def __init__(self) -> None:
        pygame.init()
        
        # Display 
        self.screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(title="Asteroids")
        
        # Timing
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.running = True

        # Game State 
        self.score = 0
        self.lives = PLAYER_INITIAL_LIVES
        
        # HUD 
        self.font = pygame.font.Font(None, 48)
        
        # Sprite Groups 
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        
        # Register sprite containers 
        Player.containers = (
            self.updatable,
            self.drawable,
        )
        
        Asteroid.containers = (
            self.asteroids,
            self.updatable,
            self.drawable,
        )
        
        AsteroidField.containers = (
            self.updatable,
        )
        
        Shot.containers = (
            self.shots,
            self.updatable,
            self.drawable,
        )
        
        # Create game objects
        self.player = Player(
            x=CENTER_SCREEN_WIDTH,
            y=CENTER_SCREEN_HEIGHT,
        )
        
        self.asteroid_field = AsteroidField()
    
    def respawn_player(self) -> None:
        """Reset the player after losing a life."""
        
        self.player.position.update(x=CENTER_SCREEN_WIDTH, y=CENTER_SCREEN_HEIGHT)
        
        self.player.velocity.update(x=0, y=0)
        self.player.rotation = 0
        
        self.player.make_invulnerable(duration=2.0)
    
    @staticmethod
    def score_for_asteroid(asteroid: Asteroid) -> int:
        """Return the points awarded for destroying an asteroid."""
        
        approximate_size_step = int(asteroid.radius // ASTEROID_MIN_RADIUS)
        
        size_step = max(1, approximate_size_step)
        size_step = min(size_step, ASTEROID_KINDS)
        
        points_per_step = 50
        
        points = (ASTEROID_KINDS - size_step + 1) * points_per_step
        
        return points
    
    def handle_player_collisions(self) -> None:
        """Handle collisions between the player and asteroids."""
        
        # Dont check collisions while the player is temporarily invulnerable.
        if self.player.is_invulnerable:
            return 
        
        for asteroid in self.asteroids:
            if asteroid.collision_check(self.player):
                self.lives -= 1
                
                if self.lives <= 0:
                    print("Game Over!")
                    self.running = False
                    return
                
                self.respawn_player()
                return
    
    def handle_shot_collisions(self) -> None:
        """Handle collisions between shots and asteroids"""
        
        for asteroid in self.asteroids.sprites():
            for shot in self.shots.sprites():
                if asteroid.collision_check(shot):
                    shot.kill()
                    
                    self.score += self.score_for_asteroid(asteroid)
                    
                    asteroid.split()
                    break
    
    def handle_collisions(self) -> None:
        """Abstraction method, Handle all game collisions."""
        
        self.handle_player_collisions()
        self.handle_shot_collisions()
    
    def handle_events(self) -> None:
        """Process Pygame events."""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self) -> None:
        """Update all game objects."""
        
        self.updatable.update(self.dt)
        self.handle_collisions()
    
    def draw_hud(self) -> None:
        """Draw the player's score and remaining lives"""
        
        hud_color = (0, 255, 255)
        
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            hud_color,
        )
        
        lives_text = self.font.render(
            f"Lives: {self.lives}",
            True,
            hud_color,
        )
        
        score_rect = score_text.get_rect()
        lives_rect = lives_text.get_rect()
        
        score_rect.topleft = (30, 20)
        lives_rect.topleft = (
            30,
            score_rect.bottom + 8,
        )
        
        padding = 12
        
        hud_width = (
            max(score_rect.width, lives_rect.width)
            + padding * 2
        )
        
        hud_height = (
            lives_rect.bottom - score_rect.top
            + padding * 2
        )
        
        hud_rect = pygame.Rect(
            score_rect.left - padding,
            score_rect.top - padding,
            hud_width,
            hud_height,
        )
        
        pygame.draw.rect(
            surface=self.screen,
            color=(20, 20, 20),
            rect=hud_rect,
        )
        
        pygame.draw.rect(
            surface=self.screen,
            color=hud_color,
            rect=hud_rect,
            width=2
        )
        
        self.screen.blit(score_text, score_rect)
        self.screen.blit(lives_text, lives_rect)
    
    def draw(self) -> None:
        """Render the current game state"""
        
        self.screen.fill((0, 0, 0))
        
        for sprite in self.drawable:
            sprite.draw(self.screen)
        
        self.draw_hud()
        
        pygame.display.flip()
    
    def run(self) -> None:
        """Run the main game loop"""
        
        while self.running:
            self.handle_events()
            
            if not self.running:
                break

            self.update()
            self.draw()
            
            self.dt = self.clock.tick(60) / 1000
        
        pygame.quit()