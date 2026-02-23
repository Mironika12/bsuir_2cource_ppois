from __future__ import annotations
import re
from typing import List

from domain.consultation import Consultation


class ProjectManager:
    """
    Руководитель курсовых проектов.
    Хранит список закреплённых проектов и проведённых консультаций.
    """

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Имя должно быть строкой.")

        if not re.fullmatch(r"[А-Я]\. *[А-Я]\. *[А-Я][а-я]+", name):
            raise ValueError("Имя должно быть в формате: И. И. Иванов")

        self.__name: str = name
        self.__projects: List[CourseProject] = []
        self.__consultations: List[Consultation] = []

    # =====================================================
    # ---------------------- PROPERTIES -------------------
    # =====================================================

    @property
    def name(self) -> str:
        return self.__name

    @property
    def projects(self) -> List[CourseProject]:
        return list(self.__projects)

    @property
    def consultations(self) -> List[Consultation]:
        return list(self.__consultations)

    # =====================================================
    # ---------------------- ПРОЕКТЫ ----------------------
    # =====================================================

    def assign_project(self, project: CourseProject) -> None:
        # if not isinstance(project, CourseProject):
        #     raise TypeError("Ожидается CourseProject.")

        if project in self.__projects:
            raise ValueError("Проект уже закреплён за руководителем.")

        self.__projects.append(project)
        project.assign_supervisor(self)

    def remove_project(self, project: CourseProject) -> None:
        if project not in self.__projects:
            raise ValueError("Проект не найден у данного руководителя.")

        self.__projects.remove(project)

    # =====================================================
    # ------------------- КОНСУЛЬТАЦИИ --------------------
    # =====================================================

    def register_consultation(self, consultation: Consultation) -> None:
        if not isinstance(consultation, Consultation):
            raise TypeError("Ожидается Consultation.")

        if consultation in self.__consultations:
            raise ValueError("Консультация уже зарегистрирована.")

        self.__consultations.append(consultation)

    def remove_consultation(self, consultation: Consultation) -> None:
        if consultation not in self.__consultations:
            raise ValueError("Консультация не найдена.")

        self.__consultations.remove(consultation)