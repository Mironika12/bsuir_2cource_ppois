class Garnishment:
    def __init__(self, garnishment_id: str, court_order_ref: str, amount: int):
        self.garnishment_id = garnishment_id
        self.court_order_ref = court_order_ref
        self.amount = amount

    def apply_garnishment(self, base_amount):
        return max(0, base_amount - self.amount)

    def release(self):
        self.amount = 0
