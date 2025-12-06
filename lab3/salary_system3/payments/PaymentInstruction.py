from salary_system3.core.Payee import Payee

class PaymentInstruction:
    def __init__(self, instruction_id: str, payee: "Payee", amount: float):
        self.instruction_id: str = instruction_id
        self.payee: "Payee" = payee
        self.amount: float = amount

    def validate(self) -> bool:
        return self.amount > 0 and self.payee.validate_account()

    def to_bank_format(self) -> dict:
        return {
            "payee_id": self.payee.payee_id,
            "bank_account": self.payee.bank_account,
            "amount": self.amount
        }
