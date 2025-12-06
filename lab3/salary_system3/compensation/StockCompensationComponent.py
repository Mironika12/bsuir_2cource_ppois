class StockCompensationComponent:
    def __init__(self, component_id: str, vesting_schedule: str, quantity: int):
        self.component_id = component_id
        self.vesting_schedule = vesting_schedule
        self.quantity = quantity
        self.vested_quantity = 0

    def vest(self, amount):
        if amount < 0:
            return
        if amount > self.quantity - self.vested_quantity:
            amount = self.quantity - self.vested_quantity
        self.vested_quantity += amount
        return self.vested_quantity

    def forfeit(self, amount):
        if amount < 0:
            return
        if amount > self.quantity - self.vested_quantity:
            amount = self.quantity - self.vested_quantity
        self.quantity -= amount
        return self.quantity
