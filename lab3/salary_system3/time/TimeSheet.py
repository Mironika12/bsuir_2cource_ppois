from .TimeEntry import TimeEntry
from .OvertimePolicy import OvertimePolicy


class TimeSheet:
    def __init__(self, timesheet_id: str, employee_id: str, entries: list[TimeEntry], overtime_policy: OvertimePolicy):
        self.timesheet_id: str = timesheet_id
        self.employee_id: str = employee_id
        self.entries: list[TimeEntry] = entries
        self.overtime_policy: OvertimePolicy = overtime_policy

    def add_entry(self, entry: TimeEntry):
        self.entries.append(entry)

    def total_hours(self) -> float:
        total = sum(e.hours for e in self.entries)
        overtime = self.overtime_policy.apply(total)
        return total + overtime
