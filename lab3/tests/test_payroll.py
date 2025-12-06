import sys
import types
import pytest

# Вставляем фиктивный модуль exceptions.exceptions, чтобы PayRun импортировал исключения
exceptions_module = types.ModuleType("exceptions.exceptions")
for name in [
    "ValidationException", "DuplicateRecordException", "EmployeeNotFoundException",
    "InsufficientFundsException", "PayrollProcessingException", "DataIntegrityException",
    "InvalidContractException", "UnsupportedCurrencyException", "UnauthorizedAccessException",
    "PaymentGatewayException", "TimesheetLockedException", "TaxFilingException"
]:
    setattr(exceptions_module, name, type(name, (Exception,), {}))
sys.modules["exceptions.exceptions"] = exceptions_module

from salary_system3.payroll.PayrollRecord import PayrollRecord
from salary_system3.payroll.PayRun import PayRun
from salary_system3.payroll.Payslip import Payslip
from salary_system3.payroll.RetroAdjustment import RetroAdjustment
from salary_system3.payroll.SalaryCalculator import SalaryCalculator

from salary_system3.compensation.BaseSalaryComponent import BaseSalaryComponent
from salary_system3.compensation.CompensationPackage import CompensationPackage
from salary_system3.deductions.DeductionRule import DeductionRule
from salary_system3.core.Employee import Employee
from salary_system3.payments.PaymentBatch import PaymentBatch
from salary_system3.payments.PaymentInstruction import PaymentInstruction

# helper fake payee to allow PaymentInstruction validation
class FakePayee:
    def __init__(self, payee_id="P1", bank_account="ACC", valid=True):
        self.payee_id = payee_id
        self.bank_account = bank_account
        self._valid = valid

    def validate_account(self):
        return self._valid

# ---------------------------
# PayrollRecord tests
# ---------------------------

def test_payroll_record_generate_slip_and_recalculate():
    emp = Employee(1, "John", "full-time")
    rec = PayrollRecord("R1", "E1", emp, 1000.0)
    slip = rec.generate_slip()
    assert slip == {"record_id": "R1", "employee_id": "E1", "net_pay": 1000.0}
    rec.recalculate(1200.0)
    assert rec.net_pay == 1200.0

# ---------------------------
# Payslip tests
# ---------------------------

def test_payslip_render_and_send():
    emp = Employee(2, "Jane", "part-time")
    rec = PayrollRecord("R2", "E2", emp, 500.0)
    payslip = Payslip("P1", {"base": 500}, "2025-01-01", rec)
    pdf = payslip.render_pdf()
    assert isinstance(pdf, bytes)
    assert b"Payslip P1 issued 2025-01-01" in pdf
    assert payslip.send_to_employee() is True

# ---------------------------
# RetroAdjustment tests
# ---------------------------

def test_retro_adjustment_apply_and_revert():
    emp = Employee(3, "Ann", "full-time")
    rec = PayrollRecord("R3", "E3", emp, 1000.0)
    adj = RetroAdjustment("A1", "correction", 200.0, rec)
    new_pay = adj.apply_to_record()
    assert new_pay == 1200.0
    assert adj.applied is True
    reverted = adj.revert()
    assert reverted == 1000.0
    assert adj.applied is False

def test_retro_adjustment_double_apply_and_revert_no_change():
    emp = Employee(4, "Bob", "full-time")
    rec = PayrollRecord("R4", "E4", emp, 800.0)
    adj = RetroAdjustment("A2", "bonus", 100.0, rec)
    first = adj.apply_to_record()
    assert first == 900.0
    second = adj.apply_to_record()
    assert second == 900.0
    rev = adj.revert()
    assert rev == 800.0
    rev_again = adj.revert()
    assert rev_again == 800.0

# ---------------------------
# SalaryCalculator tests
# ---------------------------

# def test_salary_calculator_basic_deductions_and_explain():
#     base = BaseSalaryComponent("B1", 2000.0, "USD")
#     comp_pkg = CompensationPackage(1, 10, [base])
#     # create deduction rules: fixed subtract returns max(0, amount-100), but calculator
#     # does total -= rule.apply(total). We'll compute expected accordingly.
#     fixed_rule = DeductionRule("R1", "fixed", "high")
#     percent_rule = DeductionRule("R2", "percent", "low")
#     calc = SalaryCalculator("SC1", [], {}, comp_pkg, [fixed_rule, percent_rule])
#     emp = Employee(10, "Worker", "full-time")
#     result = calc.calculate(emp, "2025-01")
#     # apply fixed_rule.apply(total): if total 2000 -> fixed returns 1900 (2000-100)
#     # then total -= 1900 -> total becomes 100
#     # next percent_rule.apply(100) -> returns 90 (100*0.9)
#     # total -= 90 => 10
#     assert pytest.approx(result, rel=1e-6) == 10.0
#     explanations = calc.explain()
#     assert isinstance(explanations, list)
#     assert "Calculated for employee" in explanations[-1]

# ---------------------------
# PayRun validate_payrun tests (various failure modes)
# ---------------------------

def make_valid_record(net_pay=1000.0):
    emp = Employee(20, "Valid", "full-time")
    return PayrollRecord("REC_OK", "EMP20", emp, net_pay)

def make_record_missing_employee_id():
    emp = Employee(21, "NoId", "full-time")
    return PayrollRecord("REC_NOEMP", None, emp, 1000.0)

def make_record_zero_pay():
    emp = Employee(22, "Zero", "full-time")
    return PayrollRecord("REC_ZERO", "EMP22", emp, 0.0)

def test_validate_payrun_no_records_raises():
    pr = PayRun("PR1", "2025-01-01", "2025-01-31", [], [])
    with pytest.raises(Exception) as exc:
        pr.validate_payrun()
    assert "Ошибка валидации PayRun" in str(exc.value)

def test_validate_payrun_duplicate_record_raises():
    rec = make_valid_record()
    pr = PayRun("PR_DUP", "2025-01-01", "2025-01-31", [rec], [])
    pr.processed_records.append("PR_DUP")
    with pytest.raises(Exception) as exc:
        pr.validate_payrun()
    assert "Ошибка валидации PayRun" in str(exc.value)

def test_validate_payrun_invalid_dates_raises():
    rec = make_valid_record()
    pr = PayRun("PR2", "2025-02-01", "2025-01-31", [rec], [])
    with pytest.raises(Exception) as exc:
        pr.validate_payrun()
    assert "Ошибка валидации PayRun" in str(exc.value)

def test_validate_payrun_missing_employee_raises():
    rec = make_record_missing_employee_id()
    pr = PayRun("PR3", "2025-01-01", "2025-01-31", [rec], [])
    with pytest.raises(Exception) as exc:
        pr.validate_payrun()
    assert "Ошибка валидации PayRun" in str(exc.value)

def test_validate_payrun_insufficient_funds_raises():
    rec = make_record_zero_pay()
    pr = PayRun("PR4", "2025-01-01", "2025-01-31", [rec], [])
    with pytest.raises(Exception) as exc:
        pr.validate_payrun()
    assert "Ошибка валидации PayRun" in str(exc.value)

# ---------------------------
# PayRun calculate_total_payout tests
# ---------------------------

def test_calculate_total_payout_normal():
    rec1 = PayrollRecord("R10", "E10", Employee(30, "A", "full"), 100.0)
    rec2 = PayrollRecord("R11", "E11", Employee(31, "B", "full"), 200.0)
    pr = PayRun("PR_OK", "2025-01-01", "2025-01-31", [rec1, rec2], [])
    total = pr.calculate_total_payout()
    assert total == 300.0
    assert pr.total_amount == 300.0

def test_calculate_total_payout_data_integrity_raises():
    class BadRecord:
        def __init__(self):
            self.record_id = "BAD1"
    pr = PayRun("PR_BAD", "2025-01-01", "2025-01-31", [BadRecord()], [])
    with pytest.raises(Exception) as exc:
        pr.calculate_total_payout()
    assert "Ошибка расчета выплат" in str(exc.value)

def test_calculate_total_payout_invalid_contract_raises():
    emp = Employee(40, "C", "full")
    # create a fake contract that is inactive
    class FakeContract:
        def is_active(self):
            return False
    emp.employment_contract = FakeContract()
    rec = PayrollRecord("R20", "E20", emp, 100.0)
    pr = PayRun("PR_CON", "2025-01-01", "2025-01-31", [rec], [])
    with pytest.raises(Exception) as exc:
        pr.calculate_total_payout()
    assert "Ошибка расчета выплат" in str(exc.value)

def test_calculate_total_payout_unsupported_currency_raises():
    rec = PayrollRecord("R_BIG", "E_BIG", Employee(50, "D", "full"), 2_000_000.0)
    pr = PayRun("PR_BIG", "2025-01-01", "2025-01-31", [rec], [])
    with pytest.raises(Exception) as exc:
        pr.calculate_total_payout()
    assert "Ошибка расчета выплат" in str(exc.value)

# ---------------------------
# PayRun execute tests (success and failure)
# ---------------------------

def make_payment_batch_with_valid_instruction():
    payee = FakePayee(valid=True)
    instr = PaymentInstruction("I_OK", payee, 100.0)
    batch = PaymentBatch("B_OK", [instr], "2025-01-01")
    return batch

def make_payment_batch_with_invalid_instruction():
    payee = FakePayee(valid=False)
    instr = PaymentInstruction("I_BAD", payee, 100.0)
    batch = PaymentBatch("B_BAD", [instr], "2025-01-01")
    return batch

def test_execute_success_sets_completed_and_processed_records():
    rec = make_valid_record(1000.0)
    batch = make_payment_batch_with_valid_instruction()
    pr = PayRun("PR_EXEC", "2025-01-01", "2025-01-31", [rec], [batch])
    result = pr.execute()
    assert result is True
    assert pr.status == "completed"
    assert "PR_EXEC" in pr.processed_records

def test_execute_payment_gateway_failure_raises_and_sets_failed_status():
    rec = make_valid_record(1000.0)
    batch = make_payment_batch_with_invalid_instruction()
    pr = PayRun("PR_FAIL", "2025-01-01", "2025-01-31", [rec], [batch])
    with pytest.raises(Exception) as exc:
        pr.execute()
    assert pr.status == "failed"
    assert "Ошибка выполнения PayRun" in str(exc.value)

def test_execute_timesheet_locked_raises_and_sets_failed_status():
    # To force timesheet locked, override _check_timesheets to return False by monkeypatching the instance method
    rec = make_valid_record(1000.0)
    batch = make_payment_batch_with_valid_instruction()
    pr = PayRun("PR_TS", "2025-01-01", "2025-01-31", [rec], [batch])
    pr._check_timesheets = lambda: False
    with pytest.raises(Exception):
        pr.execute()
    assert pr.status == "failed"

# ---------------------------
# PayRun rollback tests
# ---------------------------

def test_rollback_success_after_execute():
    rec = make_valid_record(1000.0)
    batch = make_payment_batch_with_valid_instruction()
    pr = PayRun("PR_ROLL", "2025-01-01", "2025-01-31", [rec], [batch])
    pr.execute()
    assert pr.status == "completed"
    # ensure total_amount below 100000 so no extra auth required
    pr.total_amount = 1000.0
    res = pr.rollback()
    assert res is True
    assert pr.status == "rolled_back"
    assert pr.total_amount == 0.0
    assert "PR_ROLL" not in pr.processed_records

def test_rollback_fails_if_not_completed():
    rec = make_valid_record(1000.0)
    batch = make_payment_batch_with_valid_instruction()
    pr = PayRun("PR_RFAIL", "2025-01-01", "2025-01-31", [rec], [batch])
    with pytest.raises(Exception):
        pr.rollback()

def test_rollback_requires_additional_auth_for_large_total():
    rec = make_valid_record(1000.0)
    batch = make_payment_batch_with_valid_instruction()
    pr = PayRun("PR_RAUTH", "2025-01-01", "2025-01-31", [rec], [batch])
    pr.execute()
    pr.total_amount = 200000.0
    with pytest.raises(Exception) as exc:
        pr.rollback()
    assert "Ошибка отмены PayRun" in str(exc.value)

# ---------------------------
# PayRun repr test
# ---------------------------

def test_payrun_repr_contains_fields():
    rec = make_valid_record(100.0)
    pr = PayRun("PR_REPR", "2025-01-01", "2025-01-31", [rec], [])
    r = repr(pr)
    assert "PayRun(id=PR_REPR" in r

# cleanup injected module
del sys.modules["exceptions.exceptions"]
