class OvertimePolicy:
    def __init__(self, policy_id: str, multiplier: float, threshold: float):
        self.policy_id: str = policy_id
        self.multiplier: float = multiplier
        self.threshold: float = threshold

    def compute_overtime_pay(self, hours: float, base_rate: float) -> float:
        if hours <= self.threshold:
            return 0.0
        overtime_hours = hours - self.threshold
        return overtime_hours * base_rate * self.multiplier

    def is_eligible(self, hours: float) -> bool:
        return hours > self.threshold
