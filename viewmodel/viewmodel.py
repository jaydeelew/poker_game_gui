from PySide6.QtCore import QObject, Signal, Slot
from model.game import PokerGame
from model.player import Player


class PokerGameViewModel(QObject):
    # Signals
    player_added = Signal(str)  # Emitted when a player is added
    player_removed = Signal(str)  # Emitted when a player is removed
    error_occurred = Signal(str)  # Emitted when an error occurs
    game_state_changed = Signal(str)  # Emitted when game state changes
    
    def __init__(self):
        super().__init__()
        self._game = PokerGame()
        self._game_state = "setup"  # setup, playing, finished
        
    @property
    def players(self):
        return [player._name for player in self._game._players.keys()]
    
    @Slot(str)
    def add_player(self, player_name: str) -> bool:
        """Add a player to the game if the name is valid."""
        player_name = player_name.strip()
        
        # Validate player name
        if not player_name:
            self.error_occurred.emit("Player name cannot be empty")
            return False
            
        if player_name in self.players:
            self.error_occurred.emit(f"Player '{player_name}' already exists")
            return False
            
        # Add player to the game model
        self._game._players[Player(player_name)] = None
        self.player_added.emit(player_name)
        
        # Update game state if we have enough players
        if len(self.players) >= 2:
            self._game_state = "ready"
            self.game_state_changed.emit("Game is ready to start")
            
        return True
    
    @Slot(str)
    def remove_player(self, player_name: str) -> bool:
        """Remove a player from the game."""
        # Find the Player object with this name
        player_to_remove = None
        for player in self._game._players.keys():
            if player._name == player_name:
                player_to_remove = player
                break
                
        if player_to_remove:
            del self._game._players[player_to_remove]
            self.player_removed.emit(player_name)
            
            # Update game state if we don't have enough players
            if len(self.players) < 2:
                self._game_state = "setup"
                self.game_state_changed.emit("Need at least 2 players to start")
            return True
        return False
        
    @Slot()
    def start_game(self) -> bool:
        """Start the game if we have enough players."""
        if len(self.players) < 2:
            self.error_occurred.emit("Need at least 2 players to start")
            return False
            
        if self._game_state != "ready":
            self.error_occurred.emit("Game is not ready to start")
            return False
            
        self._game_state = "playing"
        self.game_state_changed.emit("Game started")
        return True
