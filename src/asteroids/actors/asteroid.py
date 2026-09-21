import random

import pygame

from asteroids.engine.circleshape import CircleShape
from asteroids.constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(
        self, 
        x: float, 
        y: float, 
        radius: float
    ) -> None:
        super().__init__(x, y, radius)
    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            surface=screen, 
            color="white", 
            center=self.position, 
            radius=self.radius, 
            width=2
        )
    
    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)
    
    def split(self) -> None:
        self.kill()
        
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20, 50)
        
        split_velocity1 = self.velocity.rotate(random_angle)
        split_velocity2 = self.velocity.rotate(-random_angle)
        
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        asteroid1 = Asteroid(
            self.position.x, 
            self.position.y,
            new_radius
        )
        asteroid1.velocity = split_velocity1 * 1.2
        
        asteroid2 = Asteroid(
            self.position.x, 
            self.position.y, 
            new_radius
        )
        asteroid2.velocity = split_velocity2 * 1.2

