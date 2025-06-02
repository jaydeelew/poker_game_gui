from collections import Counter
from card import Card


class Hand:
    """
    Represents a poker hand of 5 cards.

    Implements poker hand ranking and comparison logic according to standard poker rules.
    Supports all standard poker hands from high card to royal flush.

    Attributes:
        _cards (list[Card]): List of 5 cards in the poker hand
        _hand_value: Tuple containing hand type and relevant card values for comparison
    """

    # Define as class constants
    ROYAL_FLUSH = 10
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def __init__(self, cards: list[Card]) -> None:
        self._cards = cards
        self._hand_value = self.best_hand()

    # Returns a list where first element is an integer 1-14 representing a hand
    # ( e.g. 10 = Royal Flush)
    # The remaining elements are the Card objects in the hand.
    @property
    def get_hand(self) -> list:
        cards = []
        cards.append(self._hand_value[0])
        for card in self._cards:
            cards.append(str(card))
        return cards

    def add_card(self, card: Card) -> None:
        self._cards.append(card)

    def remove_card(self, rank: int, suit: str) -> bool:
        for card in self._cards:
            if card.rank == rank and card.suit == suit:
                self._cards.remove(card)
                return True
        return False

    def update_best_hand(self):
        self._hand_value = self.best_hand()

    def __eq__(self, other: object) -> bool:
        # Determine if the two hands are equal in order of hands.
        if not isinstance(other, Hand):
            return NotImplemented
        if self._hand_value[0] == other._hand_value[0]:
            match self._hand_value[0]:
                # If both hands are Royal Flush, they are equal.
                case self.ROYAL_FLUSH:
                    return True
                # If both hands are Straight Flush, compare the highest card.
                case self.STRAIGHT_FLUSH:
                    return self._hand_value[1] == other._hand_value[1]
                # If both hands are Four of a Kind, compare the four of a kind value.
                case self.FOUR_OF_A_KIND:
                    return self._hand_value[1] == other._hand_value[1]
                # If both hands are Full House, compare the three of a kind value, then pair value.
                case self.FULL_HOUSE:
                    return (
                        self._hand_value[1] == other._hand_value[1]
                        and self._hand_value[2] == other._hand_value[2]
                    )
                # If both hands are Flush, compare the highest card values.
                case self.FLUSH:
                    for i in range(1, 6):
                        if self._hand_value[i] != other._hand_value[i]:  # type: ignore
                            return False
                    # If all the card values are equal:
                    return True
                # If both hands are Straight, compare the highest card value.
                case self.STRAIGHT:
                    return self._hand_value[1] == other._hand_value[1]
                # If both hands are Three of a Kind, compare the three of a kind value
                # and the remaining card values.
                case self.THREE_OF_A_KIND:
                    for i in range(1, 4):
                        if self._hand_value[i] != other._hand_value[i]:  # type: ignore
                            return False
                    return True
                # If both hands are Two Pair, compare the higher value pair,
                # the lower value pair, and the remaining card.
                case self.TWO_PAIR:
                    return (
                        self._hand_value[1] == other._hand_value[1]
                        and self._hand_value[2] == other._hand_value[2]
                        and self._hand_value[3] == other._hand_value[3]
                    )
                # If both hands are One Pair, compare the pair value and remaining cards.
                case self.ONE_PAIR:
                    for i in range(1, 5):
                        if self._hand_value[i] != other._hand_value[i]:  # type: ignore
                            return False
                    return True
                # If both hands are High Card, compare the highest card values.
                case self.HIGH_CARD:
                    return self._hand_value[1] == other._hand_value[1]
                # If hand type is not recognized, raise an error.
                case _:
                    raise ValueError("Invalid hand value comparison - unexpected hand type")
        else:
            return False

    # Compare tuple returned by this Pokerhand's _hand_value to another Pokerhand.
    def __lt__(self, other: "Hand") -> bool:
        # Determine if the two hands are equal in order of hands.
        if not isinstance(other, Hand):
            return NotImplemented
        if self._hand_value[0] == other._hand_value[0]:
            match self._hand_value[0]:
                # If both hands are Royal Flush, they are equal.
                case self.ROYAL_FLUSH:
                    return False
                # If both hands are Straight Flush, compare the highest card.
                case self.STRAIGHT_FLUSH:
                    return self._hand_value[1] < other._hand_value[1]
                # If both hands are Four of a Kind, compare the four of a kind value.
                case self.FOUR_OF_A_KIND:
                    return self._hand_value[1] < other._hand_value[1]
                # If both hands are Full House, compare the three of a kind value first,
                # then the pair value.
                case self.FULL_HOUSE:
                    for i in range(1, 3):
                        if self._hand_value[i] < other._hand_value[i]:  # type: ignore
                            return True
                        if self._hand_value[i] > other._hand_value[i]:  # type: ignore
                            return False
                    # If both hands are equal
                    return False
                # If both hands are Flush, compare the highest card values in descending order.
                case self.FLUSH:
                    for i in range(1, 6):
                        if self._hand_value[i] < other._hand_value[i]:  # type: ignore
                            return True
                        if self._hand_value[i] > other._hand_value[i]:  # type: ignore
                            return False
                    # If both hands are equal
                    return False
                # If both hands are Straight, compare the highest card value.
                case self.STRAIGHT:
                    return self._hand_value[1] < other._hand_value[1]
                # If both hands are Three of a Kind, compare the three of a kind value first,
                # then the remaining card values in descending order.
                case self.THREE_OF_A_KIND:
                    for i in range(1, 4):
                        if self._hand_value[i] < other._hand_value[i]:  # type: ignore
                            return True
                        elif self._hand_value[i] > other._hand_value[i]:  # type: ignore
                            return False
                    # If both hands are equal
                    return False
                # If both hands are Two Pair, compare the higher value pair first,
                # then the lower value pair, and finally the remaining card.
                case self.TWO_PAIR:
                    for i in range(1, 4):
                        if self._hand_value[i] < other._hand_value[i]:  # type: ignore
                            return True
                        elif self._hand_value[i] > other._hand_value[i]:  # type: ignore
                            return False
                    # If both hands are equal
                    return False
                # If both hands are One Pair, compare the pair value first,
                # then the remaining card values in descending order.
                case self.ONE_PAIR:
                    for i in range(1, 5):
                        if self._hand_value[i] < other._hand_value[i]:  # type: ignore
                            return True
                        elif self._hand_value[i] > other._hand_value[i]:  # type: ignore
                            return False
                    # If both hands are equal
                    return False
                # If both hands are High Card, compare all cards values in decending order.
                case self.HIGH_CARD:
                    for i in range(1, 6):
                        if self._hand_value[i] < other._hand_value[i]:  # type: ignore
                            return True
                        elif self._hand_value[i] > other._hand_value[i]:  # type: ignore
                            return False
                    # If both hands are equal
                    return False
                # If hand type is not recognized, raise an error.
                case _:
                    raise ValueError("Invalid hand value comparison - unexpected hand type")
        else:
            return self._hand_value[0] < other._hand_value[0]

    def best_hand(self) -> tuple[int, int, int, int, int, int]:  # type:ignore
        def check_high_card():
            return max(value_list)

        def check_one_pair() -> bool:
            pair_count = 0
            for val in values_to_counts.values():
                if val == 2:
                    pair_count += 1
            return pair_count == 1

        def check_two_pair() -> bool:
            pair_count = 0
            for val in values_to_counts.values():
                if val == 2:
                    pair_count += 1
            return pair_count == 2

        def check_three_kind() -> bool:
            for val in values_to_counts.values():
                if val == 3:
                    return True
            return False

        def check_straight() -> bool:
            for i in range(len(value_list) - 1):
                if value_list[i] - value_list[i + 1] != 1:
                    return False
            return True

        def check_flush() -> bool:
            return len(suit_set) == 1

        def check_full_house() -> bool:
            return one_pair and three_kind

        def check_four_kind() -> bool:
            for val in values_to_counts.values():
                if val == 4:
                    return True
            return False

        def check_straight_flush() -> bool:
            return flush and straight

        def check_royal_flush() -> bool:
            return straight_flush and high_card == Card.RANK_DICT["A"]

        # A -1 in indexes 1-5 of the return tuple indicates value not used.
        # Royal Flush does not need any index 1-5.
        # Four of a Kind places its value at index 1, and the fifth card at index 2.
        # Straigt Flush, Straight, and High Card place High Card at index 1.
        # Full House places its Three of a Kind value at index 1, and the pair value at index 2.
        # Flush places all five card values in descending order in indexes 1-5.
        # Three of a Kind places its value at index 1, and the remaining card values in descending
        # at index 2 and 3.
        # Two Pair places its higher value at index 1, and second value at index 2.
        # Pair places its value at index 1, and the other three value in descending order at
        # indexes 2-4.
        # and the remaining card in the third int value.
        def result_tuple(hand: int) -> tuple[int, int, int, int, int, int]:  # type:ignore
            match hand:
                case self.ROYAL_FLUSH:
                    return (self.ROYAL_FLUSH, -1, -1, -1, -1, -1)
                case self.STRAIGHT_FLUSH:
                    return (self.STRAIGHT_FLUSH, high_card, -1, -1, -1, -1)
                case self.FOUR_OF_A_KIND:
                    for val, cnt in values_to_counts.items():
                        if cnt == 4:
                            fok = val
                    return (self.FOUR_OF_A_KIND, fok, -1, -1, -1, -1)  # type: ignore
                case self.FULL_HOUSE:
                    pair = 0
                    tok = 0
                    for val, cnt in values_to_counts.items():
                        if cnt == 2:
                            pair = val
                        if cnt == 3:
                            tok = val
                    return (self.FULL_HOUSE, tok, pair, -1, -1, -1)
                case self.FLUSH:
                    a = value_list[0]
                    b = value_list[1]
                    c = value_list[2]
                    d = value_list[3]
                    e = value_list[4]
                    return (self.FLUSH, a, b, c, d, e)
                case self.STRAIGHT:
                    return (self.STRAIGHT, high_card, -1, -1, -1, -1)
                case self.THREE_OF_A_KIND:
                    other_cards = []
                    for val, cnt in values_to_counts.items():
                        if cnt == 3:
                            tok = val
                        if cnt == 1:
                            other_cards.append(val)
                    higher = max(other_cards)
                    lower = min(other_cards)
                    return (self.THREE_OF_A_KIND, tok, higher, lower, -1, -1)  # type: ignore
                case self.TWO_PAIR:
                    pairs = []
                    for val, cnt in values_to_counts.items():
                        if cnt == 2:
                            pairs.append(val)
                        if cnt == 1:
                            remaining = val
                    higher = max(pairs)
                    lower = min(pairs)
                    return (self.TWO_PAIR, higher, lower, remaining, -1, -1)  # type: ignore
                case self.ONE_PAIR:
                    for val, cnt in values_to_counts.items():
                        if cnt == 2:
                            pair = val
                    b = value_list[2]
                    c = value_list[3]
                    d = value_list[4]
                    return (self.ONE_PAIR, pair, b, c, d, -1)  # type: ignore
                case self.HIGH_CARD:
                    a = value_list[0]
                    b = value_list[1]
                    c = value_list[2]
                    d = value_list[3]
                    e = value_list[4]
                    return (self.HIGH_CARD, a, b, c, d, e)

        suit_set = {card.suit for card in self._cards}
        value_list = [card.rank for card in self._cards]
        value_list.sort(reverse=True)
        values_to_counts = Counter(value_list)

        high_card = check_high_card()  # High card holds actual card value.
        one_pair = check_one_pair()
        two_pair = check_two_pair()
        three_kind = check_three_kind()
        flush = check_flush()
        straight = check_straight()
        full_house = check_full_house()
        four_kind = check_four_kind()
        straight_flush = check_straight_flush()
        royal_flush = check_royal_flush()

        hands = [
            (royal_flush, self.ROYAL_FLUSH),
            (straight_flush, self.STRAIGHT_FLUSH),
            (four_kind, self.FOUR_OF_A_KIND),
            (full_house, self.FULL_HOUSE),
            (flush, self.FLUSH),
            (straight, self.STRAIGHT),
            (three_kind, self.THREE_OF_A_KIND),
            (two_pair, self.TWO_PAIR),
            (one_pair, self.ONE_PAIR),
            (True, self.HIGH_CARD),  # Always true as fallback
        ]

        # The first is_hand that is True is the highest hand.
        for is_hand, hand in hands:
            if is_hand:
                return result_tuple(hand)
