"""
Neon Blitz — Arcade Space Shooter
===================================
Package root. Exposes version and top-level game factory.

    from src import __version__, create_game
    game = create_game()
    game.run()
"""

__version__  = "1.0.0"
__title__    = "Neon Blitz"
__author__   = "Neon Blitz Team"
__license__  = "MIT"

from src.settings import Settings   # noqa: F401  (make importable from src)


def create_game(fullscreen: bool = False):
    """Convenience factory — import-safe (pygame not initialised yet)."""
    from src.game import Game
    return Game(fullscreen=fullscreen)


__all__ = ["__version__", "__title__", "__author__", "Settings", "create_game"]