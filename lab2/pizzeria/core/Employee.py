class Employee:
    def __init__(self, employee_id: int, name: str, phone: str, role: str, salary: float):
        self._employee_id = employee_id
        self._name = name
        self._phone = phone
        self._role = role
        self._salary = salary
        self._work_hours = 0

    def add_work_hours(self, hours: float):
        """Добавить рабочие часы за смену"""
        if hours > 0:
            self._work_hours += hours

    def calculate_monthly_payment(self) -> float:
        """Простая имитация зарплаты"""
        return self._salary + (self._work_hours * 2)

    def get_employee_id(self) -> int:
        return self._employee_id

    def get_name(self) -> str:
        return self._name

    def get_role(self) -> str:
        return self._role

    def get_phone(self) -> str:
        return self._phone

    def get_salary(self) -> float:
        return self._salary

    def get_work_hours(self) -> int:
        return self._work_hours
