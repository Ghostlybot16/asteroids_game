import pygame
import pytest

from asteroids.actors.asteroid import Asteroid
from asteroids.constants import ASTEROID_MIN_RADIUS


@pytest.fixture
def asteroid_group():
    group = pygame.sprite.Group()
    Asteroid.containers = (group,)
    
    yield group
    
    del Asteroid.containers


def test_small_asteroid_is_destroyed_when_split(asteroid_group) -> None:
    asteroid = Asteroid(
        100,
        100,
        ASTEROID_MIN_RADIUS,
    )
    
    assert asteroid.alive()
    
    asteroid.split()
    
    assert not asteroid.alive()
    assert len(asteroid_group) == 0


def test_large_asteroid_splits_into_two_smaller_asteroids(asteroid_group) -> None:
    asteroid = Asteroid(
        100,
        100,
        ASTEROID_MIN_RADIUS * 3,
    )
    
    asteroid.velocity = pygame.Vector2(100, 0)
    
    asteroid.split()
    
    assert len(asteroid_group) == 2
    
    for child in asteroid_group:
        assert child.radius == ASTEROID_MIN_RADIUS * 2
        assert child.position == pygame.Vector2(100, 100)


def test_split_asteroids_move_faster(asteroid_group) -> None:
    asteroid = Asteroid(
        100,
        100,
        ASTEROID_MIN_RADIUS * 3,
    )
    
    asteroid.velocity = pygame.Vector2(100, 0)
    
    original_speed = asteroid.velocity.length()
    
    asteroid.split()
    
    for child in asteroid_group:
        assert child.velocity.length() == pytest.approx(
            original_speed * 1.2
        )