from __future__ import annotations

from model.repository import StudentRepository


class SearchService:
    def __init__(self, repo: StudentRepository):
        self.repo = repo

    def find_by_group(self, group: str):
        return [
            s for s in self.repo.get_all_students()
            if s.group == group
        ]

    def find_by_subject_and_score(self, subject, min_score, max_score):
        result = []

        for student in self.repo.get_all_students():
            for exam in student.exams:
                if subject == exam.subject and min_score <= exam.score <= max_score:
                    result.append(student)
                    break

        return result

    def find_by_avg_and_subject(self, subject, min_avg, max_avg):
        result = []

        for student in self.repo.get_all_students():
            avg = student.get_average_score()
            has_subject = any(e.subject == subject for e in student.exams)

            if has_subject and min_avg <= avg <= max_avg:
                result.append(student)

        return result