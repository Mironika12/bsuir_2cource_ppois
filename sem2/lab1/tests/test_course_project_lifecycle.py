import pytest
from datetime import date
from domain.student import Student
from domain.project_manager import ProjectManager
from domain.deadline import Deadline
from domain.project_state import ProjectState


def setup_project():
    student = Student("Иван Иванов", "12345678")
    project = student.create_project()
    supervisor = ProjectManager("И. И. Иванов")
    supervisor.assign_project(project)
    return project


def test_choose_theme():
    project = setup_project()
    project.choose_theme("Новая тема")

    assert project.state == ProjectState.TOPIC_SELECTED


def test_cannot_write_before_research():
    project = setup_project()
    project.choose_theme("Тема")

    with pytest.raises(ValueError):
        project.write_section("Текст")


def test_full_lifecycle_to_submit():
    project = setup_project()

    project.choose_theme("Тема")

    project.add_plan_item({
        "num": 1,
        "task": "Задача",
        "deadline": Deadline(date.today()),
        "notes": None,
    })

    project.add_reference({"reference": "ГОСТ"})
    project.write_section("Текст")

    project.set_deadline(Deadline(date.today()))
    project.submit()

    assert project.state == ProjectState.SUBMITTED

def test_choose_theme_twice():
    project = setup_project()
    project.choose_theme("Тема")

    with pytest.raises(ValueError):
        project.choose_theme("Другая")

def test_set_deadline_in_created():
    project = setup_project()

    with pytest.raises(ValueError):
        project.set_deadline(Deadline(date.today()))