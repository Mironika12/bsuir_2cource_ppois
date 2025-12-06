class BonusComponent:
    def __init__(self, component_id: str, bonus_type: str, criteria: float):
        self.component_id = component_id
        self.bonus_type = bonus_type
        self.criteria = criteria

    def evaluate(self, performance_data: dict):
        return performance_data.get(self.criteria, 0)

    def schedule_payout(self, date):
        return {"component_id": self.component_id, "payout_date": date}
