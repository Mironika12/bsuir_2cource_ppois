class TerminationRecord:
    def __init__(self, termination_id: str, employee_id: str, reason: str):
        self.termination_id: str = termination_id
        self.employee_id: str = employee_id
        self.reason: str = reason
        self.exit_processed: bool = False
        self.final_pay: float | None = None

    def process_exit(self) -> bool:
        self.exit_processed = True
        return self.exit_processed

    def calculate_final_pay(self, accrued_pay: float, deductions: float) -> float:
        self.final_pay = accrued_pay - deductions
        return self.final_pay
