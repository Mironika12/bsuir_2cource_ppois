import pytest
from datetime import datetime, timedelta
from salary_system3.taxes.EmployerContributions import EmployerContributions
from salary_system3.taxes.TaxAuthority import TaxAuthority
from salary_system3.taxes.TaxConfig import TaxConfig
from salary_system3.taxes.TaxFiling import TaxFiling
from salary_system3.taxes.WithholdingSchedule import WithholdingSchedule

# ---------------------------
# EmployerContributions tests
# ---------------------------

def test_calculate_and_allocate():
    contrib = EmployerContributions("C1", "social", 0.1)
    assert contrib.calculate(1000) == 100.0
    alloc = contrib.allocate("E123")
    assert alloc["employee_id"] == "E123"
    assert alloc["contribution"] == 0.1

# ---------------------------
# TaxAuthority tests
# ---------------------------

def test_get_rates_and_file_declaration():
    authority = TaxAuthority("TA1", "US", "contact@example.com")
    rates = authority.get_rates("2025-01")
    assert rates["standard"] == 0.2
    assert rates["reduced"] == 0.1
    assert authority.file_declaration() is True

# ---------------------------
# TaxConfig tests
# ---------------------------

def test_load_for_jurisdiction_and_validate():
    authority = TaxAuthority("TA2", "US", "contact@example.com")
    rules = {"standard": 0.2}
    config = TaxConfig("TC1", "2025-01-01", rules, authority)
    
    # correct jurisdiction
    loaded = config.load_for_jurisdiction("US")
    assert loaded == rules
    # wrong jurisdiction
    loaded2 = config.load_for_jurisdiction("CA")
    assert loaded2 == {}
    assert config.validate() is True

    empty_config = TaxConfig("TC2", "2025-01-01", {}, authority)
    assert empty_config.validate() is False

# ---------------------------
# TaxFiling tests
# ---------------------------

def test_prepare_and_submit():
    authority = TaxAuthority("TA3", "US", "contact@example.com")
    filing = TaxFiling("F1", "2025-01", "pending", authority)
    assert filing.prepare() is True
    assert filing.submit() is True
    assert filing.status == "submitted"

# ---------------------------
# WithholdingSchedule tests
# ---------------------------

def test_next_withholding_date_for_frequencies():
    schedule = WithholdingSchedule("WS1", "daily", {})
    next_day = schedule.next_withholding_date("2025-12-01")
    assert next_day == "2025-12-02"

    schedule.frequency = "weekly"
    next_week = schedule.next_withholding_date("2025-12-01")
    assert next_week == "2025-12-08"

    schedule.frequency = "monthly"
    next_month = schedule.next_withholding_date("2025-12-01")
    assert next_month == "2025-12-31"

    schedule.frequency = "unknown"
    same_day = schedule.next_withholding_date("2025-12-01")
    assert same_day == "2025-12-01"

def test_is_due_behavior():
    schedule = WithholdingSchedule("WS2", "daily", {})
    assert schedule.is_due("2025-12-01") is True
    schedule.mark_withheld("2025-12-01")
    # next due is 2025-12-02
    assert schedule.is_due("2025-12-01") is False
    assert schedule.is_due("2025-12-02") is True
    assert schedule.is_due("2025-12-03") is True

def test_calculate_withholding_amount_limits():
    rules = {"rate": 0.1, "min_amount": 50, "max_amount": 200}
    schedule = WithholdingSchedule("WS3", "monthly", rules)
    # normal calculation
    amount = schedule.calculate_withholding_amount(1000)
    assert amount == 100.0
    # below min_amount
    amount = schedule.calculate_withholding_amount(400)
    assert amount == 50
    # above max_amount
    amount = schedule.calculate_withholding_amount(3000)
    assert amount == 200

def test_mark_withheld_sets_last_withheld_date():
    schedule = WithholdingSchedule("WS4", "daily", {})
    schedule.mark_withheld("2025-12-01")
    assert schedule.last_withheld_date == "2025-12-01"
