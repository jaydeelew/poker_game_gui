import pytest
import sys
import os

# Add the parent directory to the path so we can import from model
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from model.card import Card


class TestCard:
    def test_card_creation(self):
        """Test that cards can be created with rank and suit"""
        card = Card("A", "♠")
        assert card.rankstr == "A"
        assert card.suit == "♠"
        assert card.rank == 14  # Ace should have rank 14

    def test_card_string_representation(self):
        """Test that cards have proper string representation"""
        card = Card("K", "♥")
        assert str(card) == "K♥"

    def test_card_rank_values(self):
        """Test that cards have correct rank values"""
        assert Card("2", "♠").rank == 2
        assert Card("10", "♥").rank == 10
        assert Card("J", "♦").rank == 11
        assert Card("Q", "♣").rank == 12
        assert Card("K", "♠").rank == 13
        assert Card("A", "♥").rank == 14

    def test_invalid_rank(self):
        """Test that invalid rank raises error when accessing rank property"""
        card = Card("X", "♠")  # Invalid rank
        with pytest.raises(KeyError):
            _ = card.rank
