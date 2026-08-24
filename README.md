# IMPOSTER

IMPOSTER is an Android-first local pass-and-play multiplayer social-deduction game built with Python and Kivy. One player is secretly assigned as the Imposter each round, while every other player sees the secret word and category. Everyone discusses clues in real life, votes privately on one phone, and then reveals whether the group caught the Imposter.

> **One phone. One secret word. One Imposter. Can you find them?**

## SCREENSHOTS

<table>
  <tr>
    <td>
      <img src="assets/screenshots/ss1" width="250">
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/c02bda26-f2c6-464b-b1ac-26bead217cd3"  width="250">
    </td>
  </tr>
</table>





## Run on Android

You can use **any Python interpreter, IDE, or development environment that supports Python and Kivy**. **Pydroid 3 is recommended** for the easiest setup on Android.

### Recommended: Pydroid 3

1. **Install [Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3) on Android.**
2. **Install Kivy support in Pydroid 3.** Open Pydroid 3's Pip/Plugins section and install the Kivy package/plugin.
3. **Download the project ZIP.** On this GitHub page, tap **Code → Download ZIP**, then open your Downloads folder.
4. **Extract the ZIP** into a folder on your phone.
5. **Open `main.py` in Pydroid 3** and press Run.
6. **Enjoy!**

The game works offline after the required Kivy dependency is installed.

## Requirements

- Python 3
- Kivy (`kivy>=2.3.0`)

No KivyMD or network services are required.

## How It Works

- 👥 **3–10 players** play together on one phone.
- 🎭 At the start of each round, **one player is secretly chosen as the Imposter**.
- 🕵️ **Everyone except the Imposter receives the same secret word and category.** The Imposter sees only the category.
- 📱 Pass the phone around so each player can **privately view their role**.
- 💬 Once everyone knows their role, **discuss clues and try to figure out who doesn't know the word**.
- 🗳️ Each player **privately votes** for who they think the Imposter is.
- 📊 The votes are revealed and the player with the most votes is identified.
- 🏆 The game reveals the **Imposter, secret word, and whether the group caught them**.
- 🔄 **Play Again** starts another round with the same players.

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
