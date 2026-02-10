from typing import List
from .PaymentInstruction import PaymentInstruction

class PaymentBatch:
    def __init__(self, batch_id: str, instructions: List["PaymentInstruction"], created_at: str):
        self.batch_id: str = batch_id
        self.instructions: List["PaymentInstruction"] = instructions
        self.created_at: str = created_at
        self.compiled: bool = False

    def compile(self) -> bool:
        self.compiled = all(instr.validate() for instr in self.instructions)
        return self.compiled

    def submit_batch(self) -> bool:
        if not self.compiled:
            self.compile()
        return all(instr.validate() for instr in self.instructions)
