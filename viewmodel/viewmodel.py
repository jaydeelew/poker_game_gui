from PySide6.QtCore import QObject, Signal
from model.game import PokerGame


class ViewModel(QObject):
    # Signals
    player_added = Signal(str)
    player_removed = Signal(str)
    show_hand_requested = Signal(object)
    show_draw_hand_requested = Signal(object, object)
    cards_exchanged = Signal(object)
    winner_declared = Signal(int, str, str)
    game_state_changed = Signal(str)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self._game = PokerGame()

    @property
    def players(self):
        return [player._name for player in self._game._players_hands.keys()]

    def get_game_state(self):
        return self._game.state

    def set_game_state(self, text) -> bool:
        self._game.state = text

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
            self._game.state = "ready"
            self.game_state_changed.emit("Game is ready to play")

        return True

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
                self._game.state = "setup"
            return True
        else:
            self.error_occurred.emit("Player doesn't exist")
        return False

    def deal_cards(self):
        if len(self.players) < 2:
            self.error_occurred.emit("Need at least 2 players to start")
            return

        if self._game.state != "ready":
            self.error_occurred.emit("Game is not ready to start")
            return

        self._game.deal_cards(5)

        self._game.state = "playing"
        self.game_state_changed.emit("Game started")
        return

    def get_game_of_draw(self):
        self._game.get_game_of_draw()

    def set_game_of_draw(self, game_of_draw: bool):
        self._game.set_game_of_draw(game_of_draw)

    def exchange_cards(self, player, selected_cards: list[str]):
        hand_list = self._game.exchange_cards(player, selected_cards)
        self.cards_exchanged.emit(hand_list)

    def show_hand(self, name):
        # get Player object to pass to show_hand()
        player = self._game.get_player(name)
        hand_list = self._game.show_hand(player)
        self.show_hand_requested.emit(hand_list)

    def show_draw_hand(self, name):
        # get Player object to pass to show_hand()
        player = self._game.get_player(name)
        hand_list = self._game.show_hand(player)
        self.show_draw_hand_requested.emit(player, hand_list)

    def get_winner(self):
        results = self._game.winners()
        num_of_winners = results[0]
        winner_lines = []
        loser_lines = []

        i = 1
        while i <= num_of_winners:
            winner_lines.append(results[i])
            i += 1
        winners_str = "\n".join(winner_lines)

        while i < len(results):
            loser_lines.append(results[i])
            i += 1
        losers_str = "\n".join(loser_lines)

        self.winner_declared.emit(num_of_winners, winners_str, losers_str)

    def restart_game(self) -> None:
        # Reset the game model
        self._game.restart_game()
