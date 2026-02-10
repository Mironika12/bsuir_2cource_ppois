from .BaseSalaryComponent import BaseSalaryComponent

class CompensationPackage:
    def __init__(self, package_id: int, employee_id: int, components: list[BaseSalaryComponent] | None = None):
        self.package_id = package_id
        self.employee_id = employee_id
        self.components = components if components else []

    def calculate_total(self) -> float:
        total = 0.0
        for component in self.components:
            if hasattr(component, "get_amount"):
                total += component.get_amount()
        return total

    def __repr__(self):
        return f"CompensationPackage(package_id={self.package_id}, employee_id={self.employee_id})"
