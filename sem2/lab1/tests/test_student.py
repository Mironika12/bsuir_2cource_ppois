import pytest
from domain.student import Student


def test_create_project_success():
    student = Student("Иван Иванов", "12345678")
    project = student.create_project()

    assert student.course_project is project
    assert project.student is student


def test_create_project_twice():
    student = Student("Иван Иванов", "12345678")
    student.create_project()

    with pytest.raises(ValueError):
        student.create_project()


def test_empty_name():
    with pytest.raises(ValueError):
        Student("", "12345678")