class DeductionRule:
    def __init__(self, rule_id: str, rule_type: str, priority: str):
        self.rule_id = rule_id
        self.rule_type = rule_type
        self.priority = priority

    def apply(self, amount):
        if amount < 0:
            return amount
        if self.rule_type == "fixed":
            return max(0, amount - 100)
        if self.rule_type == "percent":
            return max(0, amount * 0.9)
        return amount

    def is_applicable(self):
        return True
