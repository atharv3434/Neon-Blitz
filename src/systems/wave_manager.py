"""
src/systems/wave_manager.py
============================
Controls enemy wave spawning. Each wave increases in difficulty.
"""

import random
from src.settings import Settings as S
from src.entities.enemies import Drone, Zigzagger, Diver, Tank, Swarmer, Boss


class WaveManager:
    """
    Manages wave-based enemy spawning.

    State
    -----
    wave        : current wave number (1-indexed)
    boss_count  : how many bosses have appeared
    cleared     : True when all enemies in current wave are dead
    """

    def __init__(self):
        self.wave        = 0
        self.boss_count  = 0
        self._spawn_queue: list = []
        self._spawn_delay = 600    # ms between spawns
        self._last_spawn  = 0
        self.cleared      = True   # start True so first wave triggers
        self._wave_deaths_clean = True  # no deaths this wave?

    # ── Public API ─────────────────────────────────────────────────────────────

    def start_next_wave(self) -> int:
        """Increment wave counter and populate spawn queue. Returns wave number."""
        self.wave += 1
        self.cleared = False
        self._wave_deaths_clean = True
        self._spawn_queue = self._build_queue()
        return self.wave

    def is_boss_wave(self) -> bool:
        return self.wave % S.BOSS_WAVE_INTERVAL == 0

    def update(self, enemy_group, now: int) -> list:
        """
        Called every frame. Spawns next enemy from queue if delay has passed.
        Returns list of newly spawned enemy sprites.
        """
        spawned = []
        if self._spawn_queue and now - self._last_spawn >= self._spawn_delay:
            enemy = self._spawn_queue.pop(0)
            enemy_group.add(enemy)
            spawned.append(enemy)
            self._last_spawn = now
            # Slightly decrease spawn delay as waves increase (harder)
            self._spawn_delay = max(250, 600 - self.wave * 15)
        return spawned

    def mark_player_death(self):
        self._wave_deaths_clean = False

    def wave_complete(self, enemy_group) -> dict:
        """
        Called when all enemies are dead. Returns bonus info dict.
        {
            "wave_bonus": int,
            "no_death_bonus": int,
            "total": int,
        }
        """
        self.cleared = True
        wave_bonus    = self.wave * S.WAVE_CLEAR_BONUS
        no_death_bonus = wave_bonus * (S.NO_DEATH_MULTIPLIER - 1) if self._wave_deaths_clean else 0
        return {
            "wave_bonus":    wave_bonus,
            "no_death_bonus": no_death_bonus,
            "total":         wave_bonus + no_death_bonus,
            "clean":         self._wave_deaths_clean,
        }

    # ── Spawn queue builder ────────────────────────────────────────────────────

    def _build_queue(self) -> list:
        w = self.wave
        queue = []

        if self.is_boss_wave():
            self.boss_count += 1
            x = S.WIDTH // 2
            queue.append(Boss(x, -80, wave=w, encounter=self.boss_count))
            # Add flanking drones for boss waves
            for _ in range(4):
                queue.append(Drone(random.randint(80, S.WIDTH-80), -random.randint(20, 200), wave=w))
            return queue

        # Normal wave — mix of enemy types based on wave number
        count = S.BASE_ENEMIES_PER_WAVE + (w - 1) * S.ENEMIES_WAVE_SCALE

        pool = [Drone]
        if w >= 2: pool.append(Zigzagger)
        if w >= 3: pool.extend([Diver, Diver])
        if w >= 4: pool.extend([Tank])
        if w >= 5: pool.extend([Swarmer, Swarmer, Swarmer])
        if w >= 7: pool.extend([Diver, Zigzagger])
        if w >= 10: pool.extend([Tank, Tank])

        for i in range(count):
            EClass = random.choice(pool)
            if EClass == Swarmer:
                # Spawn a pack
                pack_x = random.randint(60, S.WIDTH - 60)
                for j in range(6):
                    x = pack_x + random.randint(-30, 30)
                    y = -20 - i * 25 - j * 15
                    queue.append(Swarmer(x, y, wave=w))
            else:
                x = random.randint(60, S.WIDTH - 60)
                y = -20 - i * 35
                queue.append(EClass(x, y, wave=w))

        # Shuffle so it's not always the same order
        random.shuffle(queue)
        return queue

    @property
    def remaining_in_queue(self) -> int:
        return len(self._spawn_queue)