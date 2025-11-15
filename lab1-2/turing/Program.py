import copy
from typing import Optional, TextIO
from Tape import Tape
from TransitionRule import TransitionRule

class Program:
    """
    Represents a complete Turing machine program: alphabet, states, rules, and tape configuration.

    Parameters
    ----------
    alphabet : list[str], optional
        Allowed tape symbols.
    empty_cell : str, default='_'
        Symbol representing empty tape cells.
    start_state : str, default='q0'
        State from which execution begins.
    states : list[str], optional
        States considered accepting states.
    """

    def __init__(self, alphabet: Optional[list[str]] = None, empty_cell: str = '_', start_state: str = 'q0', states: Optional[list[str]] = None):
        self.alphabet = alphabet or []
        self.empty_cell = empty_cell
        self.start_state = start_state
        self.accept_states = set(states or [])
        self.rules: list[TransitionRule] = []

    def add_rule(self, rule: TransitionRule):
        """
        Adds a transition rule to the program.

        Parameters
        ----------
        rule : TransitionRule
        """
        self.rules.append(rule)

    def remove_rule(self, rule: TransitionRule):
        """
        Removes a transition rule if it exists.

        Parameters
        ----------
        rule : TransitionRule
        """
        self.rules = [r for r in self.rules if r != rule]

    def find_rule(self, state: str, symbol: str) -> Optional[TransitionRule]:
        """
        Finds a rule matching given state and symbol.

        Parameters
        ----------
        state : str
        symbol : str

        Returns
        -------
        TransitionRule or None
        """
        for r in self.rules:
            if r.matches(state, symbol):
                return r
        return None

    def list_rules(self) -> list[str]:
        """
        Returns all rules as formatted strings.

        Returns
        -------
        list[str]
        """
        return [repr(r) for r in self.rules]

    def from_stream(cls, f: TextIO) -> tuple['Program', Tape]:
        """
        Parses a Turing machine program and tape configuration from a text stream.

        Parameters
        ----------
        f : TextIO
            Input file-like object.

        Returns
        -------
        tuple[Program, Tape]
        """
        prog = cls()
        tape_tokens = []
        head_pos = 0
        in_rules = False
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if line.lower().startswith('alphabet:'):
                val = line.split(':', 1)[1].strip()
                prog.alphabet = [s.strip() for s in val.split(',') if s.strip()]
                continue
            if line.lower().startswith('empty_cell:'):
                prog.empty_cell = line.split(':', 1)[1].strip()
                continue
            if line.lower().startswith('start:'):
                prog.start_state = line.split(':', 1)[1].strip()
                continue
            if line.lower().startswith('accept:'):
                val = line.split(':', 1)[1].strip()
                prog.accept_states = set([s.strip() for s in val.split(',') if s.strip()])
                continue
            if line.lower().startswith('tape:'):
                val = line.split(':', 1)[1].strip()
                tape_tokens = [s for s in val.split() if s != '']
                continue
            if line.lower().startswith('head:'):
                head_pos = int(line.split(':', 1)[1].strip())
                continue
            if line.lower().startswith('rules:') or line.lower().startswith('rule:'):
                in_rules = True
                continue
            if in_rules:
                parts = line.split('->')
                if len(parts) != 2:
                    continue
                left = parts[0].strip().split()
                right = parts[1].strip().split()
                if len(left) != 2 or len(right) < 3:
                    continue
                cur_state, cur_symbol = left[0], left[1]
                new_state, write_symbol, move = right[0], right[1], right[2]
                prog.add_rule(TransitionRule(cur_state, cur_symbol, new_state, write_symbol, move))
        tape = Tape.from_tokens(tape_tokens if tape_tokens else [prog.empty_cell], head=head_pos, empty_cell=prog.empty_cell)
        return prog, tape

    def __repr__(self):
        return f"Program(start={self.start_state}, accept={self.accept_states}, rules={len(self.rules)})"

    def copy(self):
        """
        Creates a deep copy of the program.

        Returns
        -------
        Program
        """
        return copy.deepcopy(self)
