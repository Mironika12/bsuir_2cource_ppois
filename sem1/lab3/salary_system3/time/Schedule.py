class Schedule:
    def __init__(self, schedule_id: str, employee_id: str, shift_pattern: list):
        self.schedule_id: str = schedule_id
        self.employee_id: str = employee_id
        self.shift_pattern: list = shift_pattern
        self.current_index: int = 0

    def next_shift(self) -> str:
        if not self.shift_pattern:
            return ""
        shift = self.shift_pattern[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.shift_pattern)
        return shift

    def is_on_shift(self, shift: str) -> bool:
        return shift in self.shift_pattern
