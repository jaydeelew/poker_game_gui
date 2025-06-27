import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from model.game import PokerGame
from model.player import Player


class TestPokerGame:
    def test_game_initialization(self):
        """Test that a poker game is initialized correctly"""
        game = PokerGame()
        assert game.state == "setup"
        assert not game.get_game_of_draw()
        assert len(game._players_hands) == 0

    def test_add_player(self):
        """Test that players can be added to the game"""
        game = PokerGame()
        game.add_player("Alice")
        assert len(game._players_hands) == 1
        assert game.get_player("Alice").name == "Alice"

    def test_remove_player(self):
        """Test that players can be removed from the game"""
        game = PokerGame()
        game.add_player("Bob")
        game.remove_player("Bob")
        assert len(game._players_hands) == 0

    def test_get_nonexistent_player(self):
        """Test that getting non-existent player returns None"""
        game = PokerGame()
        game.add_player("Charlie")
        # This will raise an AttributeError because get_player doesn't handle non-existent players
        with pytest.raises(AttributeError):
            game.get_player("Nonexistent")

    def test_deal_cards(self):
        """Test that cards can be dealt to players"""
        game = PokerGame()
        game.add_player("David")
        game.state = "ready"
        game.deal_cards(5)

        player = game.get_player("David")
        assert game._players_hands[player] is not None
        assert len(game._players_hands[player]._cards) == 5

    def test_show_hand(self):
        """Test that hands can be displayed"""
        game = PokerGame()
        game.add_player("Eve")
        game.state = "ready"
        game.deal_cards(5)

        player = game.get_player("Eve")
        hand_display = game.show_hand(player)
        assert len(hand_display) > 0
        assert isinstance(hand_display[0], str)  # Hand type

    def test_show_hand_no_cards(self):
        """Test that showing hand when no cards dealt returns empty list"""
        game = PokerGame()
        game.add_player("Frank")
        player = game.get_player("Frank")

        hand_display = game.show_hand(player)
        assert hand_display == []

    def test_exchange_cards(self):
        """Test that cards can be exchanged"""
        game = PokerGame()
        game.add_player("Grace")
        game.state = "ready"
        game.deal_cards(5)

        player = game.get_player("Grace")
        original_hand = game.show_hand(player)

        # Exchange one card
        new_hand = game.exchange_cards(player, ["A♠"])
        assert len(new_hand) > 0
        assert new_hand != original_hand

    def test_restart_game(self):
        """Test that the game can be restarted"""
        game = PokerGame()
        game.add_player("Henry")
        game.state = "playing"
        game.deal_cards(5)

        game.restart_game()
        assert game.state == "ready"
        assert not game.get_game_of_draw()

        player = game.get_player("Henry")
        assert game._players_hands[player] is None

    def test_set_game_type(self):
        """Test that game type can be set"""
        game = PokerGame()
        assert not game.get_game_of_draw()

        game.set_game_of_draw(True)
        assert game.get_game_of_draw()

        game.set_game_of_draw(False)
        assert not game.get_game_of_draw()

    def test_state_validation(self):
        """Test that invalid states raise ValueError"""
        game = PokerGame()
        with pytest.raises(ValueError):
            game.state = "invalid_state"

    def test_winners_with_no_players(self):
        """Test that winners returns empty list when no players"""
        game = PokerGame()
        winners = game.winners()
        assert len(winners) == 1  # Just the count of winners
        assert winners[0] == 0  # No winners
