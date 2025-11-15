# pizza_system.py
# ======================
# Шаблон классов системы "Пиццерия"
# Минимум: 50 классов, 150 полей, 100 уникальных методов, 30 связей, 12 исключений

# -------------------
# Пользовательские исключения
# -------------------
class PizzaException(Exception): pass
class InvalidIngredientException(PizzaException): pass
class OutOfStockException(PizzaException): pass
class OrderNotFoundException(PizzaException): pass
class PaymentFailedException(PizzaException): pass
class DeliveryUnavailableException(PizzaException): pass
class UnauthorizedAccessException(PizzaException): pass
class InvalidCouponException(PizzaException): pass
class MenuItemNotFoundException(PizzaException): pass
class TableNotAvailableException(PizzaException): pass
class KitchenOverloadException(PizzaException): pass
class EmployeeNotFoundException(PizzaException): pass


# -------------------
# Основные сущности
# -------------------

class Pizza:
    def __init__(self, name: str, size: str, crust: str, price: float, ingredients: list):
        self.name = name
        self.size = size
        self.crust = crust
        self.price = price
        self.ingredients = ingredients  # Ассоциация с Ingredient

    def calculate_calories(self): ...
    def add_ingredient(self, ingredient): ...
    def remove_ingredient(self, ingredient): ...


class Ingredient:
    def __init__(self, name: str, quantity: int, unit: str, cost: float):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.cost = cost

    def decrease_stock(self, amount: int): ...
    def restock(self, amount: int): ...


class Order:
    def __init__(self, order_id: int, customer, pizzas: list, total_price: float, status: str):
        self.order_id = order_id
        self.customer = customer  # Ассоциация с Customer
        self.pizzas = pizzas      # Ассоциация с Pizza
        self.total_price = total_price
        self.status = status

    def calculate_total(self): ...
    def update_status(self, status: str): ...
    def apply_discount(self, coupon): ...


class Customer:
    def __init__(self, name: str, phone: str, email: str, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address  # Ассоциация с Address

    def place_order(self, order): ...
    def cancel_order(self, order_id: int): ...


class Address:
    def __init__(self, street: str, city: str, zip_code: str):
        self.street = street
        self.city = city
        self.zip_code = zip_code

    def format_address(self): ...


class Payment:
    def __init__(self, amount: float, method: str, status: str):
        self.amount = amount
        self.method = method
        self.status = status

    def process_payment(self): ...
    def refund(self): ...


class Delivery:
    def __init__(self, delivery_id: int, courier, order, address):
        self.delivery_id = delivery_id
        self.courier = courier    # Ассоциация с Courier
        self.order = order        # Ассоциация с Order
        self.address = address    # Ассоциация с Address

    def start_delivery(self): ...
    def mark_delivered(self): ...


class Courier:
    def __init__(self, name: str, vehicle: str, phone: str):
        self.name = name
        self.vehicle = vehicle
        self.phone = phone

    def accept_delivery(self, delivery): ...
    def complete_delivery(self, delivery_id: int): ...


class Employee:
    def __init__(self, name: str, role: str, salary: float):
        self.name = name
        self.role = role
        self.salary = salary

    def clock_in(self): ...
    def clock_out(self): ...


class Chef(Employee):
    def prepare_pizza(self, pizza): ...
    def check_ingredients(self): ...


class Manager(Employee):
    def approve_discount(self, coupon): ...
    def fire_employee(self, employee): ...


class Waiter(Employee):
    def take_order(self, customer): ...
    def serve_order(self, order): ...


class Inventory:
    def __init__(self):
        self.items = []  # Ассоциация с Ingredient

    def add_item(self, ingredient): ...
    def remove_item(self, name: str): ...
    def check_stock(self, name: str): ...


class Menu:
    def __init__(self):
        self.items = []  # Ассоциация с MenuItem

    def add_item(self, item): ...
    def remove_item(self, name: str): ...
    def find_item(self, name: str): ...


class MenuItem:
    def __init__(self, name: str, price: float, description: str):
        self.name = name
        self.price = price
        self.description = description

    def update_price(self, new_price: float): ...


class Coupon:
    def __init__(self, code: str, discount_percent: int, active: bool):
        self.code = code
        self.discount_percent = discount_percent
        self.active = active

    def validate(self): ...
    def deactivate(self): ...


class Table:
    def __init__(self, number: int, seats: int, reserved: bool):
        self.number = number
        self.seats = seats
        self.reserved = reserved

    def reserve(self): ...
    def free_table(self): ...


class Reservation:
    def __init__(self, customer, table, time: str):
        self.customer = customer  # Ассоциация с Customer
        self.table = table        # Ассоциация с Table
        self.time = time

    def confirm(self): ...
    def cancel(self): ...


# -------------------
# Вспомогательные классы
# -------------------

class Review:
    def __init__(self, customer, rating: int, comment: str):
        self.customer = customer
        self.rating = rating
        self.comment = comment

    def edit_comment(self, text: str): ...


class Feedback:
    def __init__(self, text: str, category: str):
        self.text = text
        self.category = category

    def analyze_sentiment(self): ...


class Notification:
    def __init__(self, message: str, recipient):
        self.message = message
        self.recipient = recipient

    def send(self): ...


class Report:
    def __init__(self, title: str, data: dict):
        self.title = title
        self.data = data

    def generate_pdf(self): ...


class Schedule:
    def __init__(self, employee, shifts: list):
        self.employee = employee
        self.shifts = shifts

    def add_shift(self, shift): ...


class Shift:
    def __init__(self, day: str, start: str, end: str):
        self.day = day
        self.start = start
        self.end = end

    def duration(self): ...


class LoyaltyCard:
    def __init__(self, customer, points: int):
        self.customer = customer
        self.points = points

    def add_points(self, amount: int): ...
    def redeem_points(self, amount: int): ...


class TaxCalculator:
    def __init__(self, rate: float):
        self.rate = rate

    def calculate_tax(self, amount: float): ...


class Kitchen:
    def __init__(self):
        self.active_orders = []

    def assign_order(self, order): ...
    def complete_order(self, order_id: int): ...


class Recipe:
    def __init__(self, name: str, ingredients: list, instructions: str):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def print_recipe(self): ...


class Supplier:
    def __init__(self, name: str, contact: str, products: list):
        self.name = name
        self.contact = contact
        self.products = products

    def place_order(self, ingredient, amount: int): ...


class SupplyOrder:
    def __init__(self, supplier, items: list, status: str):
        self.supplier = supplier
        self.items = items
        self.status = status

    def mark_received(self): ...


class Promotion:
    def __init__(self, name: str, description: str, active: bool):
        self.name = name
        self.description = description
        self.active = active

    def activate(self): ...
    def deactivate(self): ...


class Cart:
    def __init__(self, customer):
        self.customer = customer
        self.items = []  # Ассоциация с Pizza/MenuItem

    def add_item(self, item): ...
    def clear_cart(self): ...


class Event:
    def __init__(self, title: str, date: str, location: str):
        self.title = title
        self.date = date
        self.location = location

    def announce(self): ...


class Statistic:
    def __init__(self, name: str, value: float):
        self.name = name
        self.value = value

    def update_value(self, new_value: float): ...


class CleaningSchedule:
    def __init__(self, area: str, frequency: str):
        self.area = area
        self.frequency = frequency

    def mark_done(self): ...


class MaintenanceRequest:
    def __init__(self, equipment: str, description: str):
        self.equipment = equipment
        self.description = description

    def mark_fixed(self): ...


class ReviewManager:
    def __init__(self):
        self.reviews = []  # Ассоциация с Review

    def get_average_rating(self): ...


class DiscountPolicy:
    def __init__(self, threshold: float, discount: float):
        self.threshold = threshold
        self.discount = discount

    def apply(self, amount: float): ...


class TimeTracker:
    def __init__(self, employee):
        self.employee = employee
        self.hours_worked = 0

    def add_hours(self, hours: float): ...


class OnlineOrder(Order):
    def request_delivery(self): ...
    def track_order(self): ...


class InStoreOrder(Order):
    def assign_table(self, table): ...


class InventoryReport(Report):
    def summarize_stock(self): ...


class DailySalesReport(Report):
    def summarize_sales(self): ...


class OrderQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, order): ...
    def dequeue(self): ...


class PizzaBuilder:
    def __init__(self):
        self.ingredients = []

    def add_base(self, base): ...
    def add_topping(self, topping): ...
    def build(self): ...
