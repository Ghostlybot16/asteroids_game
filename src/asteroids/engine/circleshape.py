"""Base circle-shaped game entity.

This module defines `CircleShape`, a lightweight base class for circular 
game objects (e.g., the player ship's hitbox, asteroids). It centralizes:

- **Position/velocity** storage via `pygame.Vector2`
- **Radius** for circle-based collision
- a **collision check** helper for circle-circle intersection

Subclasses are expected to override:
- `draw(self, screen)` to render themselves
- `update(self, dt)` to advance their state frame
"""

import pygame 



class CircleShape(pygame.sprite.Sprite):
    """ A circular game object with position, velocity and radius.
    
    This class also participates in `pygame.sprite.Group` management using a 
    class attribute called `containers`.
    
    Attributes
    ----------
    position : pygame.Vector2
        Center of the circle in screen coordinates (pixels)
    velocity : pygame.Vector2
        Per-second motion vector (pixels/seconds)
    radius : float | int
        Circle radius in pixels; used for collision check and regularly for drawing.
    """
    
    def __init__(self, x: float, y: float, radius: float) -> None:
        """Construct a circle at (x, y) with the given radius.
        
        Parameters
        ----------
        x : float
            Initial x-coordinate of the circle center (pixels).
        y : float 
            Initial y-coordinate of the circle center (pixels).
        radius : float 
            Circle radius (pixels)
        """
        # Auto-add to groups if the subclass set `containers` on the class.
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        # Physics state (pixels, pixels/second).
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        
        # Collision/draw size (pixels).
        self.radius = radius
        
    
    
    
    # Hooks for subclasses 
    def draw(self, screen: pygame.surface) -> None:
        """Render this object tot he given screen.
        
        Parameters
        ----------
        screen: pygame.Surface
            The target surface (the main display surface).
        """
        pass


    def update(self, dt: float) -> None:
        """Advance this object's simulation by `dt` seconds.
        
        Parameters
        ----------
        dt: float
            Delta time in **seconds** since the previous frame.
        """
        pass
    
    
    
    
    def collision_check(self, another_circle: "CircleShape") -> bool:
        """Return True if this circle intersects `another_circle`.
        
        Uses circle-circle collition: two circles overlap when the distance
        between centers is less than or equal to the sum of their radii.
        
        Parameters
        ----------
        another_circle : CircleShape
            Another circle-shaped object to test against.
        
        Returns
        -------
        bool 
            True if the two circles intersect (collide), False otherwise.
        """
        distance_between_circles = self.position.distance_to(another_circle.position)
        circle_radii = self.radius + another_circle.radius # radii -> plural for radius
        
        return distance_between_circles <= circle_radii
    
                