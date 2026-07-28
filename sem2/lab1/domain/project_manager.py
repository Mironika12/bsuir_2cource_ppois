from __future__ import annotations
import re
from typing import List

from domain.consultation import Consultation
import config as cfg


class ProjectManager:
    """
    Руководитель курсовых проектов.
    Хранит список закреплённых проектов и проведённых консультаций.
    """

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Имя должно быть строкой.")

        if not re.fullmatch(cfg.FIO_TEMPLATE, name):
            raise ValueError("Имя должно быть в формате: И. И. Иванов")

        self.__name: str = name
        self.__projects: List[CourseProject] = [] # type: ignore
        self.__consultations: List[Consultation] = []


    @property
    def name(self) -> str:
        return self.__name

    @property
    def projects(self) -> List[CourseProject]: # type: ignore
        return list(self.__projects)

    @property
    def consultations(self) -> List[Consultation]:
        return list(self.__consultations)


    def assign_project(self, project: CourseProject) -> None: # type: ignore
        if project in self.__projects:
            raise ValueError("Проект уже закреплён за руководителем.")

        self.__projects.append(project)
        project.assign_project_manager(self)


    def remove_project(self, project: CourseProject) -> None: # type: ignore
        if project not in self.__projects:
            raise ValueError("Проект не найден у данного руководителя.")

        self.__projects.remove(project)


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