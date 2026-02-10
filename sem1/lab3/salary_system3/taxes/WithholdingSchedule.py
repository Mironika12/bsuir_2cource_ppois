from datetime import datetime, timedelta


class WithholdingSchedule:
    def __init__(self, schedule_id: str, frequency: str, rules: dict):
        self.schedule_id: str = schedule_id
        self.frequency: str = frequency
        self.rules: dict = rules
        self.last_withheld_date: str | None = None

    def next_withholding_date(self, current_date: str) -> str:
        date = datetime.strptime(current_date, "%Y-%m-%d")

        if self.frequency == "daily":
            next_date = date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = date + timedelta(weeks=1)
        elif self.frequency == "monthly":
            next_date = date + timedelta(days=30)
        else:
            next_date = date

        return next_date.strftime("%Y-%m-%d")

    def is_due(self, current_date: str) -> bool:
        if self.last_withheld_date is None:
            return True

        next_date = self.next_withholding_date(self.last_withheld_date)
        return current_date >= next_date

    def calculate_withholding_amount(self, gross_salary: float) -> float:
        rate = self.rules.get("rate", 0)
        min_amount = self.rules.get("min_amount", 0)
        max_amount = self.rules.get("max_amount", float("inf"))

        base_amount = gross_salary * rate
        amount = max(base_amount, min_amount)
        amount = min(amount, max_amount)
        return amount

    def mark_withheld(self, date: str):
        self.last_withheld_date = date
