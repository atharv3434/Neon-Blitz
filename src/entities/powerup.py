"""
src/entities/powerup.py
========================
Collectible power-up items that drop from defeated enemies.
"""

import pygame
import random
import math
from src.settings import Settings as S


POWERUP_TYPES = {
    "shield": {"colour": S.NEON_BLUE,   "icon": "🛡", "label": "SHIELD"},
    "rapid":  {"colour": S.NEON_RED,    "icon": "⚡", "label": "RAPID FIRE"},
    "triple": {"colour": S.NEON_YELLOW, "icon": "✦",  "label": "TRIPLE SHOT"},
    "bomb":   {"colour": S.NEON_PURPLE, "icon": "💣", "label": "BOMB"},
    "life":   {"colour": S.NEON_GREEN,  "icon": "♥",  "label": "+1 LIFE"},
    "speed":  {"colour": S.WHITE,       "icon": "↑",  "label": "SPEED"},
}

# Spawn weights — life and bomb are rarer
SPAWN_WEIGHTS = [0.25, 0.22, 0.20, 0.08, 0.10, 0.15]
SPAWN_KEYS    = ["shield", "rapid", "triple", "bomb", "life", "speed"]


class PowerUp(pygame.sprite.Sprite):
    """A floating, pulsing power-up orb."""

    def __init__(self, x: int, y: int, ptype: str = None):
        super().__init__()
        self.ptype  = ptype or random.choices(SPAWN_KEYS, weights=SPAWN_WEIGHTS)[0]
        self._cfg   = POWERUP_TYPES[self.ptype]
        self._tick  = 0
        self._base_y = y

        self.image  = self._draw()
        self.rect   = self.image.get_rect(center=(x, y))

    def _draw(self) -> pygame.Surface:
        size = 32
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        c    = self._cfg["colour"]
        # Outer glow ring
        pygame.draw.circle(surf, (*c, 60), (size//2, size//2), size//2)
        # Main circle
        pygame.draw.circle(surf, c,       (size//2, size//2), size//2 - 4)
        pygame.draw.circle(surf, S.WHITE, (size//2, size//2), size//2 - 4, 1)
        # Inner white highlight
        pygame.draw.circle(surf, S.WHITE, (size//2 - 5, size//2 - 5), 4)
        return surf

    def update(self):
        self._tick += 1
        # Float downward + gentle bob
        self.rect.y   = self._base_y + self._tick * S.POWERUP_SPEED
        self.rect.x   += math.sin(self._tick * 0.08) * 0.8

        # Pulse: redraw with varying alpha
        if self._tick % 8 == 0:
            pulse_alpha = int(180 + math.sin(self._tick * 0.15) * 75)
            self.image  = self._draw()
            self.image.set_alpha(pulse_alpha)

        if self.rect.top > S.HEIGHT + 20:
            self.kill()

    def get_label(self) -> str:
        return self._cfg["label"]

    def get_colour(self) -> tuple:
        return self._cfg["colour"]

    def draw_label(self, surface: pygame.Surface):
        """Draw a small label below the power-up orb."""
        try:
            font = pygame.font.SysFont("consolas", 10, bold=True)
            txt  = font.render(self._cfg["label"], True, self._cfg["colour"])
            x    = self.rect.centerx - txt.get_width() // 2
            y    = self.rect.bottom + 2
            surface.blit(txt, (x, y))
        except Exception:
            pass