from abc import ABC, abstractmethod
from typing import List, Dict
from .PaymentInstruction import PaymentInstruction

class PaymentGatewayAdapter(ABC):
    def __init__(self, adapter_id: str, config: Dict, supported_methods: List[str]):
        self.adapter_id: str = adapter_id
        self.config: Dict = config
        self.supported_methods: List[str] = supported_methods

    @abstractmethod
    def submit_payment(self, instruction: "PaymentInstruction") -> bool:
        pass

    @abstractmethod
    def check_status(self, instruction_id: str) -> str:
        pass
