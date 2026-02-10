# lab2/exceptions/exceptions.py

class PizzaException(Exception):
    """Базовое исключение системы пиццерии."""
    def __init__(self, message: str = "Ошибка в системе пиццерии"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


# Ингредиенты / склад
class IngredientException(PizzaException):
    """Базовое для ошибок, связанных с ингредиентами."""
    pass

class InvalidIngredientException(IngredientException):
    def __init__(self, ingredient_name: str):
        super().__init__(f"Некорректный ингредиент: {ingredient_name}")
        self.ingredient_name = ingredient_name

class OutOfStockException(IngredientException):
    def __init__(self, item: str, required: float, available: float):
        super().__init__(f"Недостаточно '{item}': нужно {required}, доступно {available}")
        self.item = item
        self.required = required
        self.available = available

class IngredientNotFoundException(IngredientException):
    def __init__(self, item: str):
        super().__init__(f"Ингредиент '{item}' не найден в инвентаре")
        self.item = item


# Заказы
class OrderException(PizzaException):
    pass

class OrderNotFoundException(OrderException):
    def __init__(self, order_id: int):
        super().__init__(f"Заказ ID={order_id} не найден")
        self.order_id = order_id

class OrderNotReadyException(OrderException):
    def __init__(self, order_id: int):
        super().__init__(f"Заказ ID={order_id} ещё не готов")
        self.order_id = order_id


# Платежи и поставки
class PaymentException(PizzaException):
    pass

class PaymentFailedException(PaymentException):
    def __init__(self, amount: float, method: str):
        super().__init__(f"Платёж не выполнен: {amount} через {method}")
        self.amount = amount
        self.method = method

class SupplierException(PizzaException):
    pass

class SupplierProductException(SupplierException):
    def __init__(self, product: str, supplier: str = None):
        msg = f"Поставщик не продаёт '{product}'"
        if supplier:
            msg += f" (поставщик: {supplier})"
        super().__init__(msg)
        self.product = product
        self.supplier = supplier

class NegativeAmountException(PizzaException):
    def __init__(self, amount):
        super().__init__(f"Недопустимое количество: {amount}")
        self.amount = amount


# Меню / купоны
class MenuException(PizzaException):
    pass

class MenuItemNotFoundException(MenuException):
    def __init__(self, item_name: str):
        super().__init__(f"Позиция меню '{item_name}' не найдена")
        self.item_name = item_name

class InvalidCouponException(PizzaException):
    def __init__(self, code: str):
        super().__init__(f"Купон '{code}' недействителен")
        self.code = code


# Персонал / доступ
class EmployeeException(PizzaException):
    pass

class EmployeeNotFoundException(EmployeeException):
    def __init__(self, employee_id: int):
        super().__init__(f"Сотрудник ID={employee_id} не найден")
        self.employee_id = employee_id

class SelfActionException(EmployeeException):
    def __init__(self, action: str):
        super().__init__(f"Нельзя выполнить операцию: {action}")
        self.action = action

class UnauthorizedAccessException(PizzaException):
    def __init__(self, user_role: str, required_role: str):
        super().__init__(f"Роль '{user_role}' не имеет доступа. Требуется: '{required_role}'")
        self.user_role = user_role
        self.required_role = required_role


# Кухня / перегрузка
class KitchenOverloadException(PizzaException):
    def __init__(self, current_orders: int, max_capacity: int):
        super().__init__(f"Кухня перегружена: {current_orders}/{max_capacity} заказов")
        self.current_orders = current_orders
        self.max_capacity = max_capacity


# Общие ошибки валидации
class ValidationException(PizzaException):
    pass

class NegativeHoursException(ValidationException):
    def __init__(self, hours):
        super().__init__(f"Нельзя добавить отрицательное число часов: {hours}")
        self.hours = hours

class InvalidOperationException(PizzaException):
    def __init__(self, message: str):
        super().__init__(message)

