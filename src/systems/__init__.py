"""
src/systems/__init__.py
========================
Systems package — stateless (or lightly stateful) subsystems that
operate on collections of entities rather than individual objects.

Exports
-------
    WaveManager     — controls enemy spawning per wave
    CollisionSystem — detects and resolves collisions
    HUD             — renders heads-up display
    Background      — scrolling parallax starfield
"""

from src.systems.wave_manager import WaveManager
from src.systems.collision    import CollisionSystem
from src.systems.hud          import HUD
from src.systems.background   import Background

__all__ = ["WaveManager", "CollisionSystem", "HUD", "Background"]