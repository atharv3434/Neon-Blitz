"""
src/systems/background.py
==========================
Parallax scrolling starfield background with nebula colour wash.
"""

import pygame
import random
import math
from src.settings import Settings as S


class Background:
    """
    Multi-layer parallax starfield.

    Three layers of stars scroll at different speeds,
    with occasional coloured nebula patches.
    """

    def __init__(self):
        self._stars   = self._init_stars()
        self._nebulas = self._init_nebulas()
        self._tick    = 0

    def _init_stars(self) -> list:
        stars = []
        for _ in range(S.NUM_STARS):
            layer = random.randint(0, 2)
            speed = S.STAR_SPEED_RANGE[0] + (layer / 2) * (S.STAR_SPEED_RANGE[1] - S.STAR_SPEED_RANGE[0])
            speed += random.uniform(-0.2, 0.2)
            brightness = 80 + layer * 60 + random.randint(-20, 20)
            brightness = max(40, min(255, brightness))
            size = layer + 1
            stars.append({
                "x":     random.randint(0, S.WIDTH),
                "y":     random.uniform(0, S.HEIGHT),
                "speed": speed,
                "size":  size,
                "colour": (brightness, brightness, min(255, brightness + 30)),
                "twinkle": random.uniform(0, math.pi * 2),
            })
        return stars

    def _init_nebulas(self) -> list:
        nebulas = []
        colours = [
            (30, 0, 60, 18),
            (0, 20, 50, 15),
            (40, 0, 20, 12),
        ]
        for c in colours:
            nebulas.append({
                "x": random.randint(0, S.WIDTH),
                "y": random.uniform(0, S.HEIGHT),
                "w": random.randint(200, 400),
                "h": random.randint(100, 250),
                "colour": c,
                "speed":  0.15,
            })
        return nebulas

    def update(self):
        self._tick += 1
        for star in self._stars:
            star["y"] += star["speed"]
            if star["y"] > S.HEIGHT:
                star["y"] = -2
                star["x"] = random.randint(0, S.WIDTH)
        for neb in self._nebulas:
            neb["y"] += neb["speed"]
            if neb["y"] > S.HEIGHT + neb["h"]:
                neb["y"] = -neb["h"]
                neb["x"] = random.randint(0, S.WIDTH)

    def draw(self, surface: pygame.Surface):
        surface.fill(S.BG_DARK)
        self._draw_nebulas(surface)
        self._draw_stars(surface)

    def _draw_nebulas(self, surface):
        for neb in self._nebulas:
            s = pygame.Surface((neb["w"], neb["h"]), pygame.SRCALPHA)
            r, g, b, a = neb["colour"]
            # Radial gradient effect via concentric ellipses
            for i in range(5, 0, -1):
                scale = i / 5
                w = int(neb["w"] * scale)
                h = int(neb["h"] * scale)
                rect = pygame.Rect(
                    neb["w"] // 2 - w // 2,
                    neb["h"] // 2 - h // 2,
                    w, h
                )
                colour = (r, g, b, int(a * (1 - scale * 0.6)))
                pygame.draw.ellipse(s, colour, rect)
            surface.blit(s, (int(neb["x"]), int(neb["y"])))

    def _draw_stars(self, surface):
        for star in self._stars:
            twinkle_alpha = int(180 + math.sin(self._tick * 0.05 + star["twinkle"]) * 75)
            r, g, b = star["colour"]
            col = (
                min(255, int(r * twinkle_alpha / 255)),
                min(255, int(g * twinkle_alpha / 255)),
                min(255, int(b * twinkle_alpha / 255)),
            )
            if star["size"] == 1:
                surface.set_at((int(star["x"]), int(star["y"])), col)
            else:
                pygame.draw.circle(surface, col, (int(star["x"]), int(star["y"])), star["size"])