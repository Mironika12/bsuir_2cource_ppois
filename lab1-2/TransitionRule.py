class TransitionRule:
    """
    Represents a transition rule of a Turing machine.

    A rule maps:
        (current_state, current_symbol)
    to
        (new_state, write_symbol, move_direction)

    Parameters
    ----------
    cur_state : str
    cur_symbol : str
    new_state : str
    write_symbol : str
    move : {'L', 'R', 'N'}
    """

    def __init__(self, cur_state: str, cur_symbol: str, new_state: str, write_symbol: str, move: str):
        self.cur_state = cur_state
        self.cur_symbol = cur_symbol
        self.new_state = new_state
        self.write_symbol = write_symbol
        self.move = move

    def matches(self, state: str, symbol: str) -> bool:
        """
        Checks whether this rule applies to given state and symbol.

        Parameters
        ----------
        state : str
        symbol : str

        Returns
        -------
        bool
        """
        return self.cur_state == state and self.cur_symbol == symbol

    def __repr__(self):
        return f"{self.cur_state} {self.cur_symbol} -> {self.new_state} {self.write_symbol} {self.move}"

    def __eq__(self, other):
        return isinstance(other, TransitionRule) and self.__dict__ == other.__dict__
