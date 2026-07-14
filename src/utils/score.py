"""
src/utils/score.py
===================
High score persistence and score management.
"""

import os
import json
from src.settings import Settings as S


class ScoreManager:
    """Loads and saves the high score to a JSON file."""

    def __init__(self):
        os.makedirs(S.SAVES_DIR, exist_ok=True)
        self._high_score = self._load()

    def _load(self) -> int:
        try:
            with open(S.HIGHSCORE_FILE) as f:
                data = json.load(f)
                return int(data.get("high_score", 0))
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return 0

    def _save(self):
        with open(S.HIGHSCORE_FILE, "w") as f:
            json.dump({"high_score": self._high_score}, f, indent=2)

    @property
    def high_score(self) -> int:
        return self._high_score

    def update(self, score: int) -> bool:
        """
        Check if score beats the record. Saves and returns True if it does.
        """
        if score > self._high_score:
            self._high_score = score
            self._save()
            return True
        return False

    def reset(self):
        """Wipe the saved high score (for testing)."""
        self._high_score = 0
        self._save()