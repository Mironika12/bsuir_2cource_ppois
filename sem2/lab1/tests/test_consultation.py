import pytest
from datetime import date
from domain.student import Student
from domain.project_manager import ProjectManager


def test_add_consultation_success():
    student = Student("Иван Иванов", "12345678")
    project = student.create_project()
    supervisor = ProjectManager("И. И. Иванов")
    supervisor.assign_project(project)

    project.add_consultation(date.today())

    assert len(project.consultations) == 1
    assert len(supervisor.consultations) == 1


def test_consultation_without_supervisor():
    student = Student("Иван Иванов", "12345678")
    project = student.create_project()

    with pytest.raises(ValueError):
        project.add_consultation(date.today())