class BenefitDeduction:
    def __init__(self, benefit_id: str, employee_share: int, plan_id: str):
        self.benefit_id = benefit_id
        self.employee_share = employee_share
        self.plan_id = plan_id

    def deduct(self, amount):
        return amount * self.employee_share

    def reconcile(self, paid_amount):
        expected = paid_amount * self.employee_share
        return paid_amount - expected
