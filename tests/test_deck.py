import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from model.deck import Deck
from model.card import Card


class TestDeck:
    def test_deck_creation(self):
        """Test that a deck is created with 52 cards"""
        deck = Deck()
        assert len(deck._deck) == 52

    def test_deck_has_all_suits(self):
        """Test that deck contains all four suits"""
        deck = Deck()
        suits = set(card.suit for card in deck._deck.values())
        assert suits == {"♠", "♥", "♦", "♣"}

    def test_deck_has_all_ranks(self):
        """Test that deck contains all 13 ranks"""
        deck = Deck()
        ranks = set(card.rankstr for card in deck._deck.values())
        expected_ranks = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"}
        assert ranks == expected_ranks

    def test_random_deal(self):
        """Test that random_deal returns the correct number of cards"""
        deck = Deck()
        dealt_cards = deck.random_deal(5)

        assert len(dealt_cards) == 5
        assert len(deck._dealt) == 5

    def test_random_deal_one(self):
        """Test that random_deal_one returns a single card"""
        deck = Deck()
        card = deck.random_deal_one()

        assert isinstance(card, Card)
        assert len(deck._dealt) == 1

    def test_reset_deck(self):
        """Test that reset_deck clears dealt cards"""
        deck = Deck()
        deck.random_deal(5)
        assert len(deck._dealt) == 5

        deck.reset_deck()
        assert len(deck._dealt) == 0

    def test_deal_all_cards(self):
        """Test that we can deal all 52 cards"""
        deck = Deck()
        all_cards = deck.random_deal(52)
        assert len(all_cards) == 52
        assert len(deck._dealt) == 52
