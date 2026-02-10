class Statistic:
    def __init__(self, name: str, value: float):
        self._name = name
        self._value = value

    def get_name(self) -> str:
        return self._name

    def get_value(self) -> float:
        return self._value

    def update_value(self, new_value: float):
        """Обновляет значение метрики."""
        self._value = new_value
