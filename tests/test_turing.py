from turing import Tape, Program, TuringMachine, TransitionRule
import pytest, io

def test_read_initial():
    tape = Tape(["1", "0", "_"], head=0)
    assert tape.read() == "1"


def test_write_changes_cell():
    tape = Tape(["1", "0"])
    tape.write("X")
    assert tape.read() == "X"


def test_move_right():
    tape = Tape(["1", "0"], head=0)
    tape.move("R")
    assert tape.head == 1
    assert tape.read() == "0"


def test_move_left_expands_tape():
    tape = Tape(["1", "0"], head=0)
    tape.move("L")
    assert tape.head == 0                # head shifts because tape expands left
    assert tape.read() == "_"            # new cell created
    assert tape.content() == ["_", "1", "0"]


def test_move_unknown_direction():
    tape = Tape(["1"])
    with pytest.raises(ValueError):
        tape.move("A")


def test_ensure_index_expands_right():
    tape = Tape(["1", "0"])
    tape.set_head(5)
    assert len(tape.content()) == 6
    assert tape.read() == "_"


def test_set_head():
    tape = Tape(["1", "0", "1"])
    tape.set_head(2)
    assert tape.head == 2
    assert tape.read() == "1"


def test_content_returns_copy():
    tape = Tape(["1", "0"])
    c = tape.content()
    c[0] = "X"
    assert tape._cells[0] == "1"


def test_as_str_format():
    tape = Tape(["1", "0", "1"], head=1)
    s = tape.as_str()
    # Проверяем, что в выводе есть строки и указатель
    assert "1 0 1" in s
    assert "^" in s
    assert "head at 1" in s


def test_from_tokens():
    t = Tape.from_tokens(["A", "B", "C"], head=2)
    assert t.read() == "C"
    assert t.head == 2


def test_eq_same():
    t1 = Tape(["1", "0"], head=1)
    t2 = Tape(["1", "0"], head=1)
    assert t1 == t2


def test_eq_different_cells():
    t1 = Tape(["1", "0"])
    t2 = Tape(["1", "1"])
    assert t1 != t2


def test_eq_different_head():
    t1 = Tape(["1", "0"], head=0)
    t2 = Tape(["1", "0"], head=1)
    assert t1 != t2


def test_copy_is_deepcopy():
    tape = Tape(["1", "0"])
    clone = tape.copy()
    assert tape == clone
    clone.write("X")
    assert tape != clone       # доказательство, что копия независима

def test_transition_rule_matches_true():
    r = TransitionRule("q0", "1", "q1", "0", "R")
    assert r.matches("q0", "1") is True


def test_transition_rule_matches_false_state():
    r = TransitionRule("q0", "1", "q1", "0", "R")
    assert r.matches("q1", "1") is False


def test_transition_rule_matches_false_symbol():
    r = TransitionRule("q0", "1", "q1", "0", "R")
    assert r.matches("q0", "0") is False


def test_transition_rule_equality():
    r1 = TransitionRule("q0", "1", "q1", "0", "R")
    r2 = TransitionRule("q0", "1", "q1", "0", "R")
    assert r1 == r2


def test_transition_rule_repr():
    r = TransitionRule("q0", "1", "q1", "0", "R")
    assert repr(r) == "q0 1 -> q1 0 R"


# ---------- Program basic behavior ----------

def test_program_add_and_remove_rule():
    p = Program()
    r = TransitionRule("q0", "1", "q1", "0", "R")

    p.add_rule(r)
    assert p.rules == [r]

    p.remove_rule(r)
    assert p.rules == []


def test_program_find_rule():
    p = Program()
    r1 = TransitionRule("q0", "1", "q1", "0", "R")
    r2 = TransitionRule("q1", "0", "q2", "1", "L")

    p.add_rule(r1)
    p.add_rule(r2)

    assert p.find_rule("q0", "1") == r1
    assert p.find_rule("q1", "0") == r2
    assert p.find_rule("q2", "_") is None


def test_program_list_rules():
    p = Program()
    r = TransitionRule("q0", "1", "q1", "0", "R")
    p.add_rule(r)

    assert p.list_rules() == ["q0 1 -> q1 0 R"]


# ---------- Program.from_stream ----------

def test_program_from_stream_parsing():
    data = """
    alphabet: 0,1
    empty_cell: _
    start: q0
    accept: qf
    tape: 1 0 1
    head: 1
    rules:
    q0 1 -> q1 0 R
    q1 0 -> qf 1 N
    """

    stream = io.StringIO(data)
    prog, tape = Program.from_stream(stream)

    # basic fields
    assert prog.alphabet == ["0", "1"]
    assert prog.empty_cell == "_"
    assert prog.start_state == "q0"
    assert prog.accept_states == {"qf"}

    # tape
    assert tape.content() == ["1", "0", "1"]
    assert tape.head == 1

    # rules
    assert len(prog.rules) == 2
    assert repr(prog.rules[0]) == "q0 1 -> q1 0 R"
    assert repr(prog.rules[1]) == "q1 0 -> qf 1 N"


def test_program_from_stream_no_tape_defaults_to_empty_cell():
    data = """
    alphabet: a,b
    start: q0
    accept: q1
    rules:
    q0 _ -> q1 a R
    """

    stream = io.StringIO(data)
    prog, tape = Program.from_stream(stream)

    assert tape.content() == ["_"]
    assert tape.head == 0
    assert prog.rules[0].cur_state == "q0"
    assert prog.rules[0].write_symbol == "a"


def test_program_copy_independent():
    p = Program()
    r = TransitionRule("q0", "1", "q1", "0", "R")
    p.add_rule(r)

    c = p.copy()
    assert c is not p
    assert c.rules is not p.rules
    assert c.rules[0] == p.rules[0]

def make_simple_machine():
    """
    Создает простую МТ:
    q0, '1' -> q1, '0', R
    q1 — accepting
    """
    prog = Program(start_state='q0', states=['q1'])
    prog.add_rule(TransitionRule('q0', '1', 'q1', '0', 'R'))
    tape = Tape(['1', '_'], head=0)
    return TuringMachine(prog, tape)


# ----------------------------------------------------------
# Tests
# ----------------------------------------------------------

def test_initial_state():
    tm = make_simple_machine()
    assert tm.current_state == 'q0'
    assert tm.step_count == 0
    assert tm.tape.read() == '1'


def test_single_step_changes_tape_and_state():
    tm = make_simple_machine()
    applied = tm.step()

    assert applied is True
    assert tm.current_state == 'q1'
    assert tm.tape.head == 1
    assert tm.tape.read() == '_'        # после движения вправо
    assert tm.tape.content() == ['0', '_']
    assert tm.step_count == 1


def test_step_no_rule_returns_false():
    prog = Program(start_state='q0')
    tape = Tape(['1'])
    tm = TuringMachine(prog, tape)

    applied = tm.step()

    assert applied is False
    assert tm.current_state == 'q0'
    assert tm.step_count == 0


def test_run_accept_state_stops_immediately():
    prog = Program(start_state='q0', states=['q0'])   # q0 — accepting
    tape = Tape(['1'])
    tm = TuringMachine(prog, tape)

    tm.run()

    assert tm.is_accept()
    assert tm.step_count == 0   # не было шагов
    assert tm.current_state == 'q0'


def test_run_stops_when_no_rule():
    prog = Program(start_state='q0', states=['q_accept'])
    prog.add_rule(TransitionRule('q0', '1', 'q0', '1', 'R'))  # будет двигаться вправо, пока символы '1'
    tape = Tape(['1', '1', '1'], head=0)

    tm = TuringMachine(prog, tape)
    tm.run()

    # остановится на пустой ячейке, где нет правила
    assert tm.step_count == 3
    assert tm.current_state == 'q0'
    assert tm.tape.head == 3
    assert tm.tape.read() == '_'  # вышел за границы и остановился


def test_run_max_steps_limit():
    prog = Program(start_state='q0')
    prog.add_rule(TransitionRule('q0', '_', 'q0', '_', 'R'))
    tape = Tape(['_'], head=0)

    tm = TuringMachine(prog, tape)
    tm.run(max_steps=5)

    assert tm.step_count == 5
    assert tm.current_state == 'q0'
    assert tm.tape.head == 5


def test_copy_machine():
    tm = make_simple_machine()
    tm2 = tm.copy()

    assert tm2 is not tm
    assert tm2.program is not tm.program
    assert tm2.tape is not tm.tape

    # эквивалентны по содержимому
    assert tm2.current_state == tm.current_state
    assert tm2.program.rules[0] == tm.program.rules[0]
    assert tm2.tape.content() == tm.tape.content()


def test_machine_repr_contains_state_and_steps():
    tm = make_simple_machine()
    repr_text = repr(tm)

    assert "state=" in repr_text
    assert "steps=" in repr_text


def test_machine_reaches_accept_state():
    prog = Program(start_state='q0', states=['q2'])
    prog.add_rule(TransitionRule('q0', '1', 'q1', '1', 'R'))
    prog.add_rule(TransitionRule('q1', '_', 'q2', '_', 'N'))  # accept

    tape = Tape(['1', '_'], head=0)
    tm = TuringMachine(prog, tape)

    tm.run()

    assert tm.is_accept()
    assert tm.current_state == 'q2'
    assert tm.step_count == 2