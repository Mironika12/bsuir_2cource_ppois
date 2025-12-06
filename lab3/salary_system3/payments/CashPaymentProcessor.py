class CashPaymentProcessor:
    def __init__(self, processor_id: str, location_id: str, petty_cash_account: str):
        self.processor_id: str = processor_id
        self.location_id: str = location_id
        self.petty_cash_account: str = petty_cash_account
        self.issued_cash: float = 0.0

    def issue_cash(self, amount: float) -> bool:
        self.issued_cash += amount
        return True

    def reconcile_cash(self, actual_cash: float) -> float:
        discrepancy = actual_cash - self.issued_cash
        self.issued_cash = 0.0
        return discrepancy
