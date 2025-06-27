import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from model.hand import Hand
from model.card import Card


class TestHand:
    def test_hand_creation(self):
        """Test that a hand can be created with cards"""
        cards = [Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")]
        hand = Hand(cards)
        assert len(hand._cards) == 5

    def test_royal_flush_detection(self):
        """Test that royal flush is correctly identified"""
        cards = [Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")]
        hand = Hand(cards)
        assert hand._hand_value[0] == Hand.ROYAL_FLUSH

    def test_straight_flush_detection(self):
        """Test that straight flush is correctly identified"""
        cards = [Card("9", "♥"), Card("8", "♥"), Card("7", "♥"), Card("6", "♥"), Card("5", "♥")]
        hand = Hand(cards)
        assert hand._hand_value[0] == Hand.STRAIGHT_FLUSH

    def test_four_of_a_kind_detection(self):
        """Test that four of a kind is correctly identified"""
        cards = [Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("A", "♣"), Card("K", "♠")]
        hand = Hand(cards)
        assert hand._hand_value[0] == Hand.FOUR_OF_A_KIND

    def test_full_house_detection(self):
        """Test that full house is correctly identified"""
        cards = [Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("K", "♠")]
        hand = Hand(cards)
        assert hand._hand_value[0] == Hand.FULL_HOUSE

    def test_flush_detection(self):
        """Test that flush is correctly identified"""
        cards = [Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("9", "♠")]
        hand = Hand(cards)
        assert hand._hand_value[0] == Hand.FLUSH

    def test_straight_detection(self):
        """Test that straight is correctly identified"""
        cards = [Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("10", "♠")]
        hand = Hand(cards)
        assert hand._hand_value[0] == Hand.STRAIGHT

    def test_three_of_a_kind_detection(self):
        """Test that three of a kind is correctly identified"""
        cards = [Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("Q", "♠")]
        hand = Hand(cards)
        assert hand._hand_value[0] == Hand.THREE_OF_A_KIND

    def test_two_pair_detection(self):
        """Test that two pair is correctly identified"""
        cards = [Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("K", "♣"), Card("Q", "♠")]
        hand = Hand(cards)
        assert hand._hand_value[0] == Hand.TWO_PAIR

    def test_one_pair_detection(self):
        """Test that one pair is correctly identified"""
        cards = [Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("J", "♠")]
        hand = Hand(cards)
        assert hand._hand_value[0] == Hand.ONE_PAIR

    def test_high_card_detection(self):
        """Test that high card is correctly identified"""
        cards = [Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("9", "♠")]
        hand = Hand(cards)
        assert hand._hand_value[0] == Hand.HIGH_CARD

    def test_hand_comparison(self):
        """Test that hands can be compared correctly"""
        royal_flush = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])
        four_kind = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("A", "♣"), Card("K", "♠")])

        assert royal_flush > four_kind
        assert four_kind < royal_flush

    def test_add_card(self):
        """Test that cards can be added to hand"""
        cards = [Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")]
        hand = Hand(cards)
        original_length = len(hand._cards)

        new_card = Card("2", "♥")
        hand.add_card(new_card)
        assert len(hand._cards) == original_length + 1

    def test_remove_card(self):
        """Test that cards can be removed from hand"""
        cards = [Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")]
        hand = Hand(cards)
        original_length = len(hand._cards)

        result = hand.remove_card("A", "♠")
        assert result == True
        assert len(hand._cards) == original_length - 1

    def test_remove_nonexistent_card(self):
        """Test that removing non-existent card returns False"""
        cards = [Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")]
        hand = Hand(cards)

        result = hand.remove_card("2", "♥")
        assert result == False
