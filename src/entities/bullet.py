"""
src/entities/bullet.py
=======================
Player and enemy projectiles.
"""

import pygame
import math
from src.settings import Settings as S


class Bullet(pygame.sprite.Sprite):
    """Player laser bolt, optionally at an angle (triple shot)."""

    def __init__(self, x: int, y: int, angle_rad: float = 0):
        super().__init__()
        self.image = pygame.Surface((S.BULLET_WIDTH, S.BULLET_HEIGHT), pygame.SRCALPHA)
        # Neon glow layered bullet
        pygame.draw.rect(self.image, S.NEON_CYAN,  (1, 0,  S.BULLET_WIDTH-2, S.BULLET_HEIGHT))
        pygame.draw.rect(self.image, S.WHITE,       (S.BULLET_WIDTH//2-1, 0, 2, S.BULLET_HEIGHT//2))
        self.rect   = self.image.get_rect(center=(x, y))
        self._vx    = math.sin(angle_rad) * S.PLAYER_BULLET_SPEED
        self._vy    = -math.cos(angle_rad) * S.PLAYER_BULLET_SPEED

    def update(self):
        self.rect.x += self._vx
        self.rect.y += self._vy
        if self.rect.bottom < 0 or self.rect.left > S.WIDTH or self.rect.right < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    """Enemy projectile aimed at the player position."""

    def __init__(self, x: int, y: int, target: tuple):
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, S.NEON_RED,    (4, 4), 4)
        pygame.draw.circle(self.image, S.NEON_ORANGE, (4, 4), 2)
        self.rect = self.image.get_rect(center=(x, y))

        if target:
            dx = target[0] - x
            dy = target[1] - y
            dist = max(1, math.hypot(dx, dy))
            self._vx = dx / dist * S.ENEMY_BULLET_SPEED
            self._vy = dy / dist * S.ENEMY_BULLET_SPEED
        else:
            self._vx = 0
            self._vy = S.ENEMY_BULLET_SPEED

    def update(self):
        self.rect.x += self._vx
        self.rect.y += self._vy
        if (self.rect.top > S.HEIGHT or self.rect.bottom < 0 or
                self.rect.left > S.WIDTH or self.rect.right < 0):
            self.kill()