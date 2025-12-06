import pytest
from unittest.mock import Mock

from salary_system3.payments.BankTransferAdapter import BankTransferAdapter
from salary_system3.payments.CashPaymentProcessor import CashPaymentProcessor
from salary_system3.payments.PaymentBatch import PaymentBatch
from salary_system3.payments.PaymentGatewayAdapter import PaymentGatewayAdapter
from salary_system3.payments.PaymentInstruction import PaymentInstruction


# ---------------------------------------
# Helper: Mock Payee
# ---------------------------------------

class FakePayee:
    def __init__(self, payee_id="P1", bank_account="ACC123", valid=True):
        self.payee_id = payee_id
        self.bank_account = bank_account
        self._valid = valid

    def validate_account(self):
        return self._valid


# ---------------------------------------
# PaymentInstruction Tests
# ---------------------------------------

def test_payment_instruction_validate_valid():
    payee = FakePayee(valid=True)
    instr = PaymentInstruction("I1", payee, 100)

    assert instr.validate() is True


def test_payment_instruction_validate_invalid_amount():
    payee = FakePayee(valid=True)
    instr = PaymentInstruction("I1", payee, -10)

    assert instr.validate() is False


def test_payment_instruction_validate_invalid_payee():
    payee = FakePayee(valid=False)
    instr = PaymentInstruction("I1", payee, 100)

    assert instr.validate() is False


def test_payment_instruction_to_bank_format():
    payee = FakePayee()
    instr = PaymentInstruction("I1", payee, 250.5)

    result = instr.to_bank_format()

    assert result == {
        "payee_id": "P1",
        "bank_account": "ACC123",
        "amount": 250.5
    }


# ---------------------------------------
# PaymentGatewayAdapter Tests (abstract)
# ---------------------------------------

# def test_payment_gateway_adapter_init():
#     adapter = BankTransferAdapter("A1", "MyBank", "https://api.bank")

#     assert adapter.adapter_id == "A1"
#     assert adapter.config == {}
#     assert adapter.supported_methods == ["bank_transfer"]
#     assert adapter.bank_name == "MyBank"
#     assert adapter.api_endpoint == "https://api.bank"


# ---------------------------------------
# BankTransferAdapter Tests
# ---------------------------------------

# def test_bank_transfer_submit_valid():
#     adapter = BankTransferAdapter("A1", "BankX", "/api")
#     payee = FakePayee(valid=True)
#     instr = PaymentInstruction("I1", payee, 100)

#     assert adapter.submit_payment(instr) is True


# def test_bank_transfer_submit_invalid():
#     adapter = BankTransferAdapter("A1", "BankX", "/api")
#     payee = FakePayee(valid=False)
#     instr = PaymentInstruction("I1", payee, 100)

#     assert adapter.submit_payment(instr) is False


# def test_bank_transfer_handle_callback():
#     adapter = BankTransferAdapter("A1", "BankX", "/api")

#     assert adapter.handle_callback("I1", "success") is True
#     assert adapter.handle_callback("I1", "failed") is True
#     assert adapter.handle_callback("I1", "unknown") is False


# ---------------------------------------
# CashPaymentProcessor Tests
# ---------------------------------------

def test_cash_payment_processor_initial_state():
    cp = CashPaymentProcessor("CP1", "LOC1", "PETTY-ACC")
    assert cp.processor_id == "CP1"
    assert cp.location_id == "LOC1"
    assert cp.petty_cash_account == "PETTY-ACC"
    assert cp.issued_cash == 0.0


def test_cash_payment_issue_cash():
    cp = CashPaymentProcessor("CP1", "LOC1", "PETTY-ACC")

    result = cp.issue_cash(150)

    assert result is True
    assert cp.issued_cash == 150


def test_cash_payment_reconcile_cash_excess():
    cp = CashPaymentProcessor("CP1", "LOC1", "PETTY-ACC")
    cp.issue_cash(200)

    discrepancy = cp.reconcile_cash(250)

    assert discrepancy == 50
    assert cp.issued_cash == 0.0


def test_cash_payment_reconcile_cash_shortage():
    cp = CashPaymentProcessor("CP1", "LOC1", "PETTY-ACC")
    cp.issue_cash(300)

    discrepancy = cp.reconcile_cash(250)

    assert discrepancy == -50
    assert cp.issued_cash == 0.0


# ---------------------------------------
# PaymentBatch Tests
# ---------------------------------------

def test_payment_batch_initial_state():
    payee = FakePayee()
    instr = PaymentInstruction("I1", payee, 100)

    pb = PaymentBatch("B1", [instr], "2025-01-01")

    assert pb.batch_id == "B1"
    assert pb.created_at == "2025-01-01"
    assert pb.instructions == [instr]
    assert pb.compiled is False


def test_payment_batch_compile_valid():
    payee = FakePayee(valid=True)
    instr1 = PaymentInstruction("I1", payee, 100)
    instr2 = PaymentInstruction("I2", payee, 200)

    pb = PaymentBatch("B1", [instr1, instr2], "2025")

    assert pb.compile() is True
    assert pb.compiled is True


def test_payment_batch_compile_invalid():
    payee_valid = FakePayee(valid=True)
    payee_invalid = FakePayee(valid=False)

    instr1 = PaymentInstruction("I1", payee_valid, 100)
    instr2 = PaymentInstruction("I2", payee_invalid, 200)

    pb = PaymentBatch("B1", [instr1, instr2], "2025")

    assert pb.compile() is False
    assert pb.compiled is False


def test_payment_batch_submit_batch_valid():
    payee = FakePayee(valid=True)
    instr = PaymentInstruction("I1", payee, 100)

    pb = PaymentBatch("B1", [instr], "2025")
    assert pb.submit_batch() is True


def test_payment_batch_submit_batch_invalid():
    payee = FakePayee(valid=False)
    instr = PaymentInstruction("I1", payee, 100)

    pb = PaymentBatch("B1", [instr], "2025")
    assert pb.submit_batch() is False


# ---------------------------------------
# Testing abstract class edges
# ---------------------------------------

# def test_payment_gateway_missing_methods():
#     class BadAdapter(PaymentGatewayAdapter):
#         def submit_payment(self, instruction):
#             return True
#         # check_status NOT IMPLEMENTED → should fail

#     ba = BadAdapter("X", {}, ["bank"])

#     with pytest.raises(TypeError):
#         # instantiating abstract class with unimplemented method
#         BadAdapter("X", {}, ["bank"])
