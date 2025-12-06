class Position:
    def __init__(self, position_id: int, title: str, grade: int, salary_range: tuple | None = None, exempt: bool = False):
        self.id = position_id
        self.title = title
        self.grade = grade
        self.salary_range = salary_range
        self.exempt = exempt

    def get_salary_range(self) -> tuple | None:
        return self.salary_range

    def is_exempt(self) -> bool:
        return self.exempt

    def __repr__(self):
        return f"Position(id={self.id}, title='{self.title}', grade={self.grade})"
