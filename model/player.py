class Player:
    """
    Represents a player in a card game.

    Attributes:
        _name (str): The player's name
    """

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self):
        return self._name
