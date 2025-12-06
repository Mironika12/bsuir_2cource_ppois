import pytest

from salary_system3.deductions.BenefitDeduction import BenefitDeduction
from salary_system3.deductions.DeductionRule import DeductionRule
from salary_system3.deductions.Garnishment import Garnishment
from salary_system3.deductions.TaxDeduction import TaxDeduction
from salary_system3.deductions.VoluntaryDeduction import VoluntaryDeduction


# -------------------------------------------------------------
# BenefitDeduction Tests
# -------------------------------------------------------------

def test_benefit_deduction_deduct():
    b = BenefitDeduction("B1", 2, "P1")
    assert b.deduct(100) == 200


def test_benefit_deduction_reconcile():
    b = BenefitDeduction("B1", 2, "P1")
    # expected = paid_amount * share = 50 * 2 = 100 → reconcile = 50 - 100 = -50
    assert b.reconcile(50) == -50


# -------------------------------------------------------------
# DeductionRule Tests
# -------------------------------------------------------------

def test_deduction_rule_apply_negative():
    rule = DeductionRule("R1", "fixed", "high")
    assert rule.apply(-10) == -10


def test_deduction_rule_apply_fixed():
    rule = DeductionRule("R2", "fixed", "low")
    assert rule.apply(200) == 100
    assert rule.apply(50) == 0


def test_deduction_rule_apply_percent():
    rule = DeductionRule("R3", "percent", "low")
    assert rule.apply(100) == 90
    assert rule.apply(10) == 9


def test_deduction_rule_apply_unknown_type():
    rule = DeductionRule("R4", "other", "mid")
    assert rule.apply(200) == 200


def test_deduction_rule_is_applicable():
    rule = DeductionRule("R5", "fixed", "low")
    assert rule.is_applicable() is True


# -------------------------------------------------------------
# Garnishment Tests
# -------------------------------------------------------------

def test_garnishment_apply_garnishment_basic():
    g = Garnishment("G1", "C123", 50)
    assert g.apply_garnishment(200) == 150


def test_garnishment_apply_garnishment_to_zero():
    g = Garnishment("G1", "C123", 300)
    assert g.apply_garnishment(200) == 0


def test_garnishment_release():
    g = Garnishment("G1", "C123", 100)
    g.release()
    assert g.amount == 0


# -------------------------------------------------------------
# TaxDeduction Tests
# -------------------------------------------------------------

def test_tax_deduction_calculate_below_threshold():
    t = TaxDeduction(101, 0.2, 1000)
    assert t.calculate(800) == 0


def test_tax_deduction_calculate_above_threshold():
    t = TaxDeduction(101, 0.2, 1000)
    # (1500 - 1000) * 0.2 = 500 * 0.2 = 100
    assert t.calculate(1500) == 100


def test_tax_deduction_withhold():
    t = TaxDeduction(101, 0.1, 1000)
    # tax = (1200 - 1000) * 0.1 = 20 → withhold = 1200 - 20 = 1180
    assert t.withhold(1200) == 1180


def test_tax_deduction_withhold_below_threshold():
    t = TaxDeduction(101, 0.3, 1000)
    assert t.withhold(900) == 900


# -------------------------------------------------------------
# VoluntaryDeduction Tests
# -------------------------------------------------------------

def test_voluntary_deduction_start_stop():
    v = VoluntaryDeduction("VD1", False, 50)
    assert v.employee_consent is False

    v.start()
    assert v.employee_consent is True

    v.stop()
    assert v.employee_consent is False
