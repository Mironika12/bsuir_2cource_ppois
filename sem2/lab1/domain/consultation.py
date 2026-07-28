from __future__ import annotations
from datetime import date


class Consultation:
    """
    Консультация по конкретному курсовому проекту.
    Является неизменяемым фактом встречи.
    """

    def __init__(
        self,
        consultation_date: date,
        project: CourseProject,
        project_manager: ProjectManager,
        student: Student,
    ) -> None:

        if not isinstance(consultation_date, date):
            raise TypeError("Дата должна быть объектом date.")

        # Проверка согласованности
        if project.supervisor is not project_manager:
            raise ValueError("Руководитель не закреплён за данным проектом.")

        if project.student is not student:
            raise ValueError("Студент не связан с данным проектом.")

        self.__date = consultation_date
        self.__project = project
        self.__project_manager = project_manager
        self.__student = student

        project_manager.register_consultation(self)

    @property
    def consultation_date(self) -> date:
        return self.__date

    @property
    def project(self) -> CourseProject:
        return self.__project

    @property
    def project_manager(self) -> ProjectManager:
        return self.__project_manager

    @property
    def student(self) -> Student:
        return self.__student