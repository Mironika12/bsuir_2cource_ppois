from salary_system3.deductions.BenefitDeduction import BenefitDeduction

class BenefitEnrollment:
    def __init__(self, enrollment_id: str, employee_id: str, plan_id: str):
        self.enrollment_id: str = enrollment_id
        self.employee_id: str = employee_id
        self.plan_id: str = plan_id
        self.active: bool = False
        self.benefit_deduction: "BenefitDeduction" | None = None

    def enroll(self, benefit_deduction: "BenefitDeduction") -> bool:
        self.active = True
        self.benefit_deduction = benefit_deduction
        return self.active

    def cancel_enrollment(self) -> bool:
        self.active = False
        self.benefit_deduction = None
        return True
