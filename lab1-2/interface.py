import argparse
from turing.Program import Program
from turing.Tape import Tape
from turing.TransitionRule import TransitionRule
from turing.TuringMachine import TuringMachine

def main():
    parser = argparse.ArgumentParser(description="Turing machine interpreter")
    parser.add_argument('file', help="Path to program file")
    parser.add_argument('-log', action='store_true', help="Log after each step")
    parser.add_argument('--max-steps', type=int, default=None, help="Max steps to run")
    args = parser.parse_args()

    with open(args.file, 'r', encoding='utf-8') as f:
        program, tape = Program.from_stream(f)

    tm = TuringMachine(program, tape)
    tm.run(max_steps=args.max_steps, log=args.log)
    print("Final tape:")
    print(tape.as_str())
    print("Final state:", tm.current_state, "steps:", tm.step_count)

if __name__ == '__main__':
    main()
