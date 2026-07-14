"""
src/entities/__init__.py
========================
Entities package — all game objects that exist in the world.

Exports
-------
    Player      — the player's ship
    Drone, Zigzagger, Diver, Tank, Swarmer, Boss
                — enemy ship variants
    Bullet, EnemyBullet
                — projectiles
    PowerUp     — collectible power-up items
    Particle    — visual-only explosion & trail particles

Usage
-----
    from src.entities import Player, Drone, PowerUp, Particle
"""

from src.entities.player   import Player
from src.entities.enemies  import Drone, Zigzagger, Diver, Tank, Swarmer, Boss
from src.entities.bullet   import Bullet, EnemyBullet
from src.entities.powerup  import PowerUp
from src.entities.particle import Particle

__all__ = [
    "Player",
    "Drone", "Zigzagger", "Diver", "Tank", "Swarmer", "Boss",
    "Bullet", "EnemyBullet",
    "PowerUp",
    "Particle",
]