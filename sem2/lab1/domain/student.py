from __future__ import annotations
from typing import Optional
import re

from domain.course_project import CourseProject


class Student:
    """
    Студент — участник образовательного процесса.
    Может иметь один курсовой проект.
    """

    def __init__(self, name: str, student_id: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Имя должно быть строкой.")
        
        if not isinstance(student_id, str):
            raise TypeError("Номер студенческого билета должен быть строкой.")

        if not student_id.strip():
            raise ValueError("Номер студенческого билета не может быть пустым.")

        self.__name: str = name
        self.__id = student_id
        self.__course_project: Optional[CourseProject] = None

    # ----------------- PROPERTIES -----------------

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def student_id(self):
        return self.__id

    @property
    def course_project(self) -> Optional[CourseProject]:
        return self.__course_project

    # ----------------- BEHAVIOUR -----------------

    def create_project(self) -> CourseProject:
        if self.__course_project is not None:
            raise ValueError("Проект уже существует.")

        project = CourseProject()
        project.assign_student(self)

        self.__course_project = project
        return project

    def remove_project(self) -> None:
        if self.__course_project is None:
            raise ValueError("Проект отсутствует.")

        self.__course_project = None