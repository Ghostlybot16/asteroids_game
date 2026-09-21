import pygame

from asteroids.engine.circleshape import CircleShape 
from asteroids.constants import (
    PLAYER_RADIUS, 
    PLAYER_SHOOT_COOLDOWN, 
    PLAYER_SHOOT_SPEED, 
    PLAYER_SPEED, 
    PLAYER_TURN_SPEED
)
from asteroids.actors.shot import Shot


class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0.0
        self.shoot_timer = 0.0
        
        # post-respawn invulnerability 
        self.is_invulnerable = False
        self.invulnerable_timer = 0.0
    
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        
        
        right = (
            pygame.Vector2(0, 1).rotate(self.rotation + 90) 
            * self.radius 
            / 1.5
        )
        
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        
        return [a, b, c]
    
    def draw(self, screen: pygame.Surface) -> None:
        # Normal = green, invulnerable = Blueish
        color = (0, 255, 0)
        
        if self.is_invulnerable:
            color = (100, 100, 255)
        
        pygame.draw.polygon(
            surface=screen, 
            color=color, 
            points=self.triangle(), 
            width=2
        )
    
    def rotate(self, dt: float) -> None:
        self.rotation += (PLAYER_TURN_SPEED * dt) 
        
    def update_timer(self, dt: float) -> None:
        """Update the player's cooldown and invulnerability timers."""
        
        if self.shoot_timer > 0:
            self.shoot_timer = max(
                0.0,
                self.shoot_timer - dt,
            )
        
        if self.invulnerable_timer > 0:
            self.invulnerable_timer = max(
                0.0, 
                self.invulnerable_timer - dt,
            )
            
            if self.invulnerable_timer == 0:
                self.is_invulnerable = False
    
    def update(self, dt: float) -> None:
        """Update the player based on input and elapsed time."""
        
        keys = pygame.key.get_pressed()
        
        # Rotate Left or Right
        if keys[pygame.K_a]:
            self.rotate(-dt)
            
        if keys[pygame.K_d]:
            self.rotate(dt)
        
        # Move Up or Down
        if keys[pygame.K_w]:
            self.move(dt)
            
        if keys[pygame.K_s]:
            self.move(-dt)
        
        self.update_timer(dt)
        
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        
    def move(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        
        # Spawn the bullets at the tip of the triangle
        bullet_spawn_pos = self.position + forward * (self.radius * 2)
        
        shot = Shot(bullet_spawn_pos.x, bullet_spawn_pos.y)
        
        shot.velocity = forward * PLAYER_SHOOT_SPEED
    
    def make_invulnerable(self, duration: float) -> None:
        """Make the player invulnerable for `duration` seconds."""
        self.is_invulnerable = True
        self.invulnerable_timer = duration
        

