from salary_system3.compensation.CompensationPackage import CompensationPackage
from salary_system3.deductions.DeductionRule import DeductionRule
from salary_system3.core.Employee import Employee

class SalaryCalculator:
    def __init__(
        self,
        calculator_id: str,
        rules_engine: list,
        context: dict,
        compensation_package: "CompensationPackage",
        deduction_rules: list
    ):
        self.calculator_id: str = calculator_id
        self.rules_engine: list = rules_engine
        self.context: dict = context
        self.compensation_package: "CompensationPackage" = compensation_package
        self.deduction_rules: list["DeductionRule"] = deduction_rules
        self.explanations: list[str] = []

    def calculate(self, employee: "Employee", period: str) -> float:
        total = self.compensation_package.calculate_total()
        for rule in self.deduction_rules:
            if rule.is_applicable():
                total -= rule.apply(total)
        self.explanations.append(f"Calculated for employee {employee.id} in period {period}")
        return total

    def explain(self) -> list:
        return self.explanations
