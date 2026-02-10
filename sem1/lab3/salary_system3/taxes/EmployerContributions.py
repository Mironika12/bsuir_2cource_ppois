class EmployerContributions:
    def __init__(self, contrib_id: str, type: str, rate: float):
        self.contrib_id: str = contrib_id
        self.type: str = type
        self.rate: float = rate

    def calculate(self, base_amount: float) -> float:
        return base_amount * self.rate

    def allocate(self, employee_id: str) -> dict:
        return {"employee_id": employee_id, "contribution": self.rate}
