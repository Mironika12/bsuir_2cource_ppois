from __future__ import annotations
from typing import List

from domain.reference import Reference


class Research:
    """ Хранит источники исследования и управляет их статусом."""

    def __init__(self) -> None:
        self.__references: List[Reference | dict] = []


    @property
    def references(self) -> List[Reference  | dict]:
        return list(self.__references)
    

    def __validate_reference(self, reference: Reference | dict) -> None:
        if not isinstance(reference, dict):
            raise TypeError("Источник должен быть словарём.")

        if "reference" not in reference:
            raise ValueError("Отсутствует ключ 'reference'.")

        if not isinstance(reference["reference"], str) or not reference["reference"].strip():
            raise ValueError("Название источника должно быть непустой строкой.")

        if "is_read" in reference and not isinstance(reference["is_read"], bool):
            raise TypeError("Поле 'is_read' должно быть bool.")


    def add_reference(self, reference: Reference | dict) -> None:
        self.__validate_reference(reference)

        if "is_read" not in reference:
            reference["is_read"] = False

        self.__references.append(reference)


    def mark_as_read(self, index: int) -> None:
        try:
            self.__references[index]["is_read"] = True
        except IndexError:
            raise ValueError("Источник не найден.")


    def get_unread(self) -> List[str]:
        return [
            ref["reference"]
            for ref in self.__references
            if not ref["is_read"]
        ]