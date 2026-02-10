from .PaymentGatewayAdapter import PaymentGatewayAdapter
from .PaymentInstruction import PaymentInstruction

class BankTransferAdapter(PaymentGatewayAdapter):
    def __init__(self, adapter_id: str, bank_name: str, api_endpoint: str):
        super().__init__(adapter_id, config={}, supported_methods=["bank_transfer"])
        self.bank_name: str = bank_name
        self.api_endpoint: str = api_endpoint

    def submit_payment(self, instruction: "PaymentInstruction") -> bool:
        if not instruction.validate():
            return False

        self._payment_status[instruction.instruction_id] = "pending"
        return True

    def handle_callback(self, instruction_id: str, status: str) -> bool:
        return status in ["success", "failed"]
    
    def check_status(self, instruction_id: str) -> str:
        return self._payment_status.get(instruction_id, "unknown")
