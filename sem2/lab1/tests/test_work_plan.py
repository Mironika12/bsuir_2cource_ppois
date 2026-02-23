import pytest
from datetime import date
from domain.work_plan import WorkPlan
from domain.deadline import Deadline


def valid_item():
    return {
        "num": 1,
        "task": "Изучить источники",
        "deadline": Deadline(date.today()),
        "notes": None,
    }


def test_add_item():
    plan = WorkPlan()
    item = valid_item()

    plan += item

    assert len(plan.items) == 1


def test_invalid_item_structure():
    plan = WorkPlan()

    with pytest.raises(ValueError):
        plan += {"num": 1}


def test_remove_item():
    plan = WorkPlan()
    item = valid_item()

    plan += item
    plan -= item

    assert len(plan.items) == 0