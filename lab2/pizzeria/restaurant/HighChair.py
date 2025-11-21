class HighChair:
    """
    Детский стульчик — состояние (свободен/занят/сломался)
    """
    def __init__(self, chair_id: str):
        self._chair_id = chair_id
        self._status = "free"  # free / occupied / broken

    def occupy(self):
        if self._status != "free":
            from exceptions.exceptions import InvalidOperationException
            raise InvalidOperationException(f"Нельзя занять стул в состоянии '{self._status}'")
        self._status = "occupied"

    def release(self):
        if self._status == "occupied":
            self._status = "free"

    def mark_broken(self):
        self._status = "broken"

    def get_status(self) -> str:
        return self._status
