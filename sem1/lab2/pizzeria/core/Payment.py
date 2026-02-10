class Payment:
    def __init__(self, payment_id: int, amount: float, method: str, status: str):
        self._payment_id = payment_id
        self._amount = amount
        self._method = method      # "cash", "card", "online"
        self._status = status      # "pending", "paid", "failed"
        self._transaction_code = None

    def process(self):
        """Имитация обработки платежа"""
        if self._amount <= 0:
            self._status = "failed"
            return False

        self._status = "paid"
        self._transaction_code = f"TXN-{self._payment_id}-{self._amount}"
        return True

    def refund(self):
        """Имитация возврата средств"""
        if self._status != "paid":
            return False

        self._status = "refunded"
        return True

    def get_payment_id(self) -> int:
        return self._payment_id

    def get_amount(self) -> float:
        return self._amount

    def get_method(self) -> str:
        return self._method

    def get_status(self) -> str:
        return self._status

    def get_transaction_code(self) -> str:
        return self._transaction_code
