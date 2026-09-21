import pygame

from asteroids.engine.circleshape import CircleShape
from asteroids.constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)
    
    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            surface=screen,
            color="red",
            center=self.position,
            radius=self.radius,
            width=2
        )
    
    def update(self, dt: float) -> None:
        self.position += self.velocity * dt