# cleaning_schedule.py
class CleaningSchedule:
    def __init__(self, area: str, frequency: str):
        self._area = area              # например: "кухня"
        self._frequency = frequency    # например: "ежедневно"
        self._last_done = None         # хранит строку с датой выполнения

    def get_area(self) -> str:
        return self._area

    def get_frequency(self) -> str:
        return self._frequency

    def get_last_done(self):
        return self._last_done

    def mark_done(self) -> str:
        """Отмечает выполнение уборки (для простоты — просто текст)."""
        self._last_done = "completed"
        return f"Уборка зоны '{self._area}' выполнена."
