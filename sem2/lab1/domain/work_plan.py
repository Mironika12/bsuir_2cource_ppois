from __future__ import annotations
from typing import List

from domain.item import Item
from domain.deadline import Deadline


class WorkPlan:
    """
    План выполнения курсового проекта.
    Отвечает только за хранение и валидацию структуры пунктов.
    """

    def __init__(self):
        self.__items: List[Item] = []

    # -------------------- PROPERTIES --------------------

    @property
    def items(self) -> List[Item]:
        # возвращаем копию, чтобы нельзя было изменить список напрямую
        return list(self.__items)

    # -------------------- PRIVATE VALIDATION --------------------

    def __validate_item(self, item: Item) -> None:
        if not isinstance(item, dict):
            raise TypeError("Пункт плана должен быть словарём.")

        required_keys = {"num", "task", "deadline", "notes"}

        if not required_keys.issubset(item.keys()):
            raise ValueError("Некорректная структура пункта плана.")

        if not isinstance(item["num"], int) or item["num"] <= 0:
            raise ValueError("Номер должен быть положительным целым числом.")

        if not isinstance(item["task"], str) or not item["task"].strip():
            raise ValueError("Описание задачи должно быть непустой строкой.")

        if not isinstance(item["deadline"], Deadline):
            raise TypeError("Дедлайн должен быть объектом Deadline.")

        if item["notes"] is not None and not isinstance(item["notes"], str):
            raise TypeError("Заметки должны быть строкой или None.")

    # -------------------- PUBLIC API --------------------

    def __iadd__(self, item: Item):
        self.__validate_item(item)
        self.__items.append(item)
        return self

    def __isub__(self, item: Item):
        try:
            self.__items.remove(item)
        except ValueError:
            raise ValueError("Пункт плана не найден.")
        return self