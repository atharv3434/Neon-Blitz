"""
src/systems/hud.py
===================
Heads-Up Display — draws all UI elements onto the game surface.
"""

import pygame
import math
from src.settings import Settings as S


class HUD:
    """Renders score, lives, wave, power-up timers, and messages."""

    def __init__(self):
        pygame.font.init()
        self._font_lg  = pygame.font.SysFont("consolas", 28, bold=True)
        self._font_md  = pygame.font.SysFont("consolas", 18, bold=True)
        self._font_sm  = pygame.font.SysFont("consolas", 13)
        self._font_xl  = pygame.font.SysFont("consolas", 52, bold=True)

        # Flash message queue
        self._messages: list[dict] = []

    # ── Main draw call ─────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface, player, wave: int, high_score: int,
             score: int, now: int):
        self._draw_score(surface, score, high_score)
        self._draw_lives(surface, player.lives)
        self._draw_wave(surface, wave)
        self._draw_powerup_timers(surface, player.get_powerup_timers(), now)
        self._draw_messages(surface, now)

    # ── Score ──────────────────────────────────────────────────────────────────

    def _draw_score(self, surface, score, high_score):
        txt  = self._font_lg.render(f"{score:08d}", True, S.NEON_CYAN)
        surface.blit(txt, (S.WIDTH // 2 - txt.get_width() // 2, 8))

        hi = self._font_sm.render(f"HI  {high_score:08d}", True, S.HUD_COLOUR)
        surface.blit(hi, (S.WIDTH // 2 - hi.get_width() // 2, 40))

    # ── Lives ──────────────────────────────────────────────────────────────────

    def _draw_lives(self, surface, lives):
        lbl = self._font_sm.render("LIVES", True, S.HUD_COLOUR)
        surface.blit(lbl, (14, 12))
        for i in range(lives):
            self._draw_mini_ship(surface, 14 + i * 22, 30)

    def _draw_mini_ship(self, surface, x, y):
        pts = [(x+8, y), (x, y+14), (x+8, y+10), (x+16, y+14)]
        pygame.draw.polygon(surface, S.NEON_CYAN, pts)

    # ── Wave ───────────────────────────────────────────────────────────────────

    def _draw_wave(self, surface, wave):
        txt = self._font_md.render(f"WAVE  {wave:02d}", True, S.NEON_YELLOW)
        surface.blit(txt, (S.WIDTH - txt.get_width() - 14, 12))

    # ── Power-up timers ────────────────────────────────────────────────────────

    _PU_META = {
        "shield": ("SHIELD",  S.NEON_BLUE,   S.SHIELD_DURATION_MS),
        "rapid":  ("RAPID",   S.NEON_RED,    S.RAPID_DURATION_MS),
        "triple": ("TRIPLE",  S.NEON_YELLOW, S.TRIPLE_DURATION_MS),
        "speed":  ("SPEED",   S.WHITE,       S.SPEED_DURATION_MS),
    }

    def _draw_powerup_timers(self, surface, timers: dict, now: int):
        x = 14
        y = S.HEIGHT - 80
        for key, remaining in timers.items():
            if remaining <= 0:
                continue
            label, colour, max_ms = self._PU_META[key]
            ratio = remaining / max_ms
            bar_w = 90
            pygame.draw.rect(surface, (40, 40, 40), (x, y, bar_w, 10), border_radius=4)
            pygame.draw.rect(surface, colour, (x, y, int(bar_w * ratio), 10), border_radius=4)
            pygame.draw.rect(surface, S.WHITE, (x, y, bar_w, 10), 1, border_radius=4)
            lbl = self._font_sm.render(label, True, colour)
            surface.blit(lbl, (x, y - 14))
            y -= 32

    # ── Flash messages ─────────────────────────────────────────────────────────

    def flash(self, text: str, colour: tuple = S.NEON_YELLOW, duration_ms: int = 1800):
        self._messages.append({
            "text":    text,
            "colour":  colour,
            "end":     pygame.time.get_ticks() + duration_ms,
        })

    def _draw_messages(self, surface, now: int):
        self._messages = [m for m in self._messages if m["end"] > now]
        for i, msg in enumerate(self._messages):
            alpha  = int(255 * min(1, (msg["end"] - now) / 600))
            txt    = self._font_md.render(msg["text"], True, msg["colour"])
            surf   = txt.copy()
            surf.set_alpha(alpha)
            surface.blit(surf, (S.WIDTH // 2 - surf.get_width() // 2, S.HEIGHT // 2 - 60 - i * 30))

    # ── Full-screen overlays ───────────────────────────────────────────────────

    def draw_pause(self, surface):
        self._overlay(surface, 100)
        txt = self._font_xl.render("PAUSED", True, S.NEON_CYAN)
        surface.blit(txt, (S.WIDTH//2 - txt.get_width()//2, S.HEIGHT//2 - 40))
        sub = self._font_md.render("Press  P  to resume", True, S.HUD_COLOUR)
        surface.blit(sub, (S.WIDTH//2 - sub.get_width()//2, S.HEIGHT//2 + 30))

    def draw_game_over(self, surface, score: int, high_score: int, wave: int, new_hi: bool):
        self._overlay(surface, 140)
        c = S.NEON_RED
        txt = self._font_xl.render("GAME OVER", True, c)
        surface.blit(txt, (S.WIDTH//2 - txt.get_width()//2, S.HEIGHT//2 - 120))
        for i, line in enumerate([
            f"Score : {score:,}",
            f"Wave  : {wave}",
            f"Best  : {high_score:,}" + ("  ← NEW!" if new_hi else ""),
            "",
            "Press  R  to restart",
            "Press ESC  to quit",
        ]):
            col = S.NEON_YELLOW if "NEW!" in line else S.WHITE if line else S.WHITE
            t = self._font_md.render(line, True, col)
            surface.blit(t, (S.WIDTH//2 - t.get_width()//2, S.HEIGHT//2 - 50 + i * 28))

    def draw_wave_banner(self, surface, wave: int, boss: bool = False):
        self._overlay(surface, 80)
        label = f"⚡  BOSS WAVE  {wave}  ⚡" if boss else f"WAVE  {wave}"
        col   = S.NEON_PINK if boss else S.NEON_GREEN
        txt   = self._font_xl.render(label, True, col)
        surface.blit(txt, (S.WIDTH//2 - txt.get_width()//2, S.HEIGHT//2 - 30))

    def _overlay(self, surface, alpha):
        ov = pygame.Surface((S.WIDTH, S.HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, alpha))
        surface.blit(ov, (0, 0))