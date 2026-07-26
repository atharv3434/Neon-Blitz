# 🚀 Neon Blitz — Arcade Space Shooter

A fast-paced neon arcade shooter built with Python + Pygame.
Survive endless waves of enemies, collect power-ups, and chase the high score!

---

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

---

## Controls

| Key | Action |
|-----|--------|
| `←` `→` or `A` `D` | Move left / right |
| `↑` `↓` or `W` `S` | Move up / down |
| `Space` | Shoot |
| `P` | Pause |
| `R` | Restart (game over screen) |
| `ESC` | Quit |
| `M` | Toggle mute |

---

## Game Features

### 🚀 Player Ship
- Smooth 8-directional movement with momentum
- Shoots neon laser bolts
- Shield system (absorbs one hit)
- Lives system (3 lives)

### 👾 Enemy Types
| Enemy | Behaviour | Points |
|-------|-----------|--------|
| **Drone** | Straight-line descent | 10 |
| **Zigzagger** | Side-to-side weave | 20 |
| **Diver** | Locks on and dives at player | 35 |
| **Tank** | Slow, takes 3 hits | 50 |
| **Swarmer** | Tiny, fast, spawns in packs | 15 |
| **Boss** | Appears every 5 waves, multiple attack patterns | 500 |

### ⚡ Power-ups
| Power-up | Effect | Duration |
|----------|--------|----------|
| 🔵 Shield | Absorbs next hit | 15s |
| 🔴 Rapid Fire | 3× fire rate | 8s |
| 🟡 Triple Shot | Fires 3 bullets in spread | 10s |
| 💜 Bomb | Destroys all on-screen enemies | Instant |
| 💚 Life | +1 life | Instant |
| ⚪ Speed Boost | 1.5× movement speed | 6s |

### 🌊 Wave System
- Enemies get faster and more numerous each wave
- New enemy types unlock as waves progress
- Boss fight every 5 waves
- Bonus points for clearing a wave without dying

### 🏆 Scoring
- Enemy kills: 10–500 points
- Wave clear bonus: wave × 100
- No-death wave bonus: ×2 multiplier
- High score saved to `saves/highscore.json`

---
