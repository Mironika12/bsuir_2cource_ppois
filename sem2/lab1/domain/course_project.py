from __future__ import annotations
from typing import Optional, List
from datetime import date

from domain.project_state import ProjectState
from domain.work_plan import WorkPlan
from domain.research import Research
from domain.consultation import Consultation
from domain.deadline import Deadline
from domain.project_manager import ProjectManager
from domain.item import Item
from domain.reference import Reference


class CourseProject:
    """
    Центральный агрегат предметной области.
    Управляет жизненным циклом курсового проекта.
    """

    def __init__(self) -> None:
        self.__theme: Optional[str] = None
        self.__student: Optional[Student] = None
        self.__supervisor: Optional[ProjectManager] = None
        self.__deadline: Optional[Deadline] = None

        self.__plan: WorkPlan = WorkPlan()
        self.__research: Research = Research()
        self.__consultations: List[Consultation] = []
        self.__text_sections: List[str] = []

        self.__state: ProjectState = ProjectState.CREATED

    # =====================================================
    # -------------------- PROPERTIES ---------------------
    # =====================================================

    @property
    def state(self) -> ProjectState:
        return self.__state

    @property
    def theme(self) -> Optional[str]:
        return self.__theme

    @property
    def student(self) -> Optional[Student]:
        return self.__student

    @property
    def supervisor(self) -> Optional[ProjectManager]:
        return self.__supervisor

    @property
    def deadline(self) -> Optional[Deadline]:
        return self.__deadline

    @property
    def work_plan(self) -> WorkPlan:
        return self.__plan

    @property
    def research(self) -> Research:
        return self.__research
    
    @property
    def consultations(self):
        return list(self.__consultations)

    @property
    def text_sections(self):
        return list(self.__text_sections)

    # =====================================================
    # ---------------- ЖИЗНЕННЫЙ ЦИКЛ ---------------------
    # =====================================================

    def assign_student(self, student: Student) -> None:
        if self.__student is not None:
            raise ValueError("Студент уже назначен.")
        self.__student = student

    def assign_supervisor(self, supervisor: ProjectManager) -> None:
        if self.__supervisor is not None:
            raise ValueError("Руководитель уже назначен.")
        self.__supervisor = supervisor

    # ---------------- Выбор темы ----------------

    def choose_theme(self, theme: str) -> None:
        if self.__state != ProjectState.CREATED:
            raise ValueError("Тему можно выбрать только при создании проекта.")

        if not theme.strip():
            raise ValueError("Тема не может быть пустой.")

        self.__theme = theme
        self.__state = ProjectState.TOPIC_SELECTED

    # ---------------- Планирование ----------------

    def add_plan_item(self, item: Item) -> None:
        if self.__state not in (
            ProjectState.TOPIC_SELECTED,
            ProjectState.PLANNING,
        ):
            raise ValueError("Нельзя редактировать план на этом этапе.")

        self.__plan += item
        self.__state = ProjectState.PLANNING

    def remove_plan_item(self, item: Item) -> None:
        if self.__state not in (
            ProjectState.TOPIC_SELECTED,
            ProjectState.PLANNING,
        ):
            raise ValueError("Нельзя редактировать план на этом этапе.")

        self.__plan -= item

    # ---------------- Исследование ----------------

    def add_reference(self, reference: Reference) -> None:
        if self.__state not in (
            ProjectState.PLANNING,
            ProjectState.RESEARCH,
        ):
            raise ValueError("Исследование недоступно на этом этапе.")

        self.__research.add_reference(reference)
        self.__state = ProjectState.RESEARCH

    # ---------------- Написание текста ----------------

    def write_section(self, text: str) -> None:
        if self.__state not in (
            ProjectState.RESEARCH,
            ProjectState.WRITING,
        ):
            raise ValueError("Нельзя писать текст на этом этапе.")

        if not text.strip():
            raise ValueError("Текст не может быть пустым.")

        self.__text_sections.append(text)
        self.__state = ProjectState.WRITING

    # ---------------- Консультации ----------------

    def add_consultation(self, consultation_date: date) -> None:
        if self.__supervisor is None or self.__student is None:
            raise ValueError("Не назначены участники проекта.")

        consultation = Consultation(
            consultation_date,
            self,
            self.__supervisor,
            self.__student,
        )

        self.__consultations.append(consultation)
        self.__state = ProjectState.CONSULTING

    # ---------------- Дедлайн ----------------

    def set_deadline(self, deadline: Deadline) -> None:
        if not isinstance(deadline, Deadline):
            raise TypeError("Ожидается объект Deadline.")

        if self.__state == ProjectState.CREATED:
            raise ValueError("Нельзя установить дедлайн без выбранной темы.")

        if self.__state == ProjectState.SUBMITTED:
            raise ValueError("Нельзя изменить дедлайн после сдачи проекта.")

        self.__deadline = deadline

    # ---------------- Сдача ----------------

    def submit(self) -> None:
        if self.__state != ProjectState.WRITING:
            raise ValueError("Проект не готов к сдаче.")

        if self.__deadline is None:
            raise ValueError("Не установлен дедлайн.")

        if not self.__text_sections:
            raise ValueError("Отсутствует текст работы.")

        self.__state = ProjectState.SUBMITTED