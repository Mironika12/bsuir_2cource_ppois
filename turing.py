from typing import Optional, TextIO
import copy

class Tape:
    def __init__(self, content: Optional[list[str]] = None, head: int = 0, empty_cell: str = '_'):
        self.empty_cell = empty_cell
        self._cells = list(content) if content is not None else [empty_cell]
        self.head = head
        self._ensure_index(self.head)

    def _ensure_index(self, i: int):
        if i < 0:
            n = -i
            self._cells = [self.empty_cell] * n + self._cells
            self.head += n
        elif i >= len(self._cells):
            self._cells.extend([self.empty_cell] * (i - len(self._cells) + 1))

    def read(self) -> str:
        self._ensure_index(self.head)
        return self._cells[self.head]

    def write(self, symbol: str):
        self._ensure_index(self.head)
        self._cells[self.head] = symbol

    def move(self, direction: str):
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
        self.head = pos
        self._ensure_index(self.head)

    def content(self) -> list[str]:
        return list(self._cells)

    def as_str(self) -> str:
        cells = ' '.join(self._cells)
        caret_pos = sum(len(c) + 1 for c in self._cells[:self.head])
        return f"{cells}\n{' ' * caret_pos}^ (head at {self.head})"

    @classmethod
    def from_tokens(cls, tokens: list[str], head: int = 0, empty_cell: str = '_'):
        return cls(content=tokens, head=head, empty_cell=empty_cell)

    def __eq__(self, other):
        return isinstance(other, Tape) and self._cells == other._cells and self.head == other.head and self.empty_cell == other.empty_cell

    def __repr__(self):
        return f"Tape({self._cells!r}, head={self.head}, empty_cell={self.empty_cell!r})"

    def copy(self):
        return copy.deepcopy(self)


class TransitionRule:
    def __init__(self, cur_state: str, cur_symbol: str, new_state: str, write_symbol: str, move: str):
        self.cur_state = cur_state
        self.cur_symbol = cur_symbol
        self.new_state = new_state
        self.write_symbol = write_symbol
        self.move = move

    def matches(self, state: str, symbol: str) -> bool:
        return self.cur_state == state and self.cur_symbol == symbol

    def __repr__(self):
        return f"{self.cur_state} {self.cur_symbol} -> {self.new_state} {self.write_symbol} {self.move}"

    def __eq__(self, other):
        return isinstance(other, TransitionRule) and self.__dict__ == other.__dict__


class Program:
    def __init__(self, alphabet: Optional[list[str]] = None, empty_cell: str = '_', start_state: str = 'q0', states: Optional[list[str]] = None):
        self.alphabet = alphabet or []
        self.empty_cell = empty_cell
        self.start_state = start_state
        self.accept_states = set(states or [])
        self.rules: list[TransitionRule] = []

    def add_rule(self, rule: TransitionRule):
        self.rules.append(rule)

    def remove_rule(self, rule: TransitionRule):
        self.rules = [r for r in self.rules if r != rule]

    def find_rule(self, state: str, symbol: str) -> Optional[TransitionRule]:
        for r in self.rules:
            if r.matches(state, symbol):
                return r
        return None

    def list_rules(self) -> list[str]:
        return [repr(r) for r in self.rules]

    @classmethod
    def from_stream(cls, f: TextIO) -> tuple['Program', Tape]:
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
        return copy.deepcopy(self)

class TuringMachine:
    def __init__(self, program: Program, tape: Tape):
        self.program = program
        self.tape = tape
        self.current_state = program.start_state
        self.step_count = 0

    def is_accept(self) -> bool:
        return self.current_state in self.program.accept_states

    def step(self) -> bool:
        """One transition. Returns True if a transition was applied, False if no applicable rule (halt)."""
        cur_symbol = self.tape.read()
        rule = self.program.find_rule(self.current_state, cur_symbol)
        if rule is None:
            return False
        self.tape.write(rule.write_symbol)
        self.tape.move(rule.move)
        self.current_state = rule.new_state
        self.step_count += 1
        return True

    def run(self, max_steps: Optional[int] = None, log: bool = False):
        while True:
            if log:
                print(f"Step {self.step_count}: state={self.current_state}, head={self.tape.head}, symbol={self.tape.read()}")
                print(self.tape.as_str())
            if self.is_accept():
                if log:
                    print("Machine is in accepting state:", self.current_state)
                break
            applied = self.step()
            if not applied:
                if log:
                    print("No applicable rule. Machine halts.")
                break
            if max_steps is not None and self.step_count >= max_steps:
                if log:
                    print(f"Reached max_steps={max_steps}. Stopping.")
                break

    def __repr__(self):
        return f"TuringMachine(state={self.current_state}, steps={self.step_count})"

    def copy(self):
        return TuringMachine(self.program.copy(), self.tape.copy())
