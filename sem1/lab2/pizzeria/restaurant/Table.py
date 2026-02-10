class Table:
    def __init__(self, number: int, seats: int, reserved: bool):
        self._number = number
        self._seats = seats
        self._reserved = reserved

    def get_number(self) -> int:
        return self._number

    def is_reserved(self) -> bool:
        return self._reserved

    def reserve(self):
        """Забронировать стол"""
        if not self._reserved:
            self._reserved = True
            return True
        return False

    def free_table(self):
        """Освободить стол"""
        if self._reserved:
            self._reserved = False
            return True
        return False
