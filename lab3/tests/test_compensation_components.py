import pytest

from salary_system3.compensation.AllowanceComponent import AllowanceComponent
from salary_system3.compensation.BaseSalaryComponent import BaseSalaryComponent
from salary_system3.compensation.BonusComponent import BonusComponent
from salary_system3.compensation.CompensationPackage import CompensationPackage
from salary_system3.compensation.StockCompensationComponent import StockCompensationComponent


# -------------------------------------------------------------
# AllowanceComponent Tests
# -------------------------------------------------------------

def test_allowance_is_taxable():
    a = AllowanceComponent("A1", "transport", 100)
    assert a.is_taxable() is True

    a2 = AllowanceComponent("A2", "rent", 200)
    assert a2.is_taxable() is False


def test_allowance_apply_cap_lowering():
    a = AllowanceComponent("A1", "meal", 500)
    new_amount = a.apply_cap(300)
    assert new_amount == 300
    assert a.amount == 300


def test_allowance_apply_cap_no_change():
    a = AllowanceComponent("A1", "meal", 100)
    new_amount = a.apply_cap(300)
    assert new_amount == 100
    assert a.amount == 100


# -------------------------------------------------------------
# BaseSalaryComponent Tests
# -------------------------------------------------------------

def test_base_salary_prorate():
    b = BaseSalaryComponent("B1", 1000, "USD")
    assert b.prorate(0.5) == 500
    assert b.prorate(1) == 1000


def test_base_salary_effective_from():
    b = BaseSalaryComponent("B1", 1500, "EUR")
    result = b.effective_from("2025-01-01")
    assert result == {"component_id": "B1", "effective_from": "2025-01-01"}


def test_base_salary_get_amount():
    b = BaseSalaryComponent("B1", 2500, "GBP")
    assert b.get_amount() == 2500


# -------------------------------------------------------------
# BonusComponent Tests
# -------------------------------------------------------------

def test_bonus_evaluate_key_exists():
    bonus = BonusComponent("BO1", "performance", "score")
    val = bonus.evaluate({"score": 10})
    assert val == 10


def test_bonus_evaluate_key_missing():
    bonus = BonusComponent("BO2", "performance", "rating")
    val = bonus.evaluate({"score": 10})
    assert val == 0


def test_bonus_schedule_payout():
    bonus = BonusComponent("BO1", "spot", "criteria")
    result = bonus.schedule_payout("2025-02-01")
    assert result == {"component_id": "BO1", "payout_date": "2025-02-01"}


# -------------------------------------------------------------
# CompensationPackage Tests
# -------------------------------------------------------------

def test_compensation_package_total_sum():
    c1 = BaseSalaryComponent("B1", 1000, "USD")
    c2 = BaseSalaryComponent("B2", 2000, "USD")
    package = CompensationPackage(1, 100, [c1, c2])

    assert package.calculate_total() == 3000


def test_compensation_package_empty_components():
    package = CompensationPackage(1, 200, None)
    assert package.calculate_total() == 0.0


def test_compensation_package_repr():
    package = CompensationPackage(5, 555)
    assert repr(package) == "CompensationPackage(package_id=5, employee_id=555)"


def test_compensation_package_ignores_components_without_get_amount():
    class Dummy:
        pass  # No get_amount()

    package = CompensationPackage(1, 1, [Dummy()])
    assert package.calculate_total() == 0.0


# -------------------------------------------------------------
# StockCompensationComponent Tests
# -------------------------------------------------------------

def test_stock_vest_normal():
    sc = StockCompensationComponent("S1", "monthly", 100)
    vested = sc.vest(30)
    assert vested == 30
    assert sc.vested_quantity == 30


def test_stock_vest_over_limit():
    sc = StockCompensationComponent("S1", "monthly", 100)
    sc.vested_quantity = 90
    vested = sc.vest(50)  # Only 10 left
    assert vested == 100
    assert sc.vested_quantity == 100


def test_stock_vest_negative():
    sc = StockCompensationComponent("S1", "monthly", 100)
    result = sc.vest(-10)
    assert result is None
    assert sc.vested_quantity == 0


def test_stock_forfeit_normal():
    sc = StockCompensationComponent("S1", "annual", 100)
    sc.vested_quantity = 20  # 80 available
    new_q = sc.forfeit(30)
    assert new_q == 70  # 100 - 30 = 70
    assert sc.quantity == 70


def test_stock_forfeit_over_limit():
    sc = StockCompensationComponent("S1", "annual", 100)
    sc.vested_quantity = 50  # 50 available
    new_q = sc.forfeit(80)   # only 50 allowed
    assert new_q == 50       # 100 - 50 = 50
    assert sc.quantity == 50


def test_stock_forfeit_negative():
    sc = StockCompensationComponent("S1", "annual", 100)
    result = sc.forfeit(-5)
    assert result is None
    assert sc.quantity == 100
