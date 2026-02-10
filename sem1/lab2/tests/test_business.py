# =======================
# TESTS FOR lab2/business/*
# =======================

# ---------- test_coupon.py ----------
from pizzeria.business.Coupon import Coupon

def test_coupon_initialization():
    c = Coupon("ABC", 20, True)
    assert c.get_code() == "ABC"
    assert c.get_discount_percent() == 20
    assert c.is_active() is True

def test_coupon_validate_valid():
    assert Coupon("SALE", 50, True).validate() is True

def test_coupon_validate_invalid_percent():
    assert Coupon("BAD", 150, True).validate() is False

def test_coupon_validate_inactive():
    assert Coupon("OFF", 10, False).validate() is False

def test_coupon_deactivate():
    c = Coupon("XYZ", 10, True)
    c.deactivate()
    assert c.is_active() is False


# ---------- test_daily_sales_report.py ----------
from pizzeria.business.DailySalesReport import DailySalesReport

def test_summarize_sales():
    report = DailySalesReport(
        title="Daily",
        data={"orders": [1, 2, 3], "total_sales": 150.5}
    )
    summary = report.summarize_sales()

    assert "Orders processed: 3" in summary
    assert "Total sales: 150.50" in summary


# ---------- test_discount_policy.py ----------
from pizzeria.business.DiscountPolicy import DiscountPolicy

def test_apply_discount_above_threshold():
    dp = DiscountPolicy(threshold=100, discount=0.2)
    assert dp.apply(200) == 160

def test_apply_discount_below_threshold():
    dp = DiscountPolicy(threshold=100, discount=0.1)
    assert dp.apply(50) == 50

def test_apply_discount_equal_threshold():
    dp = DiscountPolicy(threshold=100, discount=0.1)
    assert dp.apply(100) == 90


# ---------- test_inventory_report.py ----------
from pizzeria.business.InventoryReport import InventoryReport

def test_summarize_stock():
    data = {"Cheese": 10, "Tomato": 5}
    report = InventoryReport("Inventory", data)
    out = report.summarize_stock()

    assert "Inventory Report:" in out
    assert "Cheese: 10" in out
    assert "Tomato: 5" in out


# ---------- test_promotion.py ----------
from pizzeria.business.Promotion import Promotion

def test_promotion_activation():
    p = Promotion("Weekend", "Sale", False)
    assert not p.is_active()

    p.activate()
    assert p.is_active()

    p.deactivate()
    assert not p.is_active()

def test_promotion_data():
    p = Promotion("Holiday", "Big discount", True)
    assert p.get_name() == "Holiday"
    assert p.get_description() == "Big discount"


# ---------- test_report.py ----------
from pizzeria.business.Report import Report

def test_report_initialization():
    r = Report("TestReport", {"a": 1, "b": 2})
    assert r.get_title() == "TestReport"
    assert r.get_data() == {"a": 1, "b": 2}

def test_report_generate_pdf():
    r = Report("Test", {"x": 10})
    pdf = r.generate_pdf()

    assert "=== Test ===" in pdf
    assert "x: 10" in pdf


# ---------- test_statistic.py ----------
from pizzeria.business.Statistic import Statistic

def test_statistic_initialization():
    s = Statistic("Orders", 100)
    assert s.get_name() == "Orders"
    assert s.get_value() == 100

def test_statistic_update_value():
    s = Statistic("Revenue", 1000)
    s.update_value(1500)
    assert s.get_value() == 1500
