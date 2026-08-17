# IMPOSTER

IMPOSTER is an Android-first local pass-and-play multiplayer social-deduction game built with Python and Kivy. One player is secretly assigned as the Imposter each round, while every other player sees the secret word and category. Everyone discusses clues in real life, votes privately on one phone, and then reveals whether the group caught the Imposter.

## Run with Pydroid 3

1. Install **Pydroid 3** on Android.
2. In Pydroid 3, install the Kivy support/repository plugin if prompted.
3. Install dependencies from this repository:
   ```bash
   pip install -r requirements.txt
   ```
4. Open `main.py` in Pydroid 3 and press Run.

The game works offline after dependencies are installed.

## Requirements

- Python 3
- Kivy (`kivy>=2.3.0`)

No KivyMD or network services are required.

## Gameplay

- Supports **3 to 5 players**.
- Add player names on the main menu; blank names become `Player 1`, `Player 2`, etc.
- Pass the phone privately so each player reveals their role exactly once.
- Normal players see the word and category.
- The Imposter sees only the category and never sees the word.
- After discussion, each player privately votes for another player.
- Vote totals, ties, the actual Imposter, word, category, and caught/not-caught result are revealed at the end.
- **Play Again** starts a fresh round with the same players.

## Project Structure

```text
main.py                 # Kivy app entry point and ScreenManager setup
game/
  game_logic.py         # Central state, round setup, voting, results logic
  word_database.py      # Expandable word/category data
screens/
  common.py             # Shared styling, colors, asset path helpers
  main_menu.py          # Player setup and round start UI
  reveal.py             # Private pass-and-play secret reveal UI
  ready_vote.py         # Discussion transition screen
  voting.py             # Private pass-and-play voting UI
  vote_summary.py       # Dynamic vote table and tie notice
  results.py            # Final reveal and navigation
assets/main-menu/       # Player and pencil image assets
```
