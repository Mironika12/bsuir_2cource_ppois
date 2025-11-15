from typing import Optional
from .Program import Program
from .Tape import Tape

# разделить

class TuringMachine:
    """
    Represents a running Turing machine instance.

    Parameters
    ----------
    program : Program
        The program defining transitions and states.
    tape : Tape
        The machine's tape.
    """

    def __init__(self, program: Program, tape: Tape):
        self.program = program
        self.tape = tape
        self.current_state = program.start_state
        self.step_count = 0

    def is_accept(self) -> bool:
        """
        Checks whether the current state is accepting.

        Returns
        -------
        bool
        """
        return self.current_state in self.program.accept_states

    def step(self) -> bool:
        """
        Performs one transition step.

        Returns
        -------
        bool
            True if a transition was applied, False if no applicable rule exists.
        """
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
        """
        Runs the machine until acceptance or halt.

        Parameters
        ----------
        max_steps : int, optional
            Maximum number of steps to execute. If None, runs indefinitely.
        log : bool, default=False
            Whether to print step-by-step execution logs.
        """
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
        """
        Returns a deep copy of the machine, including program and tape.

        Returns
        -------
        TuringMachine
        """
        return TuringMachine(self.program.copy(), self.tape.copy())
