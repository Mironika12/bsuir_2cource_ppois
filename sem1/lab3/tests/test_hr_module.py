import pytest

from salary_system3.hr.BenefitEnrollment import BenefitEnrollment
from salary_system3.deductions.BenefitDeduction import BenefitDeduction
from salary_system3.hr.OnboardingChecklist import OnboardingChecklist
from salary_system3.hr.PerformanceReview import PerformanceReview
from salary_system3.hr.RecruitmentRecord import RecruitmentRecord
from salary_system3.hr.TerminationRecord import TerminationRecord


# ---------------------------
# BenefitEnrollment Tests
# ---------------------------

def test_benefit_enrollment_initial_state():
    be = BenefitEnrollment("E1", "EMP1", "PLAN1")
    assert be.enrollment_id == "E1"
    assert be.employee_id == "EMP1"
    assert be.plan_id == "PLAN1"
    assert be.active is False
    assert be.benefit_deduction is None


def test_benefit_enrollment_enroll():
    be = BenefitEnrollment("E1", "EMP1", "PLAN1")
    bd = BenefitDeduction("BD1", 2, "PLAN1")

    result = be.enroll(bd)

    assert result is True
    assert be.active is True
    assert be.benefit_deduction == bd


def test_benefit_enrollment_cancel():
    be = BenefitEnrollment("E1", "EMP1", "PLAN1")
    bd = BenefitDeduction("BD1", 2, "PLAN1")
    be.enroll(bd)

    result = be.cancel_enrollment()

    assert result is True
    assert be.active is False
    assert be.benefit_deduction is None


# ---------------------------
# OnboardingChecklist Tests
# ---------------------------

def test_onboarding_checklist_initialization():
    oc = OnboardingChecklist("C1", ["doc", "training"], "EMP1")
    assert oc.items == ["doc", "training"]
    assert oc.employee_id == "EMP1"
    assert oc.completed_items == []


def test_onboarding_checklist_mark_complete_success():
    oc = OnboardingChecklist("C1", ["doc", "training"], "EMP1")
    assert oc.mark_complete("doc") is True
    assert oc.completed_items == ["doc"]


def test_onboarding_checklist_mark_complete_twice():
    oc = OnboardingChecklist("C1", ["doc"], "EMP1")

    # First ok
    assert oc.mark_complete("doc") is True

    # Second time must fail
    assert oc.mark_complete("doc") is False
    assert oc.completed_items == ["doc"]


def test_onboarding_checklist_mark_complete_invalid_item():
    oc = OnboardingChecklist("C1", ["doc"], "EMP1")

    assert oc.mark_complete("not_exists") is False
    assert oc.completed_items == []


def test_onboarding_checklist_pending_items():
    oc = OnboardingChecklist("C1", ["doc", "training"], "EMP1")
    oc.mark_complete("doc")

    assert oc.pending_items() == ["training"]


# ---------------------------
# PerformanceReview Tests
# ---------------------------

def test_performance_review_initial_state():
    pr = PerformanceReview("R1", "EMP1", 4.5)
    assert pr.review_id == "R1"
    assert pr.employee_id == "EMP1"
    assert pr.score == 4.5
    assert pr.submitted is False


def test_performance_review_submit():
    pr = PerformanceReview("R1", "EMP1", 4.5)
    assert pr.submit() is True
    assert pr.submitted is True


def test_performance_review_summary():
    pr = PerformanceReview("R1", "EMP1", 4.5)
    pr.submit()

    summary = pr.get_summary()
    assert summary == {
        "review_id": "R1",
        "employee_id": "EMP1",
        "score": 4.5,
        "submitted": True
    }


# ---------------------------
# RecruitmentRecord Tests
# ---------------------------

def test_recruitment_record_initial_state():
    rr = RecruitmentRecord("REC1", "John Doe", "screening")
    assert rr.recruit_id == "REC1"
    assert rr.candidate_name == "John Doe"
    assert rr.status == "screening"
    assert rr.converted_employee_id is None


def test_recruitment_record_convert_to_employee():
    rr = RecruitmentRecord("REC1", "John Doe", "active")
    emp_id = rr.convert_to_employee("EMP777")

    assert emp_id == "EMP777"
    assert rr.converted_employee_id == "EMP777"
    assert rr.status == "converted"


def test_recruitment_record_archive():
    rr = RecruitmentRecord("REC1", "John Doe", "active")
    assert rr.archive() is True
    assert rr.status == "archived"


# ---------------------------
# TerminationRecord Tests
# ---------------------------

def test_termination_record_initial_state():
    tr = TerminationRecord("T1", "EMP1", "Misconduct")
    assert tr.termination_id == "T1"
    assert tr.employee_id == "EMP1"
    assert tr.reason == "Misconduct"
    assert tr.exit_processed is False
    assert tr.final_pay is None


def test_termination_record_process_exit():
    tr = TerminationRecord("T1", "EMP1", "Resigned")
    assert tr.process_exit() is True
    assert tr.exit_processed is True


def test_termination_record_calculate_final_pay():
    tr = TerminationRecord("T1", "EMP1", "Layoff")
    result = tr.calculate_final_pay(accrued_pay=3000, deductions=500)

    assert result == 2500
    assert tr.final_pay == 2500
