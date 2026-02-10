import pytest

from salary_system3.core.Employee import Employee
from salary_system3.core.EmploymentContract import EmploymentContract
from salary_system3.core.OrganizationUnit import OrganizationUnit
from salary_system3.core.Payee import Payee
from salary_system3.core.Position import Position
from salary_system3.compensation.CompensationPackage import CompensationPackage
from salary_system3.compensation.BaseSalaryComponent import BaseSalaryComponent


# -------------------------------------------------------------
# Position Tests
# -------------------------------------------------------------

def test_position_get_salary_range():
    pos = Position(1, "Engineer", 5, (50000, 70000))
    assert pos.get_salary_range() == (50000, 70000)


def test_position_get_salary_range_none():
    pos = Position(1, "Engineer", 5, None)
    assert pos.get_salary_range() is None


def test_position_is_exempt():
    pos = Position(1, "Manager", 7, exempt=True)
    assert pos.is_exempt() is True

    pos2 = Position(2, "Intern", 1, exempt=False)
    assert pos2.is_exempt() is False


def test_position_repr():
    pos = Position(10, "Lead", 9)
    assert repr(pos) == "Position(id=10, title='Lead', grade=9)"


# -------------------------------------------------------------
# EmploymentContract Tests
# -------------------------------------------------------------

def test_employment_contract_is_active():
    contract = EmploymentContract(100, 10, {"term": "1y"})
    assert contract.is_active() is True


def test_employment_contract_terminate():
    contract = EmploymentContract(100, 10, {})
    contract.terminate()
    assert contract.is_active() is False


def test_employment_contract_repr():
    contract = EmploymentContract(50, 5, {})
    assert repr(contract) == "EmploymentContract(contract_id=50, employee_id=5, active=True)"
    contract.terminate()
    assert repr(contract) == "EmploymentContract(contract_id=50, employee_id=5, active=False)"


# -------------------------------------------------------------
# OrganizationUnit Tests
# -------------------------------------------------------------

def test_org_unit_add_member():
    unit = OrganizationUnit(1, "Finance")
    unit.add_member(10)
    assert unit.members == [10]

    # duplicate add ignored
    unit.add_member(10)
    assert unit.members == [10]


def test_org_unit_remove_member():
    unit = OrganizationUnit(1, "Finance")
    unit.add_member(10)
    unit.remove_member(10)
    assert unit.members == []

    # removing missing member does nothing
    unit.remove_member(99)
    assert unit.members == []


def test_org_unit_repr():
    unit = OrganizationUnit(1, "HR", 50)
    assert repr(unit) == "OrganizationUnit(id=1, name='HR', manager_id=50)"


# -------------------------------------------------------------
# Payee Tests
# -------------------------------------------------------------

def test_payee_validate_account_valid():
    p = Payee(1, "ACC123", "John Doe")
    assert p.validate_account() is True


def test_payee_validate_account_invalid():
    p = Payee(1, "", "John Doe")
    assert p.validate_account() is False

    p2 = Payee(2, None, "Jane Doe")
    assert p2.validate_account() is False


def test_payee_get_routing_info():
    p = Payee(1, "ACC1", "Legal Name")
    assert p.get_routing_info() == {"payee_id": 1, "bank_account": "ACC1"}


def test_payee_repr():
    p = Payee(3, "ACC2", "Corp LTD")
    assert repr(p) == "Payee(payee_id=3, legal_name='Corp LTD')"


# -------------------------------------------------------------
# Employee Tests
# -------------------------------------------------------------

def test_employee_get_profile_full():
    pos = Position(1, "Engineer", 5)
    unit = OrganizationUnit(2, "IT")
    contract = EmploymentContract(3, 99, {})
    comp = CompensationPackage(10, 99, [BaseSalaryComponent("B1", 1000, "USD")])

    emp = Employee(
        employee_id=99,
        full_name="John Smith",
        employment_type="full-time",
        position=pos,
        organization_unit=unit,
        employment_contract=contract,
        compensation_package=comp,
        contact_info={"email": "js@example.com"}
    )

    profile = emp.get_profile()

    assert profile["id"] == 99
    assert profile["full_name"] == "John Smith"
    assert profile["employment_type"] == "full-time"
    assert profile["contact_info"] == {"email": "js@example.com"}
    assert profile["position"] == repr(pos)
    assert profile["organization_unit"] == repr(unit)
    assert profile["contract"] == repr(contract)
    assert profile["compensation_package"] == repr(comp)


def test_employee_get_profile_partial_none_associations():
    emp = Employee(
        employee_id=1,
        full_name="No Assoc",
        employment_type="part-time"
    )

    profile = emp.get_profile()

    assert profile["position"] is None
    assert profile["organization_unit"] is None
    assert profile["contract"] is None
    assert profile["compensation_package"] is None


def test_employee_update_contact_info_valid():
    emp = Employee(1, "Test User", "full-time")
    emp.update_contact_info({"phone": "123"})
    assert emp.contact_info == {"phone": "123"}

    # merge updates
    emp.update_contact_info({"email": "test@mail.com"})
    assert emp.contact_info == {"phone": "123", "email": "test@mail.com"}


def test_employee_update_contact_info_invalid():
    emp = Employee(1, "Test User", "full-time")

    with pytest.raises(ValueError):
        emp.update_contact_info(["not", "a", "dict"])


def test_employee_repr():
    emp = Employee(1, "Alice", "contract")
    assert repr(emp) == "Employee(id=1, full_name='Alice', employment_type='contract')"
