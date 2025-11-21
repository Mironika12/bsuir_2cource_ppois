class MaintenanceRequest:
    def __init__(self, equipment: str, description: str):
        self._equipment = equipment
        self._description = description
        self._fixed = False

    def get_equipment(self) -> str:
        return self._equipment

    def get_description(self) -> str:
        return self._description

    def is_fixed(self) -> bool:
        return self._fixed

    def mark_fixed(self) -> str:
        """Помечает запрос как выполненный."""
        self._fixed = True
        return f"Оборудование '{self._equipment}' успешно отремонтировано."
