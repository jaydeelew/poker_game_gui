import pytest
import sys
import os
from model.game import PokerGame
from model.hand import Hand
from model.card import Card

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


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
        """Test that getting non-existent player raises ValueError"""
        game = PokerGame()
        game.add_player("Charlie")
        # This will raise a ValueError because get_player now handles non-existent players
        with pytest.raises(ValueError, match="Player 'Nonexistent' not found in the game"):
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

    def test_show_hand_all_types(self):
        """Test show_hand returns correct output for all hand types and card order"""
        hand_cases = [
            # (hand_type, cards, expected_first_line, expected_card_strs)
            (
                "Royal Flush",
                [Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")],
                "Royal Flush",
                ["10♠", "J♠", "Q♠", "K♠", "A♠"],
            ),
            (
                "Straight Flush",
                [Card("9", "♥"), Card("8", "♥"), Card("7", "♥"), Card("6", "♥"), Card("5", "♥")],
                "Straight Flush",
                ["5♥", "6♥", "7♥", "8♥", "9♥"],
            ),
            (
                "Four of a Kind",
                [Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("A", "♣"), Card("K", "♠")],
                "Four of a Kind",
                ["A♠", "A♥", "A♦", "A♣", "K♠"],
            ),
            (
                "Full House",
                [Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("K", "♠")],
                "Full House",
                ["A♠", "A♥", "A♦", "K♣", "K♠"],
            ),
            (
                "Flush",
                [Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("9", "♠")],
                "Flush",
                ["A♠", "K♠", "Q♠", "J♠", "9♠"],
            ),
            (
                "Straight",
                [Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("10", "♠")],
                "Straight",
                ["10♠", "J♣", "Q♦", "K♥", "A♠"],
            ),
            (
                "Three of a Kind",
                [Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("Q", "♠")],
                "Three of a Kind",
                ["A♠", "A♥", "A♦", "K♣", "Q♠"],
            ),
            (
                "Two Pair",
                [Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("K", "♣"), Card("Q", "♠")],
                "Two Pair",
                ["A♠", "A♥", "K♦", "K♣", "Q♠"],
            ),
            (
                "One Pair",
                [Card("A", "♠"), Card("A", "♥"), Card("K", "♦"), Card("Q", "♣"), Card("J", "♠")],
                "One Pair",
                ["A♠", "A♥", "K♦", "Q♣", "J♠"],
            ),
            (
                "High Card",
                [Card("A", "♠"), Card("K", "♥"), Card("Q", "♦"), Card("J", "♣"), Card("9", "♠")],
                "High Card",
                ["A♠", "K♥", "Q♦", "J♣", "9♠"],
            ),
        ]

        for hand_name, cards, expected_type, expected_cards in hand_cases:
            game = PokerGame()
            game.add_player("TestPlayer")
            player = game.get_player("TestPlayer")
            # Assign the hand directly
            game._players_hands[player] = Hand(cards)
            result = game.show_hand(player)
            assert result[0] == expected_type, f"{hand_name}: Expected type {expected_type}, got {result[0]}"
            assert result[1:] == expected_cards, f"{hand_name}: Expected cards {expected_cards}, got {result[1:]}"

    def test_winners_various_cases(self):
        """Test winners function for single winner, ties, and all hand types"""
        # Import here to avoid circular import issues
        from model.hand import Hand
        from model.card import Card

        # Helper to build expected hand string
        def hand_str(player_name, hand_type, card_strs):
            return f"{player_name} with {hand_type} {' '.join(card_strs)}"

        # 1. Single winner, different hand types
        game = PokerGame()
        game.add_player("Alice")
        game.add_player("Bob")
        alice = game.get_player("Alice")
        bob = game.get_player("Bob")
        # Alice: Royal Flush, Bob: Straight Flush
        alice_hand = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])
        bob_hand = Hand([Card("9", "♥"), Card("8", "♥"), Card("7", "♥"), Card("6", "♥"), Card("5", "♥")])
        game._players_hands[alice] = alice_hand
        game._players_hands[bob] = bob_hand
        result = game.winners()
        expected = [
            1,
            hand_str("Alice", "Royal Flush", ["10♠", "J♠", "Q♠", "K♠", "A♠"]),
            hand_str("Bob", "Straight Flush", ["5♥", "6♥", "7♥", "8♥", "9♥"]),
        ]
        assert result == expected, f"Single winner: {result} != {expected}"

        # 2. Tie: both players have the same hand type and value
        game = PokerGame()
        game.add_player("Carol")
        game.add_player("Dave")
        carol = game.get_player("Carol")
        dave = game.get_player("Dave")
        tie_hand = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")])
        game._players_hands[carol] = tie_hand
        game._players_hands[dave] = tie_hand
        result = game.winners()
        expected = [
            2,
            hand_str("Carol", "Royal Flush", ["10♠", "J♠", "Q♠", "K♠", "A♠"]),
            hand_str("Dave", "Royal Flush", ["10♠", "J♠", "Q♠", "K♠", "A♠"]),
        ]
        assert result[:3] == expected, f"Tie: {result[:3]} != {expected}"
        # Losers list should be empty
        assert len(result) == 3, f"Tie: result should only have winners, got {result}"

        # 3. Three players, one winner, two losers
        game = PokerGame()
        game.add_player("Eve")
        game.add_player("Frank")
        game.add_player("Grace")
        eve = game.get_player("Eve")
        frank = game.get_player("Frank")
        grace = game.get_player("Grace")
        eve_hand = Hand(
            [Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("A", "♣"), Card("K", "♠")]
        )  # Four of a Kind
        frank_hand = Hand([Card("A", "♠"), Card("A", "♥"), Card("A", "♦"), Card("K", "♣"), Card("K", "♠")])  # Full House
        grace_hand = Hand([Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("9", "♠")])  # Flush
        game._players_hands[eve] = eve_hand
        game._players_hands[frank] = frank_hand
        game._players_hands[grace] = grace_hand
        result = game.winners()
        expected = [
            1,
            hand_str("Eve", "Four of a Kind", ["A♠", "A♥", "A♦", "A♣", "K♠"]),
            hand_str("Frank", "Full House", ["A♠", "A♥", "A♦", "K♣", "K♠"]),
            hand_str("Grace", "Flush", ["A♠", "K♠", "Q♠", "J♠", "9♠"]),
        ]
        assert result == expected, f"Three players: {result} != {expected}"

        # 4. Two players tie, one player has a better hand
        game = PokerGame()
        game.add_player("Heidi")
        game.add_player("Ivan")
        game.add_player("Judy")
        heidi = game.get_player("Heidi")
        ivan = game.get_player("Ivan")
        judy = game.get_player("Judy")
        tie_hand = Hand([Card("9", "♥"), Card("8", "♥"), Card("7", "♥"), Card("6", "♥"), Card("5", "♥")])
        game._players_hands[heidi] = tie_hand
        game._players_hands[ivan] = tie_hand
        game._players_hands[judy] = Hand(
            [Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("10", "♠")]
        )
        result = game.winners()
        expected = [
            1,
            hand_str("Judy", "Royal Flush", ["10♠", "J♠", "Q♠", "K♠", "A♠"]),
            hand_str("Heidi", "Straight Flush", ["5♥", "6♥", "7♥", "8♥", "9♥"]),
            hand_str("Ivan", "Straight Flush", ["5♥", "6♥", "7♥", "8♥", "9♥"]),
        ]
        assert result == expected, f"Two tie for best: {result} != {expected}"

        # 5. No players
        game = PokerGame()
        result = game.winners()
        assert result == [0], f"No players: {result} != [0]"
