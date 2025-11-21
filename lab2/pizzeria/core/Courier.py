from pizzeria.core.Employee import Employee

class Courier(Employee):
    def __init__(self, employee_id: int, name: str, phone: str, vehicle_type: str, salary: float):
        super().__init__(employee_id, name, phone, "courier", salary)
        self._vehicle_type = vehicle_type
        self._deliveries_completed = 0

    def complete_delivery(self):
        """Завершить доставку"""
        self._deliveries_completed += 1

    def get_vehicle_type(self) -> str:
        return self._vehicle_type

    def get_deliveries_completed(self) -> int:
        return self._deliveries_completed
