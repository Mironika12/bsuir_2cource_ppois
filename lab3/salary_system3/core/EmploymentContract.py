class EmploymentContract:
    def __init__(self, contract_id: int, employee_id: int, terms: dict):
        self.contract_id = contract_id
        self.employee_id = employee_id
        self.terms = terms
        self.active = True

    def is_active(self) -> bool:
        return self.active

    def terminate(self) -> None:
        self.active = False

    def __repr__(self):
        return f"EmploymentContract(contract_id={self.contract_id}, employee_id={self.employee_id}, active={self.active})"
