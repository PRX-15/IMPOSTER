"""Central game state and rules for IMPOSTER."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .word_database import WORD_DATABASE

MIN_PLAYERS = 3
MAX_PLAYERS = 10


@dataclass
class RoundWord:
    word: str
    word_hi: str
    category: str
    category_hi: str


@dataclass
class GameState:
    players: List[str] = field(default_factory=lambda: ["Player 1", "Player 2", "Player 3"])
    current_reveal_index: int = 0
    current_vote_index: int = 0
    selected_word: Optional[RoundWord] = None
    imposter_index: Optional[int] = None
    votes: Dict[int, int] = field(default_factory=dict)
    scores: Dict[int, int] = field(default_factory=dict)
    round_points: Dict[int, int] = field(default_factory=dict)
    round_scored: bool = False
    current_phase: str = "menu"
    _last_word: Optional[str] = None

    def set_players(self, names: List[str]) -> None:
        if not MIN_PLAYERS <= len(names) <= MAX_PLAYERS:
            raise ValueError("IMPOSTER supports 3 to 10 players.")
        self.players = [name.strip() or f"Player {i + 1}" for i, name in enumerate(names)]

    def reset_scores(self) -> None:
        """Start a fresh game session with all players at zero points."""
        self.scores = {i: 0 for i in range(len(self.players))}
        self.round_points.clear()
        self.round_scored = False

    def start_round(self, names: Optional[List[str]] = None) -> None:
        if names is not None:
            self.set_players(names)
        choices = list(WORD_DATABASE)
        if self._last_word and len(choices) > 1:
            choices = [entry for entry in choices if entry["word"] != self._last_word]
        entry = random.choice(choices)
        self.selected_word = RoundWord(
            entry["word"], entry["word_hi"], entry["category"], entry["category_hi"]
        )
        self._last_word = entry["word"]
        self.imposter_index = random.randrange(len(self.players))
        self.current_reveal_index = 0
        self.current_vote_index = 0
        self.votes.clear()
        self.round_points = {i: 0 for i in range(len(self.players))}
        self.round_scored = False
        # Keep scores across Play Again rounds, but initialize them if needed.
        for i in range(len(self.players)):
            self.scores.setdefault(i, 0)
        self.current_phase = "reveal"

    def get_secret_for_player(self, index: int) -> Dict[str, str | bool]:
        self._require_round()
        is_imposter = index == self.imposter_index
        return {
            "player": self.players[index],
            "is_imposter": is_imposter,
            "word": "" if is_imposter else self.selected_word.word,
            "word_hi": "" if is_imposter else self.selected_word.word_hi,
            "category": self.selected_word.category,
            "category_hi": self.selected_word.category_hi,
        }

    def cast_vote(self, voter_index: int, target_index: int) -> None:
        if not (0 <= voter_index < len(self.players) and 0 <= target_index < len(self.players)):
            raise ValueError("Invalid vote.")
        self.votes[voter_index] = target_index

    def vote_totals(self) -> Dict[int, int]:
        totals = {i: 0 for i in range(len(self.players))}
        for target in self.votes.values():
            totals[target] += 1
        return totals

    def leaders(self) -> List[int]:
        totals = self.vote_totals()
        if not totals:
            return []
        high = max(totals.values())
        return [idx for idx, total in totals.items() if total == high]

    def is_tie(self) -> bool:
        return len(self.leaders()) > 1

    def imposter_caught(self) -> bool:
        return not self.is_tie() and self.leaders() == [self.imposter_index]

    def calculate_round_points(self) -> Dict[int, int]:
        """Calculate and apply points for the completed round exactly once.

        The imposter gets 2 points if not caught, otherwise 0.
        Non-imposters get +1 for voting for the imposter and -1 for voting elsewhere.
        The imposter's own vote does not affect their score.
        """
        self._require_round()
        if self.round_scored:
            return dict(self.round_points)

        points = {i: 0 for i in range(len(self.players))}
        caught = self.imposter_caught()

        # Imposter outcome points.
        if not caught:
            points[self.imposter_index] = 2

        # Voter accuracy points for the non-imposters.
        for voter_index, target_index in self.votes.items():
            if voter_index == self.imposter_index:
                continue
            points[voter_index] = 1 if target_index == self.imposter_index else -1

        self.round_points = points
        for index, value in points.items():
            self.scores[index] = self.scores.get(index, 0) + value
        self.round_scored = True
        return dict(points)

    def reset_to_menu(self) -> None:
        self.current_phase = "menu"
        self.current_reveal_index = 0
        self.current_vote_index = 0
        self.votes.clear()

    def _require_round(self) -> None:
        if self.selected_word is None or self.imposter_index is None:
            raise RuntimeError("No round is active.")
