import pytest

from pizzeria.supply.Supplier import Supplier
from pizzeria.supply.SupplyOrder import SupplyOrder

from pizzeria.utils.CleaningSchedule import CleaningSchedule
from pizzeria.utils.PizzaBuilder import PizzaBuilder
from pizzeria.utils.Schedule import Schedule
from pizzeria.utils.TimeTracker import TimeTracker

from pizzeria.core.Ingredient import Ingredient
from pizzeria.core.Employee import Employee
from pizzeria.core.Pizza import Pizza

from exceptions.exceptions import (
    SupplierProductException,
    NegativeAmountException,
    InvalidOperationException,
    NegativeHoursException,
)


def test_supplier_basic_info():
    s = Supplier("BestFood", "123-456", [])
    assert s.get_name() == "BestFood"
    assert s.get_contact() == "123-456"


def test_supplier_place_order_success():
    i = Ingredient("Cheese", 10, "kg", 5)
    s = Supplier("FoodCo", "555", [i.get_name()])
    result = s.place_order(i, 3)
    assert result["supplier"] == "FoodCo"
    assert result["ingredient"] == "Cheese"
    assert result["amount"] == 3
    assert result["status"] == "ordered"


def test_supplier_place_order_invalid_product():
    i = Ingredient("Tomato", 5, "kg", 2)
    s = Supplier("FoodCo", "555", ["Cheese"])
    with pytest.raises(SupplierProductException):
        s.place_order(i, 2)


def test_supplier_place_order_negative_amount():
    i = Ingredient("Cheese", 5, "kg", 2)
    s = Supplier("FoodCo", "555", [i.get_name()])
    with pytest.raises(NegativeAmountException):
        s.place_order(i, -1)


def test_supply_order_getters():
    s = Supplier("Market", "123", [])
    items = [{Ingredient("Cheese", 10, "kg", 5): 3}]
    o = SupplyOrder(s, items)
    assert o.get_supplier() is s
    assert o.get_items() == items
    assert o.get_status() == "pending"


def test_supply_order_mark_received():
    s = Supplier("LogiCo", "321", [])
    o = SupplyOrder(s, [])
    msg = o.mark_received()
    assert o.get_status() == "received"
    assert "LogiCo" in msg


def test_cleaning_schedule_initial():
    c = CleaningSchedule("kitchen", "daily")
    assert c.get_area() == "kitchen"
    assert c.get_frequency() == "daily"
    assert c.get_last_done() is None


def test_cleaning_schedule_mark_done():
    c = CleaningSchedule("hall", "daily")
    msg = c.mark_done()
    assert c.get_last_done() == "completed"
    assert "hall" in msg


def test_pizza_builder_add_and_build():
    i1 = Ingredient("Base", 1, "pcs", 1)
    i2 = Ingredient("Cheese", 1, "pcs", 1)
    builder = PizzaBuilder([])
    pizza = builder.add_base(i1).add_topping(i2).build()
    assert pizza == "Пицца готова!"


def test_pizza_builder_empty_build():
    builder = PizzaBuilder([])
    with pytest.raises(InvalidOperationException):
        builder.build()


def test_schedule_add_shift():
    e = Employee(1, "Bob", "555", "cook", 1000)
    s = Schedule(e, ["morning"])
    s.add_shift("evening")
    assert "evening" in s.get_shifts()


def test_schedule_no_duplicate_shifts():
    e = Employee(2, "Ann", "777", "manager", 1500)
    s = Schedule(e, ["morning"])
    s.add_shift("morning")
    assert s.get_shifts() == ["morning"]


def test_time_tracker_add_hours():
    e = Employee(3, "Tim", "999", "waiter", 1200)
    t = TimeTracker(e)
    t.add_hours(5)
    assert t.hours_worked == 5


def test_time_tracker_negative_hours():
    e = Employee(4, "Sam", "111", "chef", 1300)
    t = TimeTracker(e)
    with pytest.raises(NegativeHoursException):
        t.add_hours(-2)
