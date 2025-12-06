import pytest
from datetime import datetime, timedelta

from salary_system3.reporting.ExportService import ExportService
from salary_system3.reporting.GLMapper import GLMapper
from salary_system3.reporting.PayrollAnalytics import PayrollAnalytics
from salary_system3.reporting.ReconciliationEngine import ReconciliationEngine
from salary_system3.reporting.ReportGenerator import ReportGenerator

# ---------------------------
# ExportService tests
# ---------------------------

def test_export_to_format_dict_json_text_and_invalid():
    service = ExportService("E1", ["dict", "json", "text"], datetime.now())
    report = {"a": 1, "b": 2}
    
    assert service.export_to_format(report, "dict") == report
    assert service.export_to_format(report, "json") == report
    text_output = service.export_to_format(report, "text")
    assert "a: 1" in text_output
    assert "b: 2" in text_output
    with pytest.raises(ValueError):
        service.export_to_format(report, "xml")

def test_schedule_export_adds_task():
    service = ExportService("E2", ["json"], datetime.now())
    schedule_time = datetime.now() + timedelta(days=1)
    dummy_generator = lambda: {"data": 123}
    service.schedule_export(dummy_generator, schedule_time)
    assert len(service.scheduled_tasks) == 1
    task = service.scheduled_tasks[0]
    assert task["report_generator"] == dummy_generator
    assert task["schedule_time"] == schedule_time

# ---------------------------
# GLMapper tests
# ---------------------------

def test_map_transaction_with_multiplier_and_target():
    rules = {
        "amount": {"target": "mapped_amount", "multiplier": 2},
        "description": {"target": "desc"}
    }
    mapper = GLMapper("M1", "GL100", rules)
    transaction = {"amount": 100, "description": "sale", "other": "ignore"}
    mapped = mapper.map_transaction(transaction)
    assert mapped["mapped_amount"] == 200
    assert mapped["desc"] == "sale"
    assert mapped["gl_account"] == "GL100"
    assert "other" not in mapped

def test_validate_mapping_true_and_false_cases():
    mapper = GLMapper("M2", "GL101", {"a": {"target": "b"}})
    assert mapper.validate_mapping() is True
    # invalid rules type
    mapper.rules = ["not a dict"]
    assert mapper.validate_mapping() is False
    # invalid key type
    mapper.rules = {123: {"target": "b"}}
    assert mapper.validate_mapping() is False
    # invalid target
    mapper.rules = {"a": {"target": 100}}
    assert mapper.validate_mapping() is False

# ---------------------------
# PayrollAnalytics tests
# ---------------------------

def test_compute_kpi_calculates_avg_total_employee_count():
    analytics = PayrollAnalytics("A1", ["avg_net_pay", "total_payroll", "employee_count"], {})
    records = [{"net_pay": 100}, {"net_pay": 200}, {"net_pay": 300}]
    result = analytics.compute_kpi(records)
    assert result["avg_net_pay"] == 200
    assert result["total_payroll"] == 600
    assert result["employee_count"] == 3
    # cached_results updated
    assert analytics.cached_results == result

def test_trend_analysis_up_down_flat_cases():
    analytics = PayrollAnalytics("A2", ["avg_net_pay"], {"2025-01": [100, 200]})
    res_up = analytics.trend_analysis("2025-01")
    assert res_up["direction"] == "up"
    analytics.cached_results["2025-02"] = [200, 100]
    res_down = analytics.trend_analysis("2025-02")
    assert res_down["direction"] == "down"
    analytics.cached_results["2025-03"] = [150]
    res_flat = analytics.trend_analysis("2025-03")
    assert res_flat["direction"] == "flat"
    res_nonexist = analytics.trend_analysis("missing")
    assert res_nonexist["direction"] == "flat"

# ---------------------------
# ReconciliationEngine tests
# ---------------------------

def test_reconcile_accounts_discrepancy_detection():
    engine = ReconciliationEngine("RE1", {}, tolerance=5.0)
    accounts = [
        {"account_id": "A1", "expected": 100.0, "actual": 102.0},  # within tolerance
        {"account_id": "A2", "expected": 200.0, "actual": 210.0}   # exceeds tolerance
    ]
    success = engine.reconcile_accounts(accounts)
    assert success is False
    assert len(engine.discrepancies) == 1
    report = engine.generate_discrepancy_report()
    assert report["total_discrepancies"] == 1
    assert report["engine_id"] == "RE1"

def test_reconcile_accounts_no_discrepancy():
    engine = ReconciliationEngine("RE2", {}, tolerance=10.0)
    accounts = [
        {"account_id": "A1", "expected": 100, "actual": 105},
        {"account_id": "A2", "expected": 200, "actual": 195}
    ]
    success = engine.reconcile_accounts(accounts)
    assert success is True
    report = engine.generate_discrepancy_report()
    assert report["total_discrepancies"] == 0

# ---------------------------
# ReportGenerator tests
# ---------------------------

def test_generate_and_export_with_gl_mapper():
    generator = ReportGenerator("R1", "typeA", {"transaction": {"amount": 100}})
    gl_mapper = GLMapper("M1", "GL100", {"amount": {"target": "mapped_amount"}})
    generator.gl_mapper = gl_mapper
    report = generator.generate()
    assert "mapped_gl" in report
    assert report["mapped_gl"]["mapped_amount"] == 100
    # export formats
    d = generator.export("dict")
    j = generator.export("json")
    t = generator.export("text")
    assert isinstance(d, dict)
    assert isinstance(j, dict)
    assert isinstance(t, str)
    # invalid export format
    with pytest.raises(ValueError):
        generator.export("xml")

def test_generate_without_gl_mapper():
    generator = ReportGenerator("R2", "typeB", {"other": 123})
    report = generator.generate()
    assert "mapped_gl" not in report
    exported = generator.export("dict")
    assert exported == report
