class Card:
    """
    Represents a standard playing card with a value and suit.

    Attributes:
        _rank (Rank): The card's value (2-10, Jack, Queen, King, Ace)
        _suit_value (Suit): The card's suit (Clubs, Diamonds, Hearts, Spades)
    """

    RANK_DICT = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }
    # RANK_DICT = {
    #     "Two": 2,
    #     "Three": 3,
    #     "Four": 4,
    #     "Five": 5,
    #     "Six": 6,
    #     "Seven": 7,
    #     "Eight": 8,
    #     "Nine": 9,
    #     "Ten": 10,
    #     "Jack": 11,
    #     "Queen": 12,
    #     "King": 13,
    #     "Ace": 14,
    # }

    SUIT_SET = {"C", "D", "H", "S"}
    # SUIT_SET = {"Clubs", "Diamonds", "Hearts", "Spades"}

    # def __init__(self, rank: Rank, suit: Suit):
    def __init__(self, rank: str, suit: str):
        self._rank = rank
        self._suit = suit

    @property
    def rank(self) -> int:
        return self.RANK_DICT[self._rank]

    @property
    def suit(self) -> str:
        return self._suit

    def __lt__(self, other: "Card") -> bool:
        return self.RANK_DICT[self._rank] < other.RANK_DICT[self._rank]

    def __str__(self) -> str:
        return f"{self._rank} of {self._suit}"
