"""
src/systems/collision.py
=========================
Collision detection and resolution between all game entities.
"""

import pygame
import random
from src.settings import Settings as S
from src.entities.particle import make_explosion, make_trail
from src.entities.powerup  import PowerUp


class CollisionSystem:
    """Handles all collision checks each frame. Returns event lists."""

    def check_all(
        self,
        player,
        player_bullets: pygame.sprite.Group,
        enemies:        pygame.sprite.Group,
        enemy_bullets:  pygame.sprite.Group,
        powerups:       pygame.sprite.Group,
    ) -> dict:
        """
        Run all collision checks.

        Returns
        -------
        dict with keys:
            score_delta   : int  — points earned this frame
            particles     : list — new Particle objects to add
            new_powerups  : list — PowerUp objects to add
            bomb_triggered: bool — bomb power-up was collected
            player_hit    : bool — player was struck
            life_lost     : bool — player lost a life
        """
        result = {
            "score_delta":    0,
            "particles":      [],
            "new_powerups":   [],
            "bomb_triggered": False,
            "player_hit":     False,
            "life_lost":      False,
        }

        # 1. Player bullets → enemies
        hits = pygame.sprite.groupcollide(player_bullets, enemies, True, False)
        for bullet, hit_enemies in hits.items():
            for enemy in hit_enemies:
                destroyed = enemy.take_hit(1)
                colour = getattr(enemy, "colour", S.NEON_RED)
                result["particles"].extend(
                    make_explosion(enemy.rect.centerx, enemy.rect.centery, colour,
                                   count=10 if destroyed else 4)
                )
                if destroyed:
                    result["score_delta"] += enemy.points
                    # Chance to drop power-up
                    if random.random() < S.POWERUP_SPAWN_CHANCE:
                        result["new_powerups"].append(
                            PowerUp(enemy.rect.centerx, enemy.rect.centery)
                        )

        # 2. Player → power-ups
        pu_hits = pygame.sprite.spritecollide(player, powerups, True)
        for pu in pu_hits:
            outcome = player.apply_powerup(pu.ptype)
            if outcome == "bomb":
                result["bomb_triggered"] = True
                # Explode all enemies
                for e in list(enemies):
                    result["particles"].extend(
                        make_explosion(e.rect.centerx, e.rect.centery, e.colour, count=20)
                    )
                    result["score_delta"] += e.points
                    e.kill()

        # 3. Enemy bullets → player
        if not player.invincible:
            eb_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
            if eb_hits:
                result["player_hit"] = True
                life_lost = player.hit()
                result["life_lost"] = life_lost
                result["particles"].extend(
                    make_explosion(player.rect.centerx, player.rect.centery,
                                   S.NEON_CYAN, count=15)
                )

        # 4. Enemies → player (body collision)
        if not player.invincible:
            body_hits = pygame.sprite.spritecollide(player, enemies, False,
                                                     pygame.sprite.collide_circle_ratio(0.6))
            if body_hits:
                result["player_hit"] = True
                life_lost = player.hit()
                result["life_lost"] = life_lost
                for e in body_hits:
                    result["particles"].extend(
                        make_explosion(e.rect.centerx, e.rect.centery, e.colour, count=20)
                    )
                    e.kill()

        return result