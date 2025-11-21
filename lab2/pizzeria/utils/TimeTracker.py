from pizzeria.core.Employee import Employee
from exceptions.exceptions import NegativeHoursException

class TimeTracker:
    def __init__(self, employee: Employee):
        self.employee = employee
        self.hours_worked = 0

    def add_hours(self, hours: float):
        if hours < 0:
            raise NegativeHoursException(hours)
        self.hours_worked += hours