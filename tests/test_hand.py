import sys
import os
from model.hand import Hand
from model.card import Card
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


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
        assert result is True
        assert len(hand._cards) == original_length - 1

    def test_remove_nonexistent_card(self):
        """Test that removing non-existent card returns False"""
        cards = [Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")]
        hand = Hand(cards)

        result = hand.remove_card("2", "♥")
        assert result is False

    def test_hand_comparison_equality(self):
        """Test that equal hands return True for equality comparison"""
        # Test royal flush equality
        royal_flush1 = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])
        royal_flush2 = Hand([Card("A", "♥"), Card("K", "♥"), Card("Q", "♥"), Card("J", "♥"), Card("10", "♥")])
        assert royal_flush1 == royal_flush2

        # Test straight flush equality (same high card)
        straight_flush1 = Hand([Card("9", "♠"), Card("8", "♠"), Card("7", "♠"), Card("6", "♠"), Card("5", "♠")])
        straight_flush2 = Hand([Card("9", "♥"), Card("8", "♥"), Card("7", "♥"), Card("6", "♥"), Card("5", "♥")])
        assert straight_flush1 == straight_flush2

        # Test four of a kind equality (same four cards)
        four_kind1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("A", "♣"), Card("K", "♠")])
        four_kind2 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("A", "♣"), Card("Q", "♥")])
        assert four_kind1 == four_kind2

        # Test full house equality (same three and pair)
        full_house1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("K", "♠")])
        full_house2 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("K", "♥")])
        assert full_house1 == full_house2

        # Test flush equality (same card values)
        flush1 = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("9", "♠")])
        flush2 = Hand([Card("A", "♥"), Card("K", "♥"), Card("Q", "♥"), Card("J", "♥"), Card("9", "♥")])
        assert flush1 == flush2

        # Test straight equality (same high card)
        straight1 = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("10", "♠")])
        straight2 = Hand([Card("A", "♥"), Card("K", "♠"), Card("Q", "♥"), Card("J", "♦"), Card("10", "♣")])
        assert straight1 == straight2

        # Test three of a kind equality (same three and kickers)
        three_kind1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("Q", "♠")])
        three_kind2 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♥"), Card("Q", "♥")])
        assert three_kind1 == three_kind2

        # Test two pair equality (same pairs and kicker)
        two_pair1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("K", "♣"), Card("Q", "♠")])
        two_pair2 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("K", "♣"), Card("Q", "♥")])
        assert two_pair1 == two_pair2

        # Test one pair equality (same pair and kickers)
        one_pair1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("J", "♠")])
        one_pair2 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("J", "♥")])
        assert one_pair1 == one_pair2

        # Test high card equality (same card values)
        high_card1 = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("9", "♠")])
        high_card2 = Hand([Card("A", "♥"), Card("K", "♠"), Card("Q", "♥"), Card("J", "♦"), Card("9", "♣")])
        assert high_card1 == high_card2

    def test_hand_comparison_inequality(self):
        """Test that different hands return False for equality comparison"""
        royal_flush = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])
        four_kind = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("A", "♣"), Card("K", "♠")])
        assert not (royal_flush == four_kind)

        # Test same hand type but different values
        straight_flush1 = Hand([Card("9", "♠"), Card("8", "♠"), Card("7", "♠"), Card("6", "♠"), Card("5", "♠")])
        straight_flush2 = Hand([Card("8", "♥"), Card("7", "♥"), Card("6", "♥"), Card("5", "♥"), Card("4", "♥")])
        assert not (straight_flush1 == straight_flush2)

    def test_hand_comparison_less_than(self):
        """Test that hand comparison using __lt__ works correctly"""
        # Test different hand types
        royal_flush = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])
        straight_flush = Hand([Card("9", "♥"), Card("8", "♥"), Card("7", "♥"), Card("6", "♥"), Card("5", "♥")])
        four_kind = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("A", "♣"), Card("K", "♠")])
        full_house = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("K", "♠")])
        flush = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("9", "♠")])
        straight = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("10", "♠")])
        three_kind = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("Q", "♠")])
        two_pair = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("K", "♣"), Card("Q", "♠")])
        one_pair = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("J", "♠")])
        high_card = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("9", "♠")])

        # Test hand type hierarchy
        assert straight_flush < royal_flush
        assert four_kind < straight_flush
        assert full_house < four_kind
        assert flush < full_house
        assert straight < flush
        assert three_kind < straight
        assert two_pair < three_kind
        assert one_pair < two_pair
        assert high_card < one_pair

    def test_hand_comparison_same_type_less_than(self):
        """Test comparison of hands of the same type using __lt__"""
        # Test straight flush with different high cards
        straight_flush1 = Hand([Card("9", "♠"), Card("8", "♠"), Card("7", "♠"), Card("6", "♠"), Card("5", "♠")])
        straight_flush2 = Hand([Card("8", "♥"), Card("7", "♥"), Card("6", "♥"), Card("5", "♥"), Card("4", "♥")])
        assert straight_flush2 < straight_flush1

        # Test four of a kind with different four card values
        four_kind1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("A", "♣"), Card("K", "♠")])
        four_kind2 = Hand([Card("K", "♠"), Card("K", "♥"), Card("K", "♦"), Card("K", "♣"), Card("A", "♠")])
        assert four_kind2 < four_kind1

        # Test full house with different three of a kind values
        full_house1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("K", "♠")])
        full_house2 = Hand([Card("K", "♠"), Card("K", "♥"), Card("K", "♦"), Card("A", "♣"), Card("A", "♠")])
        assert full_house2 < full_house1

        # Test full house with same three of a kind but different pair
        full_house3 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("K", "♠")])
        full_house4 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("Q", "♣"), Card("Q", "♠")])
        assert full_house4 < full_house3

        # Test flush with different high cards
        flush1 = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("9", "♠")])
        flush2 = Hand([Card("K", "♥"), Card("Q", "♥"), Card("J", "♥"), Card("10", "♥"), Card("8", "♥")])
        assert flush2 < flush1

        # Test straight with different high cards
        straight1 = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("10", "♠")])
        straight2 = Hand([Card("K", "♠"), Card("Q", "♥"), Card("J", "♦"), Card("10", "♣"), Card("9", "♠")])
        assert straight2 < straight1

        # Test three of a kind with different three card values
        three_kind1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("Q", "♠")])
        three_kind2 = Hand([Card("K", "♠"), Card("K", "♥"), Card("K", "♦"), Card("A", "♣"), Card("Q", "♠")])
        assert three_kind2 < three_kind1

        # Test three of a kind with same three but different kickers
        three_kind3 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("Q", "♠")])
        three_kind4 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("J", "♠")])
        assert three_kind4 < three_kind3

        # Test two pair with different higher pair
        two_pair1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("K", "♣"), Card("Q", "♠")])
        two_pair2 = Hand([Card("K", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("Q", "♣"), Card("A", "♠")])
        assert two_pair2 < two_pair1

        # Test two pair with same higher pair but different lower pair
        two_pair3 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("K", "♣"), Card("Q", "♠")])
        two_pair4 = Hand([Card("A", "♠"), Card("A", "♥"), Card("Q", "♦"), Card("Q", "♣"), Card("K", "♠")])
        assert two_pair4 < two_pair3

        # Test two pair with same pairs but different kicker
        two_pair5 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("K", "♣"), Card("Q", "♠")])
        two_pair6 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("K", "♣"), Card("J", "♠")])
        assert two_pair6 < two_pair5

        # Test one pair with different pair values
        one_pair1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("J", "♠")])
        one_pair2 = Hand([Card("K", "♠"), Card("K", "♥"), Card("A", "♦"), Card("Q", "♣"), Card("J", "♠")])
        assert one_pair2 < one_pair1

        # Test one pair with same pair but different kickers
        one_pair3 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("J", "♠")])
        one_pair4 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("10", "♠")])
        assert one_pair4 < one_pair3

        # Test high card with different high cards
        high_card1 = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("9", "♠")])
        high_card2 = Hand([Card("K", "♠"), Card("Q", "♥"), Card("J", "♦"), Card("10", "♣"), Card("8", "♠")])
        assert high_card2 < high_card1

    def test_hand_comparison_edge_cases(self):
        """Test edge cases for hand comparisons"""
        # Test ace-low straight (5-4-3-2-A)
        ace_low_straight = Hand([Card("5", "♠"), Card("4", "♥"), Card("3", "♦"), Card("2", "♣"), Card("A", "♠")])
        regular_straight = Hand([Card("6", "♠"), Card("5", "♥"), Card("4", "♦"), Card("3", "♣"), Card("2", "♠")])
        assert ace_low_straight < regular_straight

        # Test wheel straight (A-2-3-4-5) vs other straights
        wheel_straight = Hand([Card("A", "♠"), Card("2", "♥"), Card("3", "♦"), Card("4", "♣"), Card("5", "♠")])
        ten_high_straight = Hand([Card("10", "♠"), Card("9", "♥"), Card("8", "♦"), Card("7", "♣"), Card("6", "♠")])
        assert wheel_straight < ten_high_straight

        # Test hands with same kicker values but different suits
        flush1 = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("9", "♠")])
        flush2 = Hand([Card("A", "♥"), Card("K", "♥"), Card("Q", "♥"), Card("J", "♥"), Card("9", "♥")])
        assert flush1 == flush2  # Should be equal since suits don't matter for comparison

    def test_hand_comparison_invalid_types(self):
        """Test that comparison with invalid types returns NotImplemented"""
        hand = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])

        # Test comparison with non-Hand objects
        assert hand.__eq__("not a hand") == NotImplemented
        assert hand.__lt__("not a hand") == NotImplemented

    def test_hand_comparison_comprehensive_scenarios(self):
        """Test comprehensive scenarios covering all hand types and their comparisons"""
        # Create hands of all types
        royal_flush = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])
        straight_flush = Hand([Card("9", "♥"), Card("8", "♥"), Card("7", "♥"), Card("6", "♥"), Card("5", "♥")])
        four_kind = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("A", "♣"), Card("K", "♠")])
        full_house = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("K", "♠")])
        flush = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("9", "♠")])
        straight = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("10", "♠")])
        three_kind = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("Q", "♠")])
        two_pair = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("K", "♣"), Card("Q", "♠")])
        one_pair = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("J", "♠")])
        high_card = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("9", "♠")])

        # Test that hands are not equal to themselves (except royal flush)
        assert royal_flush == royal_flush
        assert straight_flush == straight_flush
        assert four_kind == four_kind
        assert full_house == full_house
        assert flush == flush
        assert straight == straight
        assert three_kind == three_kind
        assert two_pair == two_pair
        assert one_pair == one_pair
        assert high_card == high_card

        # Test that no hand is less than itself
        assert not (royal_flush < royal_flush)
        assert not (straight_flush < straight_flush)
        assert not (four_kind < four_kind)
        assert not (full_house < full_house)
        assert not (flush < flush)
        assert not (straight < straight)
        assert not (three_kind < three_kind)
        assert not (two_pair < two_pair)
        assert not (one_pair < one_pair)
        assert not (high_card < high_card)

        # Test complete ordering
        hands = [
            high_card,
            one_pair,
            two_pair,
            three_kind,
            straight,
            flush,
            full_house,
            four_kind,
            straight_flush,
            royal_flush,
        ]
        for i in range(len(hands)):
            for j in range(i + 1, len(hands)):
                assert hands[i] < hands[j]
                assert not (hands[j] < hands[i])
                assert not (hands[i] == hands[j])

    def test_hand_comparison_with_ace_rankings(self):
        """Test hand comparisons involving ace rankings in different contexts"""
        # Test ace as high card in high card hand
        ace_high = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("9", "♠")])
        king_high = Hand([Card("K", "♠"), Card("Q", "♥"), Card("J", "♦"), Card("10", "♣"), Card("8", "♠")])
        assert king_high < ace_high

        # Test ace as low card in wheel straight
        wheel_straight = Hand([Card("A", "♠"), Card("2", "♥"), Card("3", "♦"), Card("4", "♣"), Card("5", "♠")])
        six_high_straight = Hand([Card("6", "♠"), Card("5", "♥"), Card("4", "♦"), Card("3", "♣"), Card("2", "♠")])
        assert wheel_straight < six_high_straight

        # Test ace in pair comparison
        ace_pair = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("J", "♠")])
        king_pair = Hand([Card("K", "♠"), Card("K", "♥"), Card("A", "♦"), Card("Q", "♣"), Card("J", "♠")])
        assert king_pair < ace_pair

    def test_hand_comparison_with_tie_breaking(self):
        """Test hand comparisons that require tie-breaking logic"""
        # Test flush tie-breaking (compare all cards in descending order)
        flush1 = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("9", "♠")])
        flush2 = Hand([Card("A", "♥"), Card("K", "♥"), Card("Q", "♥"), Card("J", "♥"), Card("8", "♥")])
        assert flush2 < flush1

        # Test high card tie-breaking (compare all cards in descending order)
        high_card1 = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("9", "♠")])
        high_card2 = Hand([Card("A", "♥"), Card("K", "♠"), Card("Q", "♥"), Card("J", "♦"), Card("8", "♣")])
        assert high_card2 < high_card1

        # Test three of a kind with same three but different kickers
        three_kind1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("Q", "♠")])
        three_kind2 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("J", "♠")])
        assert three_kind2 < three_kind1

        # Test one pair with same pair but different kickers
        one_pair1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("J", "♠")])
        one_pair2 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("10", "♠")])
        assert one_pair2 < one_pair1

    def test_invalid_hand_type_comparison(self):
        """Test that comparing hands with invalid hand type raises ValueError in __eq__ and __lt__"""
        from model.hand import Hand
        from model.card import Card

        h1 = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])
        h2 = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])
        # Set invalid hand type
        h1._hand_value = (999, -1, -1, -1, -1, -1)
        h2._hand_value = (999, -1, -1, -1, -1, -1)
        with pytest.raises(ValueError, match="unexpected hand type"):
            h1 == h2
        with pytest.raises(ValueError, match="unexpected hand type"):
            h1 < h2

    def test_hand_type_fallback_else_branches(self):
        """Test else branches for __eq__ and __lt__ with different hand types"""
        from model.hand import Hand
        from model.card import Card

        # High card vs one pair
        high_card = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("9", "♠")])
        one_pair = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("J", "♠")])
        # __eq__ should be False
        assert not (high_card == one_pair)
        # __lt__ should be True
        assert high_card < one_pair

    def test_remove_card_returns_false(self):
        """Test that remove_card returns False when the card is not present"""
        hand = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])
        assert hand.remove_card("2", "♥") is False

    def test_eq_and_lt_return_false(self):
        """Test __eq__ and __lt__ return False for non-equal and not-less-than hands"""
        # __eq__ returns False for different hand types
        hand1 = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])
        hand2 = Hand([Card("9", "♥"), Card("8", "♥"), Card("7", "♥"), Card("6", "♥"), Card("5", "♥")])
        assert (hand1 == hand2) is False
        # __lt__ returns False for higher hand not less than lower hand
        assert (hand1 < hand2) is False
        # __lt__ returns False for equal hands
        hand3 = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])
        assert (hand1 < hand3) is False

    def test_best_hand_check_methods_return_false(self):
        """Test that all check_* methods in best_hand can return False"""
        # Use a hand that is only a high card (no pairs, no straight, no flush, etc.)
        hand = Hand([Card("A", "♠"), Card("K", "♥"), Card("8", "♦"), Card("5", "♣"), Card("2", "♠")])
        # Patch best_hand to expose check_* methods
        value_list = [card.rank for card in hand._cards]
        value_list.sort(reverse=True)
        values_to_counts = {v: value_list.count(v) for v in set(value_list)}
        suit_set = {card.suit for card in hand._cards}
        # check_one_pair
        pair_count = 0
        for val in values_to_counts.values():
            if val == 2:
                pair_count += 1
        assert pair_count == 0  # so check_one_pair would return False
        # check_two_pair
        assert sum(1 for v in values_to_counts.values() if v == 2) == 0  # so check_two_pair would return False
        # check_three_kind
        assert all(v != 3 for v in values_to_counts.values())  # so check_three_kind would return False
        # check_straight
        is_straight = True
        for i in range(len(value_list) - 1):
            if value_list[i] - value_list[i + 1] != 1:
                is_straight = False
        assert is_straight is False
        # check_flush
        assert len(suit_set) != 1  # so check_flush would return False
        # check_full_house
        one_pair = False
        three_kind = False
        for v in values_to_counts.values():
            if v == 2:
                one_pair = True
            if v == 3:
                three_kind = True
        assert not (one_pair and three_kind)  # so check_full_house would return False
        # check_four_kind
        assert all(v != 4 for v in values_to_counts.values())  # so check_four_kind would return False
        # check_straight_flush
        flush = len(suit_set) == 1
        straight = is_straight
        assert not (flush and straight)  # so check_straight_flush would return False
        # check_royal_flush
        high_card = max(value_list)
        straight_flush = flush and straight
        assert not (straight_flush and high_card == Card.RANK_DICT["A"])  # so check_royal_flush would return False

    def test_eq_and_lt_loops_return_false(self):
        """Test __eq__ and __lt__ return False in the looped value comparisons for each hand type"""
        from model.hand import Hand
        from model.card import Card

        # Flush: only one card different
        flush1 = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("9", "♠")])
        flush2 = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("8", "♠")])
        assert flush1 != flush2
        assert not (flush1 == flush2)
        assert not (flush1 < flush2)
        # Three of a Kind: same three, different kicker
        tok1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("Q", "♠")])
        tok2 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("J", "♠")])
        assert tok1 != tok2
        assert not (tok1 == tok2)
        assert not (tok1 < tok2)
        # Two Pair: same pairs, different kicker
        tp1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("K", "♣"), Card("Q", "♠")])
        tp2 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("K", "♣"), Card("J", "♠")])
        assert tp1 != tp2
        assert not (tp1 == tp2)
        assert not (tp1 < tp2)
        # One Pair: same pair, different kicker
        op1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("J", "♠")])
        op2 = Hand([Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("10", "♠")])
        assert op1 != op2
        assert not (op1 == op2)
        assert not (op1 < op2)
        # High Card: different lowest card
        hc1 = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("9", "♠")])
        hc2 = Hand([Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("8", "♠")])
        assert hc1 != hc2
        assert not (hc1 == hc2)
        assert not (hc1 < hc2)

    def test_full_house_eq_and_lt_return_false(self):
        """Test __eq__ and __lt__ for FULL_HOUSE with different three-of-a-kind or pair values (should return False)"""
        from model.hand import Hand
        from model.card import Card

        # Different three-of-a-kind value
        fh1 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("K", "♠")])
        fh2 = Hand([Card("K", "♠"), Card("K", "♥"), Card("K", "♦"), Card("A", "♣"), Card("A", "♥")])
        assert fh1 != fh2
        assert not (fh1 == fh2)
        assert not (fh1 < fh2)
        # Same three-of-a-kind, different pair value
        fh3 = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("Q", "♣"), Card("Q", "♠")])
        assert fh1 != fh3
        assert not (fh1 == fh3)
        assert not (fh1 < fh3)
