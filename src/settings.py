"""
src/settings.py
================
Central configuration for Neon Blitz.
All magic numbers live here — tweak to adjust difficulty & feel.
"""

import os


class Settings:
    # ── Window ────────────────────────────────────────────────────────────────
    WIDTH          = 800
    HEIGHT         = 900
    FPS            = 60
    TITLE          = "🚀 Neon Blitz"
    CAPTION        = "Neon Blitz — Arcade Shooter"

    # ── Colours (neon palette) ─────────────────────────────────────────────────
    BLACK          = (0,   0,   0)
    BG_DARK        = (5,   5,   15)
    WHITE          = (255, 255, 255)
    NEON_CYAN      = (0,   255, 255)
    NEON_PINK      = (255, 20,  147)
    NEON_GREEN     = (57,  255, 20)
    NEON_YELLOW    = (255, 255, 0)
    NEON_ORANGE    = (255, 140, 0)
    NEON_PURPLE    = (180, 0,   255)
    NEON_RED       = (255, 30,  30)
    NEON_BLUE      = (30,  100, 255)
    STAR_COLOUR    = (200, 200, 220)
    HUD_COLOUR     = (0,   220, 255)
    HUD_WARN       = (255, 120, 0)

    # ── Player ────────────────────────────────────────────────────────────────
    PLAYER_SPEED        = 5.5
    PLAYER_LIVES        = 3
    PLAYER_SHOOT_DELAY  = 220       # ms between shots (normal)
    PLAYER_RAPID_DELAY  = 70        # ms (rapid fire power-up)
    PLAYER_BULLET_SPEED = 12
    PLAYER_INVINCIBLE_MS = 2000     # invincibility frames after being hit
    PLAYER_WIDTH        = 44
    PLAYER_HEIGHT       = 52

    # ── Bullets ───────────────────────────────────────────────────────────────
    BULLET_WIDTH   = 4
    BULLET_HEIGHT  = 18
    ENEMY_BULLET_SPEED = 5

    # ── Enemies ───────────────────────────────────────────────────────────────
    DRONE_SPEED    = 2.5
    DRONE_HP       = 1
    DRONE_POINTS   = 10

    ZIGZAG_SPEED   = 2.8
    ZIGZAG_HP      = 1
    ZIGZAG_POINTS  = 20

    DIVER_SPEED    = 3.5
    DIVER_HP       = 1
    DIVER_POINTS   = 35

    TANK_SPEED     = 1.5
    TANK_HP        = 4
    TANK_POINTS    = 50

    SWARMER_SPEED  = 4.2
    SWARMER_HP     = 1
    SWARMER_POINTS = 15

    BOSS_SPEED     = 2.0
    BOSS_HP_BASE   = 30            # +10 per boss encounter
    BOSS_POINTS    = 500

    # ── Power-ups ─────────────────────────────────────────────────────────────
    POWERUP_SPEED         = 2.2
    POWERUP_SPAWN_CHANCE  = 0.18   # per enemy kill
    SHIELD_DURATION_MS    = 15_000
    RAPID_DURATION_MS     = 8_000
    TRIPLE_DURATION_MS    = 10_000
    SPEED_DURATION_MS     = 6_000

    # ── Waves ─────────────────────────────────────────────────────────────────
    BASE_ENEMIES_PER_WAVE  = 8
    ENEMIES_WAVE_SCALE     = 3     # added per wave
    WAVE_SPEED_MULTIPLIER  = 0.08  # enemy speed × (1 + wave × mult)
    BOSS_WAVE_INTERVAL     = 5     # boss every N waves
    WAVE_CLEAR_BONUS       = 100   # × wave number
    NO_DEATH_MULTIPLIER    = 2

    # ── Particles ─────────────────────────────────────────────────────────────
    EXPLOSION_PARTICLES    = 30
    TRAIL_PARTICLES        = 3
    PARTICLE_LIFETIME_MS   = 700

    # ── Stars ─────────────────────────────────────────────────────────────────
    NUM_STARS              = 180
    STAR_SPEED_RANGE       = (0.3, 2.5)

    # ── Paths ─────────────────────────────────────────────────────────────────
    SAVES_DIR              = "saves"
    HIGHSCORE_FILE         = os.path.join(SAVES_DIR, "highscore.json")
    UPLOAD_DIR             = "assets"