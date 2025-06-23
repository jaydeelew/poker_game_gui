from .hand import Hand
from .deck import Deck
from .player import Player


class PokerGame:
    """
    Manages a poker game session.

    Handles game setup, player management, dealing cards, and determining winners.
    Supports both 5-card draw and 5-card stud variants.

    Attributes:
        _draw_game (bool): True if playing 5-card draw, False for 5-card stud
        _num_players (int): Number of players in the game
        _deck (Deck): The game's deck of cards
        _players_hands (dict[Player, Hand]): Maps players to their poker hands
        or None if cards have not been dealt
    """

    def __init__(self) -> None:
        self._draw_game = False
        self._deck: Deck = Deck()
        self._players_hands: dict[Player, Hand | None] = {}
        self._game_state = "setup"  # setup, ready, playing, reveal, finished

    @property
    def state(self) -> str:
        return self._game_state

    @state.setter
    def state(self, text: str) -> bool:
        if text in ["setup", "ready", "playing", "reveal", "drawreveal", "finished"]:
            self._game_state = text
        else:
            raise ValueError("Trying to set invalid state")

    def get_game_of_draw(self):
        return self._draw_game

    def set_game_of_draw(self, draw_game: bool) -> None:
        self._draw_game = draw_game

    def add_player(self, name: str):
        self._players_hands[Player(name)] = None

    def get_player(self, name: str) -> Player:
        for player in self._players_hands.keys():
            if player.name == name:
                return player

    def remove_player(self, name: str):
        # Find the Player object with this name
        for player in self._players_hands.keys():
            if player.name == name:
                del self._players_hands[player]

    def deal_cards(self, hand_size: int) -> None:
        for player in self._players_hands:
            hand = self._deck.random_deal(hand_size)
            self._players_hands[player] = Hand(hand)

    def show_hand(self, player: Player) -> list:
        hand = self._players_hands[player]
        hand_list = []
        if hand:  # Check if hand exists
            match hand._hand_value[0]:
                case Hand.ROYAL_FLUSH:
                    sorted_cards = sorted(hand._cards, key=lambda x: x.rank)
                    hand_list.append("Royal Flush")
                    for card in sorted_cards:
                        hand_list.append(str(card))

                case Hand.STRAIGHT_FLUSH:
                    sorted_cards = sorted(hand._cards, key=lambda x: x.rank)
                    hand_list.append("Straight Flush")
                    for card in sorted_cards:
                        hand_list.append(str(card))

                case Hand.FOUR_OF_A_KIND:
                    # Group four matching cards first, then the remaining card
                    four_value = hand._hand_value[1]
                    four_cards = [card for card in hand._cards if card.rank == four_value]
                    other_card = [card for card in hand._cards if card.rank != four_value]
                    hand_list.append("Four of a Kind")
                    for card in four_cards + other_card:
                        hand_list.append(str(card))

                case Hand.FULL_HOUSE:
                    # Group three matching cards first, then the pair
                    three_value = hand._hand_value[1]
                    pair_value = hand._hand_value[2]
                    three_cards = [card for card in hand._cards if card.rank == three_value]
                    pair_cards = [card for card in hand._cards if card.rank == pair_value]
                    hand_list.append("Full House")
                    for card in three_cards + pair_cards:
                        hand_list.append(str(card))

                case Hand.FLUSH:
                    # Sort by value since they're all the same suit
                    sorted_cards = sorted(hand._cards, key=lambda x: x.rank, reverse=True)
                    hand_list.append("Flush")
                    for card in sorted_cards:
                        hand_list.append(str(card))

                case Hand.STRAIGHT:
                    sorted_cards = sorted(hand._cards, key=lambda x: x.rank)
                    hand_list.append("Straight")
                    for card in sorted_cards:
                        hand_list.append(str(card))

                case Hand.THREE_OF_A_KIND:
                    three_value = hand._hand_value[1]
                    three_cards = [card for card in hand._cards if card.rank == three_value]
                    other_cards = sorted(
                        [card for card in hand._cards if card.rank != three_value],
                        key=lambda x: x.rank,
                        reverse=True,
                    )
                    hand_list.append("Three of a Kind")
                    for card in three_cards + other_cards:
                        hand_list.append(str(card))

                case Hand.TWO_PAIR:
                    high_pair = hand._hand_value[1]
                    low_pair = hand._hand_value[2]
                    high_pair_cards = [card for card in hand._cards if card.rank == high_pair]
                    low_pair_cards = [card for card in hand._cards if card.rank == low_pair]
                    other_card = [card for card in hand._cards if card.rank not in (high_pair, low_pair)]
                    hand_list.append("Two Pair")
                    for card in high_pair_cards + low_pair_cards + other_card:
                        hand_list.append(str(card))

                case Hand.ONE_PAIR:
                    pair_value = hand._hand_value[1]
                    pair_cards = [card for card in hand._cards if card.rank == pair_value]
                    other_cards = sorted(
                        [card for card in hand._cards if card.rank != pair_value],
                        key=lambda x: x.rank,
                        reverse=True,
                    )
                    hand_list.append("One Pair")
                    for card in pair_cards + other_cards:
                        hand_list.append(str(card))

                case Hand.HIGH_CARD:
                    sorted_cards = sorted(hand._cards, key=lambda x: x.rank, reverse=True)
                    hand_list.append("High Card")
                    for card in sorted_cards:
                        hand_list.append(str(card))

        return hand_list

    def exchange_cards(self, player: Player, selected_cards: list) -> list:
        hand = self._players_hands[player]

        for i in range(0, len(selected_cards)):
            # rank is everything except the last character
            # suit is the last character
            rank, suit = selected_cards[i][:-1], selected_cards[i][-1]
            hand.remove_card(rank, suit)
            new_card = self._deck.random_deal_one()
            hand.add_card(new_card)

        hand.update_best_hand()
        self._players_hands[player] = hand

        # return hand_list
        return self.show_hand(player)

    def winners(self) -> str:
        winners = []
        curr_winning_hand = None

        for player, hand in self._players_hands.items():
            # Skip if current hand is None
            if hand is None:
                continue

            # The first player with a valid hand is the initial winner.
            if len(winners) == 0 or curr_winning_hand is None:
                winners.append(player)
                curr_winning_hand = hand
            elif hand > curr_winning_hand:
                winners = [player]
                curr_winning_hand = hand
            elif hand == curr_winning_hand:
                winners.append(player)

        lines = []
        for player in winners:
            text = f"{player.name} - {self.show_hand(player)}"
            lines.append(text)
        final_text = "\n".join(lines)
        return final_text

    def restart_game(self) -> None:
        self._draw_game = False
        self._deck = Deck()  # Create a new deck
        for player in self._players_hands:  # Clear players' hands
            self._players_hands[player] = None
        self._game_state = "setup"  # Reset game state
