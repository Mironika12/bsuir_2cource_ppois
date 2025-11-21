class Apron:
    """
    Описывает фартук персонала (экипировка) — модель, цвет, состояние чистоты.
    Это полезно для дисплея экипировки, выдачи на смену и проверки состояния.
    """
    def __init__(self, size: str, color: str, assigned_to: int | None = None):
        self._size = size
        self._color = color
        self._assigned_to = assigned_to  # employee_id или None
        self._is_clean = True

    def assign_to(self, employee_id: int):
        self._assigned_to = employee_id

    def unassign(self):
        self._assigned_to = None

    def mark_dirty(self):
        self._is_clean = False

    def wash(self):
        self._is_clean = True

    def is_clean(self) -> bool:
        return self._is_clean

    def get_info(self) -> dict:
        return {
            "size": self._size,
            "color": self._color,
            "assigned_to": self._assigned_to,
            "is_clean": self._is_clean,
        }
