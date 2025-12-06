from salary_system3.core.Employee import Employee

class PayrollRecord:
    def __init__(self, record_id: str, employee_id: str, employee: "Employee", net_pay: float):
        self.record_id: str = record_id
        self.employee_id: str = employee_id
        self.employee: "Employee" = employee
        self.net_pay: float = net_pay

    def generate_slip(self) -> dict:
        return {
            "record_id": self.record_id,
            "employee_id": self.employee_id,
            "net_pay": self.net_pay
        }

    def recalculate(self, new_net_pay: float) -> None:
        self.net_pay = new_net_pay
