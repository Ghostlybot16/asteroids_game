from asteroids.actors.asteroid import Asteroid
from asteroids.constants import ASTEROID_MIN_RADIUS
from asteroids.game import Game

def test_small_asteroid_awards_150_points() -> None:
    asteroid = Asteroid(
        0,
        0,
        ASTEROID_MIN_RADIUS,
    )
    
    assert Game.score_for_asteroid(asteroid) == 150


def test_medium_asteroid_awards_100_points() -> None:
    asteroid = Asteroid(
        0,
        0,
        ASTEROID_MIN_RADIUS * 2,
    )
    
    assert Game.score_for_asteroid(asteroid) == 100


def test_large_asteroid_awards_50_points() -> None:
    asteroid = Asteroid(
        0,
        0,
        ASTEROID_MIN_RADIUS * 3,
    )
    
    assert Game.score_for_asteroid(asteroid) == 50