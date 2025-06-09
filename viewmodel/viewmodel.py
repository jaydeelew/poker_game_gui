from PySide6.QtCore import QObject, Signal, Slot
from model.game import PokerGame


class ViewModel(QObject):
    # Signals
    player_added = Signal(str)  # Emitted when a player is added
    player_removed = Signal(str)  # Emitted when a player is removed
    error_occurred = Signal(str)  # Emitted when an error occurs
    game_state_changed = Signal(str)  # Emitted when game state changes
    cards_dealt = Signal(bool)  # Emitted when cards are dealt

    def __init__(self):
        super().__init__()
        self._game = PokerGame()

    @property
    def players(self):
        return [player._name for player in self._game._players_hands.keys()]

    @Slot(str)
    def check_game_state(self):
        return self._game._game_state

    @Slot(str)
    def set_game_status_label(self, text):
        return self._game.report_game_state(text)

    @Slot(bool)
    def set_game_of_draw(self, game_of_draw: bool):
        self._game.set_game_of_draw(game_of_draw)

    @Slot(str)
    def add_player(self, player_name: str) -> bool:

        # Validate player name
        if not player_name:
            self.error_occurred.emit("Player name cannot be empty")
            return False

        if player_name in self.players:
            self.error_occurred.emit(f"Player '{player_name}' already exists")
            return False

        # Add new player (without a hand) to the game model
        self._game.add_player(player_name)
        self.player_added.emit(player_name)

        # Update game state if we have enough players
        if len(self.players) >= 2:
            self._game.set_game_state("ready")
            self.game_state_changed.emit("Game is ready to start")

        return True

    @Slot(str)
    def remove_player(self, player_name: str) -> bool:
        # Find the Player object with this name
        player_to_remove = None
        for player in self._game._players_hands.keys():
            if player._name == player_name:
                player_to_remove = player
                break

        if player_to_remove:
            del self._game._players_hands[player_to_remove]
            self.player_removed.emit(player_name)

            # Update game state if we don't have enough players
            if len(self.players) < 2:
                self._game.set_game_state("setup")
                self.game_state_changed.emit("Need at least 2 players to start")
            return True
        else:
            self.error_occurred.emit("Player doesn't exist")
        return False

    @Slot()
    def deal(self):
        if len(self.players) < 2:
            self.error_occurred.emit("Need at least 2 players to start")
            return

        if self._game.status != "ready":
            self.error_occurred.emit("Game is not ready to start")
            return

        self._game.deal_cards(5)

        self._game.set_game_state("playing")
        self.game_state_changed.emit("Game started")
        return True
