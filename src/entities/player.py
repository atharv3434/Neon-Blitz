"""
src/entities/player.py
=======================
Player ship entity with movement, shooting, shield, and power-up state.
"""

import pygame
import math
import time
from src.settings import Settings as S


class Player(pygame.sprite.Sprite):
    """
    The player-controlled ship.

    Attributes
    ----------
    lives         : remaining lives
    score         : current session score
    shield_active : shield power-up active
    rapid_fire    : rapid fire power-up active
    triple_shot   : triple shot power-up active
    speed_boost   : speed boost power-up active
    """

    def __init__(self):
        super().__init__()
        self.image_orig = self._draw_ship()
        self.image      = self.image_orig.copy()
        self.rect       = self.image.get_rect()
        self.rect.centerx = S.WIDTH // 2
        self.rect.bottom  = S.HEIGHT - 20

        # Physics
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.speed = S.PLAYER_SPEED

        # State
        self.lives          = S.PLAYER_LIVES
        self.score          = 0
        self.invincible     = False
        self._invincible_end = 0
        self._blink_timer   = 0

        # Shooting
        self._last_shot     = 0
        self.shoot_delay    = S.PLAYER_SHOOT_DELAY

        # Power-ups
        self.shield_active  = False
        self._shield_end    = 0
        self.rapid_fire     = False
        self._rapid_end     = 0
        self.triple_shot    = False
        self._triple_end    = 0
        self.speed_boost    = False
        self._speed_end     = 0

        # Thrust flame animation
        self._flame_frame   = 0
        self._flame_timer   = 0

    # ── Drawing ───────────────────────────────────────────────────────────────

    def _draw_ship(self) -> pygame.Surface:
        surf = pygame.Surface((S.PLAYER_WIDTH, S.PLAYER_HEIGHT), pygame.SRCALPHA)
        w, h = S.PLAYER_WIDTH, S.PLAYER_HEIGHT

        # Main body (cyan)
        body = [(w//2, 2), (w-6, h-12), (w//2, h-6), (6, h-12)]
        pygame.draw.polygon(surf, S.NEON_CYAN, body)
        pygame.draw.polygon(surf, S.WHITE, body, 1)

        # Cockpit (pink glow)
        pygame.draw.ellipse(surf, S.NEON_PINK, (w//2-8, h//2-14, 16, 18))
        pygame.draw.ellipse(surf, S.WHITE,     (w//2-8, h//2-14, 16, 18), 1)

        # Wing accents
        pygame.draw.line(surf, S.NEON_YELLOW, (6, h-12), (w//2-4, h//2), 2)
        pygame.draw.line(surf, S.NEON_YELLOW, (w-6, h-12), (w//2+4, h//2), 2)

        return surf

    def _draw_flame(self, surface: pygame.Surface):
        """Draw animated engine flame below the ship."""
        self._flame_timer += 1
        if self._flame_timer % 4 == 0:
            self._flame_frame = (self._flame_frame + 1) % 3
        flame_h = [10, 14, 10][self._flame_frame]
        cx = self.rect.centerx
        cy = self.rect.bottom
        pts = [(cx - 6, cy), (cx, cy + flame_h), (cx + 6, cy)]
        pygame.draw.polygon(surface, S.NEON_ORANGE, pts)
        inner = [(cx - 3, cy), (cx, cy + flame_h - 4), (cx + 3, cy)]
        pygame.draw.polygon(surface, S.NEON_YELLOW, inner)

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, keys: pygame.key.ScancodeWrapper):
        now = pygame.time.get_ticks()
        spd = self.speed * (1.5 if self.speed_boost else 1.0)

        # Movement
        dx = dy = 0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: dx -= spd
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += spd
        if keys[pygame.K_UP]    or keys[pygame.K_w]: dy -= spd
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: dy += spd

        # Diagonal normalise
        if dx and dy:
            dx *= 0.707
            dy *= 0.707

        self.rect.x = max(0, min(S.WIDTH  - self.rect.width,  self.rect.x + dx))
        self.rect.y = max(0, min(S.HEIGHT - self.rect.height, self.rect.y + dy))

        # Invincibility blink
        if self.invincible:
            if now >= self._invincible_end:
                self.invincible = False
                self.image = self.image_orig.copy()
            else:
                if (now // 100) % 2 == 0:
                    self.image = self.image_orig.copy()
                else:
                    blink = self.image_orig.copy()
                    blink.set_alpha(80)
                    self.image = blink

        # Power-up expiry
        if self.rapid_fire  and now >= self._rapid_end:
            self.rapid_fire  = False
            self.shoot_delay = S.PLAYER_SHOOT_DELAY
        if self.triple_shot and now >= self._triple_end:
            self.triple_shot = False
        if self.speed_boost and now >= self._speed_end:
            self.speed_boost = False
        if self.shield_active and now >= self._shield_end:
            self.shield_active = False

    def draw_extras(self, surface: pygame.Surface):
        """Draw flame + shield ring (called after sprite draw)."""
        self._draw_flame(surface)
        if self.shield_active:
            cx, cy = self.rect.centerx, self.rect.centery
            r = max(self.rect.width, self.rect.height) // 2 + 10
            pygame.draw.circle(surface, S.NEON_BLUE, (cx, cy), r, 2)
            alpha_surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(alpha_surf, (*S.NEON_BLUE, 30), (r, r), r)
            surface.blit(alpha_surf, (cx - r, cy - r))

    # ── Shooting ──────────────────────────────────────────────────────────────

    def can_shoot(self) -> bool:
        delay = S.PLAYER_RAPID_DELAY if self.rapid_fire else self.shoot_delay
        return pygame.time.get_ticks() - self._last_shot >= delay

    def shoot(self) -> list:
        """Return list of Bullet objects to add to the game."""
        from src.entities.bullet import Bullet
        self._last_shot = pygame.time.get_ticks()
        cx = self.rect.centerx
        top = self.rect.top + 4
        bullets = [Bullet(cx, top, 0)]
        if self.triple_shot:
            bullets.append(Bullet(cx, top, -0.35))
            bullets.append(Bullet(cx, top,  0.35))
        return bullets

    # ── Hit handling ──────────────────────────────────────────────────────────

    def hit(self) -> bool:
        """
        Called when the player is struck.
        Returns True if a life was lost (shield absorbed = False).
        """
        if self.invincible:
            return False
        if self.shield_active:
            self.shield_active = False
            self._make_invincible()
            return False
        self.lives -= 1
        self._make_invincible()
        return True

    def _make_invincible(self):
        self.invincible      = True
        self._invincible_end = pygame.time.get_ticks() + S.PLAYER_INVINCIBLE_MS

    # ── Power-up application ──────────────────────────────────────────────────

    def apply_powerup(self, ptype: str):
        now = pygame.time.get_ticks()
        if ptype == "shield":
            self.shield_active = True
            self._shield_end   = now + S.SHIELD_DURATION_MS
        elif ptype == "rapid":
            self.rapid_fire  = True
            self._rapid_end  = now + S.RAPID_DURATION_MS
            self.shoot_delay = S.PLAYER_RAPID_DELAY
        elif ptype == "triple":
            self.triple_shot = True
            self._triple_end = now + S.TRIPLE_DURATION_MS
        elif ptype == "speed":
            self.speed_boost = True
            self._speed_end  = now + S.SPEED_DURATION_MS
        elif ptype == "life":
            self.lives = min(self.lives + 1, 9)
        elif ptype == "bomb":
            return "bomb"   # signal to game to clear enemies
        return None

    def get_powerup_timers(self) -> dict:
        """Return remaining ms for each active power-up (for HUD)."""
        now = pygame.time.get_ticks()
        return {
            "shield": max(0, self._shield_end  - now) if self.shield_active else 0,
            "rapid":  max(0, self._rapid_end   - now) if self.rapid_fire   else 0,
            "triple": max(0, self._triple_end  - now) if self.triple_shot  else 0,
            "speed":  max(0, self._speed_end   - now) if self.speed_boost  else 0,
        }

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def alive(self) -> bool:
        return self.lives > 0