"""
src/entities/particle.py
=========================
Visual-only particles for explosions, thrust trails, and hit sparks.
"""

import pygame
import random
import math
from src.settings import Settings as S


class Particle:
    """A single particle — not a Sprite, updated & drawn manually for speed."""

    __slots__ = ("x", "y", "vx", "vy", "colour", "size", "alpha", "lifetime", "age", "gravity")

    def __init__(
        self,
        x: float, y: float,
        colour: tuple,
        speed: float   = 3.0,
        size: int      = 4,
        lifetime: int  = S.PARTICLE_LIFETIME_MS,
        angle: float   = None,
        gravity: float = 0.05,
    ):
        self.x        = x
        self.y        = y
        self.colour   = colour
        self.size     = size
        self.alpha    = 255
        self.lifetime = lifetime
        self.age      = 0
        self.gravity  = gravity

        if angle is None:
            angle = random.uniform(0, math.pi * 2)
        speed *= random.uniform(0.4, 1.6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def update(self, dt: float = 16.67) -> bool:
        """Advance particle by dt ms. Returns True while alive."""
        self.age  += dt
        ratio      = self.age / self.lifetime
        self.x    += self.vx
        self.y    += self.vy
        self.vy   += self.gravity
        self.vx   *= 0.97
        self.alpha = max(0, int(255 * (1 - ratio)))
        self.size  = max(1, int(self.size * (1 - ratio * 0.5)))
        return self.age < self.lifetime

    def draw(self, surface: pygame.Surface):
        if self.alpha <= 0 or self.size <= 0:
            return
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.colour, self.alpha), (self.size, self.size), self.size)
        surface.blit(surf, (int(self.x) - self.size, int(self.y) - self.size))


def make_explosion(x: float, y: float, colour: tuple, count: int = S.EXPLOSION_PARTICLES) -> list:
    """Factory: burst of particles radiating outward."""
    particles = []
    for _ in range(count):
        p = Particle(x, y, colour, speed=random.uniform(1.5, 5), size=random.randint(2, 6))
        particles.append(p)
    # Add a few white sparks
    for _ in range(count // 4):
        p = Particle(x, y, S.WHITE, speed=random.uniform(3, 8), size=random.randint(1, 3), lifetime=300)
        particles.append(p)
    return particles


def make_trail(x: float, y: float, colour: tuple) -> list:
    """Factory: small trail particles (for ship thrust)."""
    particles = []
    for _ in range(S.TRAIL_PARTICLES):
        p = Particle(
            x + random.uniform(-4, 4), y + random.uniform(0, 8),
            colour,
            speed=random.uniform(0.5, 2.0),
            size=random.randint(1, 3),
            lifetime=250,
            angle=random.uniform(math.pi * 0.4, math.pi * 0.6),
        )
        particles.append(p)
    return particles