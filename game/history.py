"""Persistent local game-history storage for IMPOSTER."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime


class HistoryDB:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self):
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    played_at TEXT NOT NULL,
                    rounds INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id INTEGER NOT NULL,
                    player_index INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    FOREIGN KEY(game_id) REFERENCES games(id) ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS rounds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id INTEGER NOT NULL,
                    round_number INTEGER NOT NULL,
                    word TEXT NOT NULL,
                    word_hi TEXT NOT NULL,
                    FOREIGN KEY(game_id) REFERENCES games(id) ON DELETE CASCADE
                );
                """
            )

    def save_game(self, players, scores, rounds):
        played_at = datetime.now().astimezone().isoformat(timespec="seconds")
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO games (played_at, rounds) VALUES (?, ?)",
                (played_at, len(rounds)),
            )
            game_id = cursor.lastrowid
            for index, name in enumerate(players):
                conn.execute(
                    "INSERT INTO players (game_id, player_index, name, score) VALUES (?, ?, ?, ?)",
                    (game_id, index, name, int(scores.get(index, 0))),
                )
            for number, item in enumerate(rounds, start=1):
                conn.execute(
                    "INSERT INTO rounds (game_id, round_number, word, word_hi) VALUES (?, ?, ?, ?)",
                    (game_id, number, item["word"], item["word_hi"]),
                )
        return game_id

    def list_games(self):
        with self._connect() as conn:
            games = conn.execute(
                "SELECT id, played_at, rounds FROM games ORDER BY id DESC"
            ).fetchall()
            result = []
            for game in games:
                players = conn.execute(
                    "SELECT player_index, name, score FROM players WHERE game_id = ? ORDER BY player_index",
                    (game["id"],),
                ).fetchall()
                result.append({
                    "id": game["id"],
                    "played_at": game["played_at"],
                    "rounds": game["rounds"],
                    "players": [dict(p) for p in players],
                })
            return result

    def get_game(self, game_id):
        with self._connect() as conn:
            game = conn.execute(
                "SELECT id, played_at, rounds FROM games WHERE id = ?", (game_id,)
            ).fetchone()
            if not game:
                return None
            players = conn.execute(
                "SELECT player_index, name, score FROM players WHERE game_id = ? ORDER BY player_index",
                (game_id,),
            ).fetchall()
            rounds = conn.execute(
                "SELECT round_number, word, word_hi FROM rounds WHERE game_id = ? ORDER BY round_number",
                (game_id,),
            ).fetchall()
            return {
                "id": game["id"],
                "played_at": game["played_at"],
                "rounds": game["rounds"],
                "players": [dict(p) for p in players],
                "round_words": [dict(r) for r in rounds],
            }
