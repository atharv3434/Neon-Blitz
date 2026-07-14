"""
src/entities/enemies.py
========================
All enemy ship types: Drone, Zigzagger, Diver, Tank, Swarmer, Boss.
Each subclasses BaseEnemy and overrides movement & shoot logic.
"""

import pygame
import math
import random
from src.settings import Settings as S


class BaseEnemy(pygame.sprite.Sprite):
    colour   = S.NEON_RED
    hp       = 1
    points   = 10
    size     = (36, 36)
    shoots   = False
    shoot_interval = 2000

    def __init__(self, x: float, y: float, wave: int = 1):
        super().__init__()
        self.wave          = wave
        self.max_hp        = self.hp
        self._hp           = self.hp
        self._speed_mult   = 1 + wave * S.WAVE_SPEED_MULTIPLIER
        self.image         = self._draw()
        self.rect          = self.image.get_rect(center=(x, y))
        self._last_shot    = pygame.time.get_ticks() + random.randint(0, 2000)
        self._hit_flash    = 0

    def _draw(self) -> pygame.Surface:
        surf = pygame.Surface(self.size, pygame.SRCALPHA)
        self._draw_body(surf)
        return surf

    def _draw_body(self, surf):
        w, h = self.size
        pts = [(w//2, h-2), (2, 2), (w//2, h//3), (w-2, 2)]
        pygame.draw.polygon(surf, self.colour, pts)
        pygame.draw.polygon(surf, S.WHITE, pts, 1)

    @property
    def hp(self): return self._hp

    @hp.setter
    def hp(self, v):
        self._hp = v

    def take_hit(self, dmg: int = 1):
        self._hp -= dmg
        self._hit_flash = 6
        if self._hp <= 0:
            self.kill()
            return True
        return False

    def _flash(self):
        if self._hit_flash > 0:
            self._hit_flash -= 1
            flash = self.image.copy()
            flash.fill((255, 255, 255, 160), special_flags=pygame.BLEND_RGBA_ADD)
            return flash
        return self.image

    def can_shoot(self) -> bool:
        if not self.shoots:
            return False
        return pygame.time.get_ticks() - self._last_shot >= self.shoot_interval

    def do_shoot(self, player_pos: tuple) -> "EnemyBullet":
        from src.entities.bullet import EnemyBullet
        self._last_shot = pygame.time.get_ticks()
        return EnemyBullet(self.rect.centerx, self.rect.bottom, player_pos)

    def update(self, player_pos: tuple = None):
        self._move(player_pos)
        if self.rect.top > S.HEIGHT + 60:
            self.kill()

    def _move(self, player_pos):
        self.rect.y += self.base_speed * self._speed_mult

    @property
    def base_speed(self):
        return S.DRONE_SPEED

    def draw_hp_bar(self, surface: pygame.Surface):
        if self.max_hp <= 1:
            return
        bw = self.rect.width
        ratio = max(0, self._hp / self.max_hp)
        bar_rect = pygame.Rect(self.rect.left, self.rect.top - 7, bw, 4)
        fill_rect = pygame.Rect(self.rect.left, self.rect.top - 7, int(bw * ratio), 4)
        pygame.draw.rect(surface, (80, 0, 0), bar_rect)
        pygame.draw.rect(surface, S.NEON_GREEN, fill_rect)

    def draw(self, surface: pygame.Surface):
        surface.blit(self._flash(), self.rect)
        self.draw_hp_bar(surface)


# ── Drone ─────────────────────────────────────────────────────────────────────

class Drone(BaseEnemy):
    """Straight-line descender. Most basic enemy."""
    colour = S.NEON_RED
    size   = (32, 32)

    def _draw_body(self, surf):
        w, h = self.size
        pygame.draw.polygon(surf, self.colour, [(w//2, h-2), (2, 4), (w-2, 4)])
        pygame.draw.polygon(surf, S.WHITE,     [(w//2, h-2), (2, 4), (w-2, 4)], 1)
        pygame.draw.rect(surf, S.NEON_ORANGE, (w//2-4, h//2-2, 8, 8))

    @property
    def base_speed(self): return S.DRONE_SPEED


# ── Zigzagger ─────────────────────────────────────────────────────────────────

class Zigzagger(BaseEnemy):
    """Weaves side-to-side as it descends."""
    colour = S.NEON_YELLOW
    size   = (30, 30)

    def __init__(self, x, y, wave=1):
        self._tick = 0
        self._dir  = random.choice([-1, 1])
        super().__init__(x, y, wave)

    def _draw_body(self, surf):
        w, h = self.size
        pygame.draw.polygon(surf, self.colour, [(w//2, h-2), (0, h//2), (w//2, 2), (w, h//2)])
        pygame.draw.polygon(surf, S.WHITE, [(w//2, h-2), (0, h//2), (w//2, 2), (w, h//2)], 1)

    def _move(self, player_pos):
        self._tick += 1
        spd = S.ZIGZAG_SPEED * self._speed_mult
        self.rect.y += spd * 0.7
        self.rect.x += math.sin(self._tick * 0.08) * spd * 2.5
        self.rect.x  = max(0, min(S.WIDTH - self.rect.width, self.rect.x))


# ── Diver ─────────────────────────────────────────────────────────────────────

class Diver(BaseEnemy):
    """Slowly tracks player, then dives straight at them."""
    colour   = S.NEON_ORANGE
    size     = (34, 34)
    shoots   = False

    def __init__(self, x, y, wave=1):
        self._phase    = "track"
        self._dive_vx  = 0.0
        self._dive_vy  = 0.0
        self._track_t  = pygame.time.get_ticks() + random.randint(800, 2000)
        super().__init__(x, y, wave)

    def _draw_body(self, surf):
        w, h = self.size
        pygame.draw.polygon(surf, self.colour, [(w//2, h), (0, 0), (w//4, h//2), (w*3//4, h//2), (w, 0)])
        pygame.draw.polygon(surf, S.WHITE, [(w//2, h), (0, 0), (w//4, h//2), (w*3//4, h//2), (w, 0)], 1)

    def _move(self, player_pos):
        spd = S.DIVER_SPEED * self._speed_mult
        if self._phase == "track":
            self.rect.y += spd * 0.4
            if player_pos:
                dx = player_pos[0] - self.rect.centerx
                self.rect.x += max(-spd, min(spd, dx * 0.04))
            if pygame.time.get_ticks() >= self._track_t:
                self._phase = "dive"
                if player_pos:
                    ang = math.atan2(player_pos[1] - self.rect.centery, player_pos[0] - self.rect.centerx)
                    self._dive_vx = math.cos(ang) * spd * 2.5
                    self._dive_vy = math.sin(ang) * spd * 2.5
                else:
                    self._dive_vy = spd * 2
        else:
            self.rect.x += self._dive_vx
            self.rect.y += self._dive_vy


# ── Tank ──────────────────────────────────────────────────────────────────────

class Tank(BaseEnemy):
    """Slow and tough — takes 4 hits. Shoots at player."""
    colour  = S.NEON_PURPLE
    size    = (52, 46)
    shoots  = True
    shoot_interval = 1800

    def __init__(self, x, y, wave=1):
        self._hp = S.TANK_HP + (wave // 3)
        self.max_hp = self._hp
        super().__init__(x, y, wave)
        self._hp      = self.max_hp  # reset after super().__init__

    @property
    def hp(self): return self._hp
    @hp.setter
    def hp(self, v): self._hp = v

    def _draw_body(self, surf):
        w, h = self.size
        pygame.draw.rect(surf, self.colour, (4, 4, w-8, h-8), border_radius=6)
        pygame.draw.rect(surf, S.WHITE,     (4, 4, w-8, h-8), 2, border_radius=6)
        pygame.draw.rect(surf, S.NEON_RED,  (w//2-4, h-8, 8, 8))
        pygame.draw.circle(surf, S.NEON_PINK, (w//2, h//2), 8)

    @property
    def base_speed(self): return S.TANK_SPEED


# ── Swarmer ───────────────────────────────────────────────────────────────────

class Swarmer(BaseEnemy):
    """Tiny and fast — spawns in packs of 6."""
    colour = S.NEON_GREEN
    size   = (18, 18)

    def __init__(self, x, y, wave=1):
        self._offset = random.uniform(-1.5, 1.5)
        self._tick   = random.randint(0, 100)
        super().__init__(x, y, wave)

    def _draw_body(self, surf):
        w, h = self.size
        pygame.draw.polygon(surf, self.colour, [(w//2, h), (0, 0), (w, 0)])
        pygame.draw.polygon(surf, S.WHITE,     [(w//2, h), (0, 0), (w, 0)], 1)

    def _move(self, player_pos):
        self._tick += 1
        spd = S.SWARMER_SPEED * self._speed_mult
        self.rect.y += spd
        self.rect.x += math.sin(self._tick * 0.12) * self._offset * spd


# ── Boss ──────────────────────────────────────────────────────────────────────

class Boss(BaseEnemy):
    """
    Wave boss with three attack phases:
    Phase 1: side-to-side sweep
    Phase 2: dive attacks
    Phase 3: rapid fire + random movement
    """
    colour  = S.NEON_PINK
    size    = (100, 80)
    shoots  = True
    shoot_interval = 600

    def __init__(self, x, y, wave=1, encounter=1):
        self._encounter = encounter
        self._phase     = 1
        self._tick      = 0
        self._dir       = 1
        self._dive_vy   = 0.0
        self._dive_active = False
        hp = S.BOSS_HP_BASE + (encounter - 1) * 10
        self._hp = hp
        self.max_hp = hp
        super().__init__(x, y, wave)
        self._hp = hp   # reset after super

    @property
    def hp(self): return self._hp
    @hp.setter
    def hp(self, v): self._hp = v

    def _draw_body(self, surf):
        w, h = self.size
        # Main hull
        pts = [(w//2, h-4), (4, h//2), (4, 8), (w//2, 4), (w-4, 8), (w-4, h//2)]
        pygame.draw.polygon(surf, self.colour, pts)
        pygame.draw.polygon(surf, S.WHITE, pts, 2)
        # Cannon
        pygame.draw.rect(surf, S.NEON_RED, (w//2-5, h-20, 10, 24))
        # Eye
        pygame.draw.circle(surf, S.NEON_YELLOW, (w//2, h//2), 14)
        pygame.draw.circle(surf, S.NEON_RED,    (w//2, h//2), 8)
        pygame.draw.circle(surf, S.WHITE,       (w//2, h//2), 4)
        # Wing accents
        pygame.draw.line(surf, S.NEON_CYAN, (4, h//2), (w//4, h//3), 2)
        pygame.draw.line(surf, S.NEON_CYAN, (w-4, h//2), (w*3//4, h//3), 2)

    @property
    def base_speed(self): return S.BOSS_SPEED

    def _move(self, player_pos):
        self._tick += 1
        ratio = self._hp / self.max_hp

        if ratio > 0.6:
            self._phase = 1
        elif ratio > 0.3:
            self._phase = 2
        else:
            self._phase = 3

        spd = S.BOSS_SPEED * self._speed_mult

        if self._phase == 1:
            # Sweep side to side at top
            self.rect.x += self._dir * spd * 1.8
            if self.rect.right >= S.WIDTH or self.rect.left <= 0:
                self._dir *= -1
            target_y = 80
            self.rect.y += (target_y - self.rect.y) * 0.03

        elif self._phase == 2:
            # Occasional dives
            if not self._dive_active:
                self.rect.x += self._dir * spd * 1.5
                if self.rect.right >= S.WIDTH or self.rect.left <= 0:
                    self._dir *= -1
                target_y = 60
                self.rect.y += (target_y - self.rect.y) * 0.03
                if self._tick % 120 == 0:
                    self._dive_active = True
                    self._dive_vy = spd * 3
            else:
                self.rect.y += self._dive_vy
                if self.rect.centery > S.HEIGHT // 2:
                    self._dive_active = False
                    self.rect.y = 0
                    self._dive_vy = 0

        elif self._phase == 3:
            # Chaotic fast movement
            self.rect.x += math.sin(self._tick * 0.06) * spd * 3.5
            self.rect.y  = 50 + math.cos(self._tick * 0.04) * 30
            self.rect.x  = max(0, min(S.WIDTH - self.rect.width, self.rect.x))

    def do_shoot(self, player_pos: tuple) -> list:
        """Boss fires spread in phase 3, single shot otherwise."""
        from src.entities.bullet import EnemyBullet
        self._last_shot = pygame.time.get_ticks()
        bullets = [EnemyBullet(self.rect.centerx, self.rect.bottom, player_pos)]
        if self._phase == 3:
            for offset in [-40, 40]:
                fake_target = (player_pos[0] + offset, player_pos[1])
                bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom, fake_target))
        return bullets

    def draw_hp_bar(self, surface: pygame.Surface):
        """Boss gets a big HP bar at the top of the screen."""
        bar_w = S.WIDTH - 200
        bar_h = 14
        x = 100
        y = 12
        ratio = max(0, self._hp / self.max_hp)
        pygame.draw.rect(surface, (60, 0, 0), (x, y, bar_w, bar_h), border_radius=4)
        fill_colour = S.NEON_GREEN if ratio > 0.5 else S.NEON_YELLOW if ratio > 0.25 else S.NEON_RED
        pygame.draw.rect(surface, fill_colour, (x, y, int(bar_w * ratio), bar_h), border_radius=4)
        pygame.draw.rect(surface, S.WHITE, (x, y, bar_w, bar_h), 1, border_radius=4)

        try:
            font = pygame.font.SysFont("consolas", 13, bold=True)
            txt  = font.render(f"BOSS  {self._hp} / {self.max_hp}", True, S.NEON_PINK)
            surface.blit(txt, (x, y - 16))
        except Exception:
            pass