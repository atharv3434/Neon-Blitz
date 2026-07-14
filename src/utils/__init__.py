"""
src/utils/__init__.py
======================
Utilities package — helper modules with no game-state dependencies.

Exports
-------
    ScoreManager    — saves/loads high scores to JSON
    SoundManager    — procedurally generates sound effects via pygame
    draw_glow_text  — renders text with a neon glow halo
    draw_glow_rect  — renders a rectangle with glow border
"""

from src.utils.score    import ScoreManager
from src.utils.sounds   import SoundManager
from src.utils.renderer import draw_glow_text, draw_glow_rect

__all__ = [
    "ScoreManager",
    "SoundManager",
    "draw_glow_text",
    "draw_glow_rect",
]