from pizzeria.core.Employee import Employee

class Schedule:
    def __init__(self, employee: Employee, shifts: list[str]):
        self._employee = employee
        self._shifts = shifts

    def get_employee(self):
        return self._employee

    def get_shifts(self):
        return self._shifts

    def add_shift(self, shift: str):
        """Добавить смену сотруднику"""
        if shift not in self._shifts:
            self._shifts.append(shift)
