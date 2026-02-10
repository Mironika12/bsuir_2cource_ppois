import pytest
from salary_system3.time.LeaveRequest import LeaveRequest
from salary_system3.time.OvertimePolicy import OvertimePolicy
from salary_system3.time.Schedule import Schedule
from salary_system3.time.TimeEntry import TimeEntry
from salary_system3.time.TimeSheet import TimeSheet

# ---------------------------
# LeaveRequest tests
# ---------------------------

class DummyEmployee:
    employee_id = "E123"

def test_leave_request_approve_and_reject():
    emp = DummyEmployee()
    leave = LeaveRequest("L1", emp, "vacation")
    
    leave.approve()
    assert leave.approved is True
    assert leave.rejected is False
    
    leave.reject()
    assert leave.approved is False
    assert leave.rejected is True

# ---------------------------
# OvertimePolicy tests
# ---------------------------

def test_compute_overtime_pay_and_eligibility():
    policy = OvertimePolicy("OT1", multiplier=1.5, threshold=8)
    
    # below threshold
    assert policy.compute_overtime_pay(6, 10) == 0.0
    assert policy.is_eligible(6) is False
    
    # exactly threshold
    assert policy.compute_overtime_pay(8, 20) == 0.0
    assert policy.is_eligible(8) is False
    
    # above threshold
    assert policy.compute_overtime_pay(10, 15) == (10-8)*15*1.5
    assert policy.is_eligible(10) is True

# ---------------------------
# Schedule tests
# ---------------------------

def test_schedule_next_shift_and_is_on_shift():
    sched = Schedule("S1", "E123", ["morning", "evening"])
    
    assert sched.next_shift() == "morning"
    assert sched.next_shift() == "evening"
    assert sched.next_shift() == "morning"  # wraps around
    assert sched.is_on_shift("morning") is True
    assert sched.is_on_shift("night") is False
    
    # empty shift_pattern
    empty_sched = Schedule("S2", "E124", [])
    assert empty_sched.next_shift() == ""

# ---------------------------
# TimeEntry tests
# ---------------------------

def test_time_entry_validate_and_is_overtime():
    entry = TimeEntry("TE1", "2025-12-01", 5)
    assert entry.validate() is True
    assert entry.is_overtime() is False
    
    entry2 = TimeEntry("TE2", "2025-12-01", 10)
    assert entry2.validate() is True
    assert entry2.is_overtime() is True
    
    # negative hours
    entry3 = TimeEntry("TE3", "2025-12-01", -1)
    assert entry3.validate() is False

# ---------------------------
# TimeSheet tests
# ---------------------------

class DummyOvertimePolicy:
    def apply(self, hours):
        # simple: if hours > 40, add 5 bonus hours
        return 5 if hours > 40 else 0

def test_timesheet_add_entry_and_total_hours():
    policy = DummyOvertimePolicy()
    ts = TimeSheet("TS1", "E123", [], policy)
    
    entry1 = TimeEntry("TE1", "2025-12-01", 8)
    entry2 = TimeEntry("TE2", "2025-12-02", 10)
    
    ts.add_entry(entry1)
    ts.add_entry(entry2)
    
    assert len(ts.entries) == 2
    # total hours 18, policy applies 0 bonus (less than 40)
    assert ts.total_hours() == 18
    
    # add more entries to exceed 40 hours
    ts.add_entry(TimeEntry("TE3", "2025-12-03", 30))
    # total = 48, policy adds 5
    assert ts.total_hours() == 53
