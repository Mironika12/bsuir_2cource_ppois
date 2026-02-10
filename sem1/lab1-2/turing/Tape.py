import copy
from typing import Optional

class Tape:
    """
    Represents the tape of a Turing machine.

    The tape is conceptually infinite in both directions. This class dynamically
    expands the underlying list of cells when the head moves beyond current bounds.

    Parameters
    ----------
    content : list[str], optional
        Initial tape content. If omitted, the tape starts with a single empty cell.
    head : int, default=0
        Initial head position.
    empty_cell : str, default='_'
        Symbol used for empty / uninitialized cells.
    """

    def __init__(self, content: Optional[list[str]] = None, head: int = 0, empty_cell: str = '_'):
        self.empty_cell = empty_cell
        self._cells = list(content) if content is not None else [empty_cell]
        self.head = head
        self._ensure_index(self.head)

    def _ensure_index(self, i: int):
        """
        Ensures that index ``i`` exists on the tape. Expands tape if necessary.

        Parameters
        ----------
        i : int
            Index to check or create.
        """

        if i < 0:
            n = -i
            self._cells = [self.empty_cell] * n + self._cells
            self.head += n
        elif i >= len(self._cells):
            self._cells.extend([self.empty_cell] * (i - len(self._cells) + 1))

    def read(self) -> str:
        """
        Reads the symbol at the current head position.

        Returns
        -------
        str
            Symbol under the head.
        """
        self._ensure_index(self.head)
        return self._cells[self.head]

    def write(self, symbol: str):
        """
        Writes a symbol at the current head position.

        Parameters
        ----------
        symbol : str
            Symbol to write.
        """
        self._ensure_index(self.head)
        self._cells[self.head] = symbol

    def move(self, direction: str):
        """
        Moves the head left, right, or stays in place.

        Parameters
        ----------
        direction : {'L', 'R', 'N'}
            Direction to move: left, right, or no movement.

        Raises
        ------
        ValueError
            If direction is invalid.
        """
        if direction == 'L':
            self.head -= 1
        elif direction == 'R':
            self.head += 1
        elif direction == 'N':
            pass
        else:
            raise ValueError("Unknown move: " + direction)
        self._ensure_index(self.head)

    def set_head(self, pos: int):
        """
        Sets the head to a specific position.

        Parameters
        ----------
        pos : int
            New head position.
        """
        self.head = pos
        self._ensure_index(self.head)

    def content(self) -> list[str]:
        """
        Returns a shallow copy of the tape content.

        Returns
        -------
        list[str]
        """
        return list(self._cells)

    def as_str(self) -> str:
        """
        Produces a human-readable representation of the tape with head position.

        Returns
        -------
        str
        """
        cells = ' '.join(self._cells)
        caret_pos = sum(len(c) + 1 for c in self._cells[:self.head])
        return f"{cells}\n{' ' * caret_pos}^ (head at {self.head})"

    def __eq__(self, other):
        return isinstance(other, Tape) and self._cells == other._cells and self.head == other.head and self.empty_cell == other.empty_cell

    def __repr__(self):
        return f"Tape({self._cells!r}, head={self.head}, empty_cell={self.empty_cell!r})"

    def copy(self):
        """
        Returns a deep copy of the tape.

        Returns
        -------
        Tape
        """
        return copy.deepcopy(self)
    
def tape_from_tokens(tokens, head=0, empty_cell='_'):
    """
    Creates a Tape object from an existing sequence of tokens.

    Parameters
    ----------
    tokens : list[str]
        Initial tape content.
    head : int, default=0
        Initial head position.
    empty_cell : str, default='_'
        Symbol for empty cell.

    Returns
    -------
    Tape
    """
    return Tape(content=tokens, head=head, empty_cell=empty_cell)