import pygame 

from asteroids.engine.circleshape import CircleShape


class ConcreteCircle(CircleShape):
    def draw(self, screen: pygame.Surface) -> None:
        pass

    def update(self, dt: float) -> None:
        pass
    
def test_collision_when_circles_overlap() -> None:
    circle1 = ConcreteCircle(0, 0, 10)
    circle2 = ConcreteCircle(15, 0, 10)
    
    assert circle1.collision_check(circle2) is True

def test_no_collision_when_circles_are_separate() -> None:
    circle1 = ConcreteCircle(0, 0, 10)
    circle2 = ConcreteCircle(25, 0, 10)
    
    assert circle1.collision_check(circle2) is False

def test_collision_when_circle_edges_touch() -> None:
    circle1 = ConcreteCircle(0, 0, 10)
    circle2 = ConcreteCircle(20, 0, 10)
    
    assert circle1.collision_check(circle2) is True