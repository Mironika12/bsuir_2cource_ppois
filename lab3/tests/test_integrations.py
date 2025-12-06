import pytest

from salary_system3.integrations.AuditLogger import AuditLogger
from salary_system3.integrations.ConfigService import ConfigService
from salary_system3.integrations.NotificationService import NotificationService
from salary_system3.integrations.PayrollFileImporter import PayrollFileImporter
from salary_system3.integrations.Repository import Repository


# ---------------------------
# AuditLogger Tests
# ---------------------------

def test_audit_logger_initial_state():
    al = AuditLogger("L1", "file", "INFO")
    assert al.logger_id == "L1"
    assert al.destination == "file"
    assert al.level == "INFO"
    assert al.logs == []


def test_audit_logger_log():
    al = AuditLogger("L1", "file", "INFO")

    result = al.log("CREATE", {"id": 1})

    assert result is True
    assert len(al.logs) == 1
    assert al.logs[0]["action"] == "CREATE"
    assert al.logs[0]["payroll_record"] == {"id": 1}


def test_audit_logger_query_logs_no_filter():
    al = AuditLogger("L1", "file", "INFO")
    al.logs = [
        {"action": "A", "level": "INFO"},
        {"action": "B", "level": "WARN"},
    ]

    result = al.query_logs()
    assert len(result) == 2
    assert result[0]["action"] == "A"
    assert result[1]["action"] == "B"


def test_audit_logger_query_logs_with_filter():
    al = AuditLogger("L1", "file", "INFO")
    al.logs = [
        {"action": "A", "level": "INFO"},
        {"action": "B", "level": "WARN"},
        {"action": "C", "level": "INFO"},
    ]

    result = al.query_logs("INFO")

    assert len(result) == 2
    assert {r["action"] for r in result} == {"A", "C"}


# ---------------------------
# ConfigService Tests
# ---------------------------

def test_config_service_initial_state():
    cs = ConfigService("C1", {"timeout": 30}, 1)
    assert cs.config_id == "C1"
    assert cs.values == {"timeout": 30}
    assert cs.version == 1


def test_config_service_get_existing():
    cs = ConfigService("C1", {"timeout": 30}, 1)
    assert cs.get("timeout") == 30


def test_config_service_get_missing():
    cs = ConfigService("C1", {"timeout": 30}, 1)
    assert cs.get("missing") is None


def test_config_service_set():
    cs = ConfigService("C1", {"timeout": 30}, 1)

    cs.set("timeout", 60)

    assert cs.values["timeout"] == 60
    assert cs.version == 2


# ---------------------------
# NotificationService Tests
# ---------------------------

def test_notification_service_initial_state():
    ns = NotificationService("N1", ["email"], {"welcome": "Hello!"})
    assert ns.service_id == "N1"
    assert ns.channels == ["email"]
    assert ns.templates == {"welcome": "Hello!"}
    assert ns.sent_notifications == []


def test_notification_service_notify():
    ns = NotificationService("N1", ["email"], {})

    result = ns.notify("user@example.com", "Your payslip", {"id": 1})

    assert result is True
    assert len(ns.sent_notifications) == 1
    rec = ns.sent_notifications[0]
    assert rec["recipient"] == "user@example.com"
    assert rec["message"] == "Your payslip"
    assert rec["payslip"] == {"id": 1}


def test_notification_service_schedule():
    ns = NotificationService("N1", ["email"], {})

    result = ns.schedule("user@example.com", "Reminder", "2025-01-01 10:00", None)

    assert result is True
    assert len(ns.sent_notifications) == 1
    rec = ns.sent_notifications[0]
    assert rec["recipient"] == "user@example.com"
    assert rec["message"] == "Reminder"
    assert rec["send_time"] == "2025-01-01 10:00"
    assert rec["payslip"] is None


# ---------------------------
# PayrollFileImporter Tests
# ---------------------------

def test_payroll_file_importer_initial_state():
    pfi = PayrollFileImporter("IMP1", "json", {"id": "employee_id"})
    assert pfi.import_id == "IMP1"
    assert pfi.source_type == "json"
    assert pfi.mapping == {"id": "employee_id"}
    assert pfi.records == []


def test_payroll_file_importer_parse_file():
    pfi = PayrollFileImporter("IMP1", "json", {"id": "employee_id", "pay": "salary"})

    file_content = [
        {"id": "E1", "pay": 1000},
        {"id": "E2", "pay": 1500},
    ]

    records = pfi.parse_file(file_content)

    assert len(records) == 2
    assert records[0] == {"employee_id": "E1", "salary": 1000}
    assert records[1] == {"employee_id": "E2", "salary": 1500}
    assert pfi.records == records


def test_payroll_file_importer_validate_records_valid():
    pfi = PayrollFileImporter("IMP1", "json", {"id": "employee_id"})
    pfi.records = [{"employee_id": "E1"}, {"employee_id": "E2"}]

    assert pfi.validate_records() is True


def test_payroll_file_importer_validate_records_invalid_missing_key():
    pfi = PayrollFileImporter("IMP1", "json", {"id": "employee_id"})
    pfi.records = [{"id": "E1"}]  # missing mapped key

    assert pfi.validate_records() is False


def test_payroll_file_importer_validate_records_invalid_none():
    pfi = PayrollFileImporter("IMP1", "json", {"id": "employee_id"})
    pfi.records = [{"employee_id": None}]  # invalid

    assert pfi.validate_records() is False


# ---------------------------
# Repository Tests
# ---------------------------

class DummyEntity:
    def __init__(self, id=None, employee_id=None):
        self.id = id
        self.employee_id = employee_id


def test_repository_initial_state():
    repo = Repository("R1", {}, None)
    assert repo.repo_id == "R1"
    assert repo.data_source == {}
    assert repo.cache == {}


def test_repository_save_by_id():
    repo = Repository("R1", {}, None)
    ent = DummyEntity(id="E1")

    result = repo.save(ent)

    assert result is True
    assert repo.data_source["E1"] is ent
    assert repo.cache["E1"] is ent


def test_repository_save_by_employee_id():
    repo = Repository("R1", {}, None)
    ent = DummyEntity(id=None, employee_id="EMP100")

    result = repo.save(ent)

    assert result is True
    assert repo.data_source["EMP100"] is ent
    assert repo.cache["EMP100"] is ent


def test_repository_save_fail_no_id():
    repo = Repository("R1", {}, None)
    ent = DummyEntity(id=None, employee_id=None)

    result = repo.save(ent)

    assert result is False
    assert repo.data_source == {}
    assert repo.cache == {}


def test_repository_find_by_id_from_cache():
    repo = Repository("R1", {}, None)
    ent = DummyEntity(id="E1")
    repo.cache["E1"] = ent

    result = repo.find_by_id("E1")

    assert result is ent


def test_repository_find_by_id_loads_to_cache():
    repo = Repository("R1", {"E1": DummyEntity(id="E1")}, None)

    result = repo.find_by_id("E1")

    assert result is repo.data_source["E1"]
    assert repo.cache["E1"] == repo.data_source["E1"]


def test_repository_find_by_id_missing():
    repo = Repository("R1", {}, None)
    result = repo.find_by_id("UNKNOWN")

    assert result is None
