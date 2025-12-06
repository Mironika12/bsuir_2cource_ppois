class AllowanceComponent:
    def __init__(self, component_id: str, allowance_type: str, amount: float):
        self.component_id = component_id
        self.allowance_type = allowance_type
        self.amount = amount

    def is_taxable(self):
        return self.allowance_type.lower() in ["transport", "meal", "housing"]

    def apply_cap(self, cap_value):
        if self.amount > cap_value:
            self.amount = cap_value
        return self.amount
