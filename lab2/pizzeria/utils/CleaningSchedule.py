class CleaningSchedule:
    def __init__(self, area: str, frequency: str):
        self._area = area  
        self._frequency = frequency 
        self._last_done = None  

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
