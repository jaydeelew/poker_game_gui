# Poker Game GUI

> **⚠️ This project is still under construction. Features and documentation may change.**

A desktop Poker game built with Python and PySide6, following the MVVM (Model-View-ViewModel) architecture. The game supports both 5-card draw and 5-card stud variants, allowing multiple players to join, play, and determine the winner based on standard poker hand rankings.

[GitHub Repository](https://github.com/jaydeelew/poker_game_gui)

---

## Features

- **Graphical User Interface**: Built with PySide6 and Qt Designer UI files.
- **Poker Variants**: Play 5-card draw or 5-card stud.
- **Multiple Players**: Add or remove players before starting a game.
- **Hand Evaluation**: Automatic hand ranking and winner determination.
- **Card Exchange**: In 5-card draw, exchange up to 3 cards per player.
- **Game Restart**: Easily restart the game and play again.

---

## Gameplay Overview

- **Add Players**: Enter player names and add at least two players.
- **Choose Variant**: Select "5 Card Draw?" for draw poker, or leave unchecked for stud.
- **Deal Cards**: Click **PLAY** to deal cards to all players.
- **Reveal Hands**: Each player can view their hand privately. In draw poker, players may exchange up to 3 cards.
- **Reveal Winner**: Click **Reveal Winner** to show the winner and all hands.
- **Restart**: Use the Game menu or Restart button to play again.

### Supported Poker Hands

- Royal Flush
- Straight Flush
- Four of a Kind
- Full House
- Flush
- Straight
- Three of a Kind
- Two Pair
- One Pair
- High Card

---

## Installation

1. **Clone the repository** (if you haven't already):

   ```bash
   git clone https://github.com/jaydeelew/poker_game_gui.git
   cd poker_game_gui
   ```

2. **(Optional) Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

1. **Ensure all required UI files are present in the `view/` directory:**

   - `pokergame.ui`
   - `cardsdealt.ui`
   - `displaystring.ui`
   - `drawhand.ui`
   - `hand.ui`

2. **Start the GUI:**
   ```bash
   python3 main.py
   ```

The main window will open. Add players, select the game variant, and enjoy playing Poker!

---

## Project Structure

```
poker_game_gui/
  main.py
  requirements.txt
  model/
  view/
  viewmodel/
```

- **model/**: Game logic, card/deck/hand/player classes
- **view/**: UI files and main window logic
- **viewmodel/**: ViewModel connecting UI and game logic

---

## Requirements

- Python 3.7+
- PySide6 (see requirements.txt)

---

## License

MIT License

---
