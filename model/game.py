from .hand import Hand
from .deck import Deck
from .player import Player
from .card import Card


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
        # Game setup in progress, Game is Ready to start, Game is active, Game is finished
        self._game_state = "setup"  # setup, ready, playing, finished

    @property
    def state(self) -> str:
        return self._game_state

    @state.setter
    def state(self, text: str) -> bool:
        if text in ["setup", "ready", "playing", "reveal", "finished"]:
            self._game_state = text
        else:
            raise ValueError("Trying to set invalid state")

    def set_draw_game(self, draw_game: bool) -> None:
        self._draw_game = draw_game

    def add_player(self, name: str):
        self._players_hands[Player(name)] = None

    def remove_player(self, name: str):
        # Find the Player object with this name
        for player in self._players_hands.keys():
            if player.name == name:
                del self._players_hands[player]

    def get_player(self, name: str) -> Player:
        for player in self._players_hands.keys():
            if player.name == name:
                return player

    def deal_cards(self, hand_size: int) -> None:
        for player in self._players_hands:
            hand = self._deck.random_deal(hand_size)
            self._players_hands[player] = Hand(hand)

    def show_hand(self, player: Player) -> str:
        hand = self._players_hands[player]
        if hand:  # Check if hand exists
            match hand._hand_value[0]:
                case Hand.ROYAL_FLUSH:
                    sorted_cards = sorted(hand._cards, key=lambda x: x.rank)
                    return f"Royal Flush: {', '.join(str(card) for card in sorted_cards)}"

                case Hand.STRAIGHT_FLUSH:
                    sorted_cards = sorted(hand._cards, key=lambda x: x.rank)
                    return f"Straight Flush: {', '.join(str(card) for card in sorted_cards)}"

                case Hand.FOUR_OF_A_KIND:
                    # Group four matching cards first, then the remaining card
                    four_value = hand._hand_value[1]
                    four_cards = [card for card in hand._cards if card.rank == four_value]
                    other_card = [card for card in hand._cards if card.rank != four_value]
                    return f"Four of a Kind: {', '.join(str(card) for card in four_cards + other_card)}"

                case Hand.FULL_HOUSE:
                    # Group three matching cards first, then the pair
                    three_value = hand._hand_value[1]
                    pair_value = hand._hand_value[2]
                    three_cards = [card for card in hand._cards if card.rank == three_value]
                    pair_cards = [card for card in hand._cards if card.rank == pair_value]
                    return (
                        f"Full House: {', '.join(str(card) for card in three_cards + pair_cards)}"
                    )

                case Hand.FLUSH:
                    # Sort by value since they're all the same suit
                    sorted_cards = sorted(hand._cards, key=lambda x: x.rank, reverse=True)
                    return f"Flush: {', '.join(str(card) for card in sorted_cards)}"

                case Hand.STRAIGHT:
                    sorted_cards = sorted(hand._cards, key=lambda x: x.rank)
                    return f"Straight: {', '.join(str(card) for card in sorted_cards)}"

                case Hand.THREE_OF_A_KIND:
                    three_value = hand._hand_value[1]
                    three_cards = [card for card in hand._cards if card.rank == three_value]
                    other_cards = sorted(
                        [card for card in hand._cards if card.rank != three_value],
                        key=lambda x: x.rank,
                        reverse=True,
                    )
                    return f"Three of a Kind: {', '.join(str(card) for card in three_cards + other_cards)}"

                case Hand.TWO_PAIR:
                    high_pair = hand._hand_value[1]
                    low_pair = hand._hand_value[2]
                    high_pair_cards = [card for card in hand._cards if card.rank == high_pair]
                    low_pair_cards = [card for card in hand._cards if card.rank == low_pair]
                    other_card = [
                        card for card in hand._cards if card.rank not in (high_pair, low_pair)
                    ]
                    return f"Two Pair: {', '.join(str(card) for card in high_pair_cards + low_pair_cards + other_card)}"

                case Hand.ONE_PAIR:
                    pair_value = hand._hand_value[1]
                    pair_cards = [card for card in hand._cards if card.rank == pair_value]
                    other_cards = sorted(
                        [card for card in hand._cards if card.rank != pair_value],
                        key=lambda x: x.rank,
                        reverse=True,
                    )
                    return f"One Pair: {', '.join(str(card) for card in pair_cards + other_cards)}"

                case Hand.HIGH_CARD:
                    sorted_cards = sorted(hand._cards, key=lambda x: x.rank, reverse=True)
                    return f"High Card: {', '.join(str(card) for card in sorted_cards)}"

    def show_players_hands_hand(self, player):
        self.show_hand(player)

    def show_all_hands(self) -> None:
        for player in self._players_hands.keys():
            pass

    def draw_cards(self) -> None:
        for player in self._players_hands:
            num_cards_trading = 0
            print(f"\n{player.name}, please have a seat")
            input("Press Enter when you are ready to see your cards ...")
            self.show_hand(player)
            while True:
                ans = input(f"\n{player.name}, how many cards are you trading in (0-3)? ")
                try:
                    num_cards_trading = int(ans)
                except ValueError:
                    print("Invalid input. Please enter a number")
                    input("Press Enter to continue ...")
                    continue

                if not 0 <= num_cards_trading <= 3:
                    print("You must enter a number from 0 to 3")
                    input("Press Enter to continue ...")
                    continue
                else:
                    break

            curr_num_cards = 0
            while curr_num_cards < num_cards_trading:
                trade = input("Enter the card you are trading (e.g. Two of Hearts): ").split()

                # Get the player's hand.
                player_hand = self._players_hands[player]

                # Check if player has a valid hand.
                if player_hand is None:
                    print(f"Player {player.name} has no hand")
                    continue

                # Is trade is a valid card?
                if trade[0] in Card.RANK_DICT and trade[2] in Card.SUIT_SET:
                    # If the player is holding this card, remove the card from the players hand.
                    if player_hand.remove_card(Card.RANK_DICT[trade[0]], trade[2]):
                        new_card = self._deck.random_deal_one()
                        player_hand.add_card(new_card)
                        player_hand.update_best_hand()
                        curr_num_cards += 1
                    else:
                        print(f"{player.name} does not have a {trade[0]} of {trade[2]}")
                        input("Press Enter to continue ...")
                else:
                    print("Invalid card. Please enter a valid card value and suit.")
                    input("Press Enter to continue ...")

            print("\nYour final hand:")
            self.show_hand(player)
            input("\nPress Enter when you are done seeing your cards ...")

    def winners(self) -> set:
        curr_winners = set()
        curr_winning_hand = None

        for player, hand in self._players_hands.items():
            # Skip if current hand is None
            if hand is None:
                continue

            # The first player with a valid hand is the initial winner.
            if len(curr_winners) == 0 or curr_winning_hand is None:
                curr_winners.add(player)
                curr_winning_hand = hand
            elif hand > curr_winning_hand:
                curr_winners = {player}
                curr_winning_hand = hand
            elif hand == curr_winning_hand:
                curr_winners.add(player)

        return curr_winners

    def restart_game(self) -> None:
        self._draw_game = False
        self._deck = Deck()  # Create a new deck
        self._players_hands.clear()  # Clear all players and hands
        self._game_state = "setup"  # Reset game state
