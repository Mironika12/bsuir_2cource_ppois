from pizzeria.core.Employee import Employee

class Cleaner(Employee):
    def __init__(self, employee_id, name, phone, role, salary, assigned_zones):
        super().__init__(employee_id, name, phone, role, salary)
        self._assigned_zones = assigned_zones or []
        self._completed_tasks = 0

    def assign_zone(self, zone: str):
        """Назначить уборщику новую зону"""
        if zone not in self._assigned_zones:
            self._assigned_zones.append(zone)

    def get_assigned_zones(self) -> list:
        """Получить список зон, за которые отвечает уборщик"""
        return self._assigned_zones

    def complete_cleaning(self, zone: str) -> str:
        """Отметить уборку в зоне"""
        if zone not in self._assigned_zones:
            return f"Зона '{zone}' не закреплена за уборщиком {self.get_name()}."

        self._completed_tasks += 1
        return f"Уборка в зоне '{zone}' выполнена."

    def get_completed_tasks(self) -> int:
        """Количество выполненных уборок"""
        return self._completed_tasks