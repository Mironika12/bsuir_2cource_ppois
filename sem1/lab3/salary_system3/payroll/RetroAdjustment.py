from .PayrollRecord import PayrollRecord

class RetroAdjustment:
    def __init__(
        self,
        adjustment_id: str,
        reason: str,
        amount: float,
        payroll_record: "PayrollRecord"
    ):
        self.adjustment_id: str = adjustment_id
        self.reason: str = reason
        self.amount: float = amount
        self.payroll_record: "PayrollRecord" = payroll_record
        self.applied: bool = False

    def apply_to_record(self) -> float:
        if not self.applied:
            self.payroll_record.net_pay += self.amount
            self.applied = True
        return self.payroll_record.net_pay

    def revert(self) -> float:
        if self.applied:
            self.payroll_record.net_pay -= self.amount
            self.applied = False
        return self.payroll_record.net_pay
