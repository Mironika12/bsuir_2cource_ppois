class BaseSalaryComponent:
    def __init__(self, component_id: str, amount: float, currency: str):
        self.component_id = component_id
        self.amount = amount
        self.currency = currency

    def prorate(self, ratio):
        return self.amount * ratio

    def effective_from(self, date):
        return {"component_id": self.component_id, "effective_from": date}
    
    def get_amount(self):
        return self.amount
