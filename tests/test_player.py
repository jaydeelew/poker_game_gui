import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from model.player import Player


class TestPlayer:
    def test_player_creation(self):
        """Test that a player can be created with a name"""
        player = Player("Alice")
        assert player.name == "Alice"

    def test_player_name_property(self):
        """Test that player name is accessible via property"""
        player = Player("Bob")
        assert player.name == "Bob"

    def test_player_with_empty_name(self):
        """Test that player can be created with empty name"""
        player = Player("")
        assert player.name == ""

    def test_player_with_special_characters(self):
        """Test that player can be created with special characters in name"""
        player = Player("Player_123!")
        assert player.name == "Player_123!"
