import pytest

from exceptions.exceptions import (
    PizzaException,
    IngredientException,
    InvalidIngredientException,
    OutOfStockException,
    IngredientNotFoundException,
    OrderException,
    OrderNotFoundException,
    OrderNotReadyException,
    PaymentException,
    PaymentFailedException,
    SupplierException,
    SupplierProductException,
    NegativeAmountException,
    MenuException,
    MenuItemNotFoundException,
    InvalidCouponException,
    EmployeeException,
    EmployeeNotFoundException,
    SelfActionException,
    UnauthorizedAccessException,
    KitchenOverloadException,
    ValidationException,
    NegativeHoursException,
    InvalidOperationException,
)


# ============================================================
#                    Base Exception
# ============================================================

def test_pizza_exception_message():
    ex = PizzaException("Test message")
    assert str(ex) == "Test message"


# ============================================================
#                    Ingredient Exceptions
# ============================================================

def test_invalid_ingredient_exception():
    with pytest.raises(InvalidIngredientException) as e:
        raise InvalidIngredientException("Cheese")

    assert "Некорректный ингредиент: Cheese" in str(e.value)
    assert e.value.ingredient_name == "Cheese"


def test_out_of_stock_exception():
    with pytest.raises(OutOfStockException) as e:
        raise OutOfStockException("Tomato", 5, 2)

    msg = "Недостаточно 'Tomato': нужно 5, доступно 2"
    assert msg in str(e.value)
    assert e.value.item == "Tomato"
    assert e.value.required == 5
    assert e.value.available == 2


def test_ingredient_not_found_exception():
    with pytest.raises(IngredientNotFoundException) as e:
        raise IngredientNotFoundException("Pepper")

    assert "ингредиент" in str(e.value).lower()
    assert e.value.item == "Pepper"


# ============================================================
#                     Order Exceptions
# ============================================================

def test_order_not_found_exception():
    with pytest.raises(OrderNotFoundException) as e:
        raise OrderNotFoundException(10)

    assert e.value.order_id == 10
    assert "Заказ ID=10 не найден" in str(e.value)


def test_order_not_ready_exception():
    with pytest.raises(OrderNotReadyException) as e:
        raise OrderNotReadyException(22)

    assert e.value.order_id == 22
    assert "ещё не готов" in str(e.value)


# ============================================================
#                     Payment Exceptions
# ============================================================

def test_payment_failed_exception():
    with pytest.raises(PaymentFailedException) as e:
        raise PaymentFailedException(100.0, "card")

    assert e.value.amount == 100.0
    assert e.value.method == "card"
    assert "Платёж не выполнен" in str(e.value)


def test_negative_amount_exception():
    with pytest.raises(NegativeAmountException) as e:
        raise NegativeAmountException(-5)

    assert e.value.amount == -5
    assert "Недопустимое количество: -5" in str(e.value)


# ============================================================
#                      Supplier Exceptions
# ============================================================

def test_supplier_product_exception_without_supplier():
    with pytest.raises(SupplierProductException) as e:
        raise SupplierProductException("Flour")

    assert e.value.product == "Flour"
    assert "Поставщик не продаёт 'Flour'" in str(e.value)


def test_supplier_product_exception_with_supplier():
    with pytest.raises(SupplierProductException) as e:
        raise SupplierProductException("Cheese", "BestFood")

    assert e.value.product == "Cheese"
    assert e.value.supplier == "BestFood"
    assert "(поставщик: BestFood)" in str(e.value)


# ============================================================
#                     Menu Exceptions
# ============================================================

def test_menu_item_not_found_exception():
    with pytest.raises(MenuItemNotFoundException) as e:
        raise MenuItemNotFoundException("Pasta")

    assert e.value.item_name == "Pasta"
    assert "Позиция меню 'Pasta' не найдена" in str(e.value)


def test_invalid_coupon_exception():
    with pytest.raises(InvalidCouponException) as e:
        raise InvalidCouponException("X123")

    assert e.value.code == "X123"
    assert "Купон 'X123' недействителен" in str(e.value)


# ============================================================
#                     Employee Exceptions
# ============================================================

def test_employee_not_found_exception():
    with pytest.raises(EmployeeNotFoundException) as e:
        raise EmployeeNotFoundException(99)

    assert e.value.employee_id == 99
    assert "Сотрудник ID=99 не найден" in str(e.value)


def test_self_action_exception():
    with pytest.raises(SelfActionException) as e:
        raise SelfActionException("уволить себя")

    assert e.value.action == "уволить себя"
    assert "Нельзя выполнить операцию" in str(e.value)


def test_unauthorized_access_exception():
    with pytest.raises(UnauthorizedAccessException) as e:
        raise UnauthorizedAccessException("waiter", "manager")

    assert e.value.user_role == "waiter"
    assert e.value.required_role == "manager"
    assert "Роль 'waiter'" in str(e.value)


# ============================================================
#                     Kitchen Exception
# ============================================================

def test_kitchen_overload_exception():
    with pytest.raises(KitchenOverloadException) as e:
        raise KitchenOverloadException(10, 5)

    assert e.value.current_orders == 10
    assert e.value.max_capacity == 5
    assert "Кухня перегружена" in str(e.value)


# ============================================================
#                Validation / Operation Exceptions
# ============================================================

def test_negative_hours_exception():
    with pytest.raises(NegativeHoursException) as e:
        raise NegativeHoursException(-3)

    assert e.value.hours == -3
    assert "отрицательное число часов" in str(e.value)


def test_invalid_operation_exception():
    with pytest.raises(InvalidOperationException) as e:
        raise InvalidOperationException("Нельзя отменить завершённый заказ")

    assert "Нельзя отменить завершённый заказ" in str(e.value)
