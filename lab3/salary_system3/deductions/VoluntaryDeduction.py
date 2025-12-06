class VoluntaryDeduction:
    def __init__(self, deduction_id: str, employee_consent: bool, amount: float):
        self.deduction_id = deduction_id
        self.employee_consent = employee_consent
        self.amount = amount

    def start(self):
        self.employee_consent = True

    def stop(self):
        self.employee_consent = False
