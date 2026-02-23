import pytest
from datetime import date
from domain.deadline import Deadline


def test_deadline_valid():
    d = Deadline(date.today())
    assert d.deadline_date <= d.semester_end_date


def test_deadline_invalid_type():
    with pytest.raises(TypeError):
        Deadline("2026-05-10")


def test_deadline_after_semester():
    future = date.today().replace(year=date.today().year + 2)
    with pytest.raises(ValueError):
        Deadline(future)