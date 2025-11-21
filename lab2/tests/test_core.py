# ============================
#       TESTS FOR core/*
# ============================

import pytest
from datetime import datetime, timedelta

# ---- imports of core classes ----
from pizzeria.core.Address import Address
from pizzeria.core.Chef import Chef
from pizzeria.core.Cleaner import Cleaner
from pizzeria.core.Courier import Courier
from pizzeria.core.Customer import Customer
from pizzeria.core.Delivery import Delivery
from pizzeria.core.Employee import Employee
from pizzeria.core.Ingredient import Ingredient
from pizzeria.core.InStoreOrder import InStoreOrder
from pizzeria.core.Inventory import Inventory
from pizzeria.core.Manager import Manager
from pizzeria.core.OnlineOrder import OnlineOrder
from pizzeria.core.Order import Order
from pizzeria.core.OrderQueue import OrderQueue
from pizzeria.core.Oven import Oven
from pizzeria.core.Payment import Payment
from pizzeria.core.Pizza import Pizza
from pizzeria.core.PizzaBox import PizzaBox
from pizzeria.core.Waiter import Waiter

from exceptions.exceptions import (
    KitchenOverloadException,
    OrderNotReadyException,
    IngredientNotFoundException,
    InvalidCouponException,
    SelfActionException,
    InvalidIngredientException,
)


# =====================================
#  Address
# =====================================
def test_address_format():
    addr = Address("Main", "NY", "12345")
    assert addr.format_address() == "Main, NY, 12345"


# =====================================
#  Employee
# =====================================
def test_employee_hours_and_payment():
    e = Employee(1, "Bob", "123", "chef", 1000)
    e.add_work_hours(10)
    assert e.get_work_hours() == 10
    assert e.calculate_monthly_payment() == 1000 + 20


# =====================================
#  Ingredient
# =====================================
def test_ingredient_stock_changes():
    ing = Ingredient("Cheese", 10, "g", 1.0)
    ing.decrease_stock(5)
    assert ing.get_quantity() == 5
    ing.restock(3)
    assert ing.get_quantity() == 8


# =====================================
#  Pizza
# =====================================
def test_pizza_calories_and_modification():
    ing1 = Ingredient("Cheese", 1, "g", 1)
    ing2 = Ingredient("Tom", 1, "g", 1)
    pizza = Pizza("Margarita", "L", "thin", 10, [ing1, ing2])

    assert pizza.calculate_calories() == 200 + 2 * 50

    pizza.remove_ingredient("Cheese")
    assert len(pizza.get_ingredients()) == 1

    pizza.add_ingredient(ing1)
    assert len(pizza.get_ingredients()) == 2


# =====================================
#  Chef
# =====================================
def test_chef_prepare_pizza_success():
    chef = Chef(1, "Mario", "123", "chef", 1000)
    pizza = Pizza("Test", "M", "thin", 10, [Ingredient("Cheese", 1, "g", 1)])
    assert "приготовил" in chef.prepare_pizza(pizza)

def test_chef_prepare_pizza_invalid():
    chef = Chef(1, "Mario", "123", "chef", 1000)
    pizza = Pizza("Bad", "M", "thin", 10,
                  [Ingredient("Cheese", 0, "g", 1)])
    with pytest.raises(Exception):
        chef.prepare_pizza(pizza)


# =====================================
#  Cleaner
# =====================================
def test_cleaner_zones_and_tasks():
    c = Cleaner(1, "Anna", "888", "cleaner", 500, ["hall"])
    c.assign_zone("kitchen")
    assert "kitchen" in c.get_assigned_zones()

    res = c.complete_cleaning("hall")
    assert "выполнена" in res
    assert c.get_completed_tasks() == 1


# =====================================
#  Courier
# =====================================
def test_courier_delivery_count():
    c = Courier(1, "John", "888", "bike", 700)
    c.complete_delivery()
    assert c.get_deliveries_completed() == 1


# =====================================
#  Customer
# =====================================
def test_customer_order_history():
    c = Customer("Bob", "123", "mail", Address("a","b","c"))
    assert c.get_name() == "Bob"
    assert c.get_email() == "mail"
    assert c.get_phone() == "123"
    


# =====================================
#  Order
# =====================================
def test_order_total_and_discount():
    p1 = Pizza("A", "M", "thin", 10, [])
    p2 = Pizza("B", "L", "thin", 20, [])
    order = Order(1, None, [p1, p2], "new")

    assert order.calculate_total() == 30
    order.apply_discount(10)
    assert order.get_total_price() == 27


# =====================================
#  OnlineOrder
# =====================================
def test_online_order_status():
    o = OnlineOrder(1, None, [], "new", Address("s","c","z"))
    o.request_delivery()
    assert o.get_status() == "delivery_requested"


# =====================================
#  InStoreOrder
# =====================================
def test_instore_assign_table():
    o = InStoreOrder(123, Customer("Bob", 121, "mail", Address("1","2","3")), [], "pending")
    text = o.assign_table(5)
    assert "5" in text
    assert o.get_status() == "table_assigned"


# =====================================
#  OrderQueue
# =====================================
def test_order_queue():
    q = OrderQueue([])
    order = Order(1, None, [], "new")
    q.enqueue(order)
    assert q.dequeue() is order
    assert q.dequeue() is None


# =====================================
#  Delivery
# =====================================
def test_delivery_estimated_time():
    courier = Courier(1, "Joe", "111", "scooter", 700)
    order = Order(1, None, [], "new")
    addr = Address("a","b","c")

    d = Delivery(10, order, courier, addr, "created")
    assert d.calculate_estimated_time() == 25

def test_delivery_status_updates():
    courier = Courier(1, "Joe", "111", "bike", 700)
    order = Order(1, None, [], "new")
    addr = Address("a","b","c")

    d = Delivery(2, order, courier, addr, "created")
    d.update_status("delivered")
    assert courier.get_deliveries_completed() == 1


# =====================================
#  Inventory
# =====================================
def test_inventory_add_and_remove():
    ing = Ingredient("Cheese", 5, "g", 1)
    inv = Inventory([ing])

    inv.add_item(Ingredient("Cheese", 3, "g", 1))
    assert ing.get_quantity() == 8

    with pytest.raises(IngredientNotFoundException):
        inv.remove_item("Bread")

    assert inv.remove_item("Cheese") == "Ингредиент 'Cheese' удалён."


def test_inventory_check_stock():
    inv = Inventory([Ingredient("Olives", 2, "g", 1)])
    assert inv.check_stock("Olives") == 2

    with pytest.raises(IngredientNotFoundException):
        inv.check_stock("Unknown")


# =====================================
#  Manager
# =====================================
class DummyCoupon:
    def __init__(self, active=True):
        self._active = active

    def is_active(self): return self._active
    def get_code(self): return "TEST"


def test_manager_approve_coupon():
    m = Manager(1, "Boss", "999", "manager", 2000)
    assert "одобрил" in m.approve_discount(DummyCoupon(True))

    with pytest.raises(InvalidCouponException):
        m.approve_discount(DummyCoupon(False))


def test_manager_fire_employee():
    m = Manager(1, "Boss", "999", "manager", 2000)
    e = Employee(2, "Worker", "321", "chef", 1000)

    assert "уволил" in m.fire_employee(e)

    with pytest.raises(SelfActionException):
        m.fire_employee(m)


# =====================================
# Waiter
# =====================================
def test_waiter_take_and_serve():
    w = Waiter(1, "Ann", "333", "waiter", 800)
    cust = Customer("John", "11", "mail", Address("s","c","z"))
    assert "принял заказ" in w.take_order(cust)

    order = Order(5, None, [], "ready")
    assert "подал заказ" in w.serve_order(order)

def test_waiter_serve_not_ready():
    w = Waiter(1, "Ann", "333", "waiter", 800)
    order = Order(5, None, [], "new")
    with pytest.raises(OrderNotReadyException):
        w.serve_order(order)


# =====================================
#  Oven
# =====================================
def test_oven_loading_and_status():
    oven = Oven("OV1", capacity=1)
    oven.load_pizza("Margherita", bake_minutes=0)
    ready = oven.unload_ready()
    assert "Margherita" in ready

def test_oven_overload():
    oven = Oven("OV2", capacity=1)
    oven.load_pizza("A")

    with pytest.raises(KitchenOverloadException):
        oven.load_pizza("B")


# =====================================
#  Payment
# =====================================
def test_payment_process_and_refund():
    p = Payment(1, 10, "card", "pending")
    assert p.process() is True
    assert p.get_status() == "paid"

    assert p.refund() is True
    assert p.get_status() == "refunded"

def test_payment_invalid_amount():
    p = Payment(2, -5, "card", "pending")
    assert p.process() is False
    assert p.get_status() == "failed"


# =====================================
#  PizzaBox
# =====================================
def test_pizzabox_seal_label():
    box = PizzaBox("L")
    box.seal()
    assert box.is_sealed() is True

    box.unseal()
    assert box.is_sealed() is False

    box.set_label("Holiday")
    info = box.get_info()
    assert info["label"] == "Holiday"
