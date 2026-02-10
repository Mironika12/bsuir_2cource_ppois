from .PayrollRecord import PayrollRecord

class Payslip:
    def __init__(
        self,
        payslip_id: str,
        breakdown: dict,
        issued_date: str,
        payroll_record: "PayrollRecord"
    ):
        self.payslip_id: str = payslip_id
        self.breakdown: dict = breakdown
        self.issued_date: str = issued_date
        self.payroll_record: "PayrollRecord" = payroll_record

    def render_pdf(self) -> bytes:
        content = f"Payslip {self.payslip_id} issued {self.issued_date}"
        return content.encode("utf-8")

    def send_to_employee(self) -> bool:
        return True
