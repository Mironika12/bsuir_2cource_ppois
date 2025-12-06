class Payee:
    def __init__(self, payee_id: int, bank_account: str, legal_name: str):
        self.payee_id = payee_id
        self.bank_account = bank_account
        self.legal_name = legal_name

    def validate_account(self) -> bool:
        return isinstance(self.bank_account, str) and len(self.bank_account) > 0

    def get_routing_info(self) -> dict:
        return {
            "payee_id": self.payee_id,
            "bank_account": self.bank_account
        }

    def __repr__(self):
        return f"Payee(payee_id={self.payee_id}, legal_name='{self.legal_name}')"
