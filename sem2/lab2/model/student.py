from __future__ import annotations

from model.exam import Exam

class Student:
    def __init__(self, fio: str, group: str, exams: list[Exam] = []):
        self.id: int | None = None
        self.fio = fio
        self.group = group
        self.exams = exams

    def get_average_score(self) -> float:
        if not self.exams:
            return 0
        return sum(e.score for e in self.exams) / len(self.exams)