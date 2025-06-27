import random
from .card import Card


class Deck:
    """
    Represents a standard 52-card playing deck.

    Manages deck state including dealt cards and provides methods for dealing
    cards randomly.

    Attributes:
        _deck (dict[int, Card]): Maps card IDs to Card objects
        _dealt (list[int]): List of IDs of cards that have been dealt
    """

    def __init__(self) -> None:
        self._deck: dict[int, Card] = {}
        self._dealt: list[int] = []
        self._build_deck()

    def _build_deck(self) -> None:
        count = 1
        for suit in Card.SUIT_SET:
            for rank in Card.RANK_DICT:
                new_card = Card(rank, suit)
                self._deck[count] = new_card
                count += 1

    def random_deal(self, hand_size: int) -> list[Card]:
        hand = []
        # Convert range to set and remove dealt cards via set subtraction.
        available_cards = set(range(1, len(self._deck) + 1)) - set(self._dealt)
        # Convert back to list for random.sample.
        sample = random.sample(list(available_cards), hand_size)

        for card_num in sample:
            hand.append(self._deck[card_num])
            self._dealt.append(card_num)

        return hand

    def random_deal_one(self) -> Card:
        # Convert range to set and remove dealt cards via set subtraction.
        available_cards = set(range(1, len(self._deck) + 1)) - set(self._dealt)
        # Convert back to list for random.sample.
        sample = random.sample(list(available_cards), 1)
        # random.sample return list. We access first/only element.
        self._dealt.append(sample[0])
        return self._deck[sample[0]]

    def reset_deck(self) -> None:
        self._dealt.clear()
