class TimeEntry:
    def __init__(self, entry_id: str, date: str, hours: float):
        self.entry_id: str = entry_id
        self.date: str = date
        self.hours: float = hours

    def validate(self) -> bool:
        return self.hours >= 0

    def is_overtime(self) -> bool:
        return self.hours > 8
