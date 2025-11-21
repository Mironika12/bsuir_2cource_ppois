from Customer import Customer
from Pizza import Pizza

class Order:
    def __init__(self, order_id: int, customer: Customer, pizzas: list[Pizza], status: str):
        self._order_id = order_id
        self._customer = customer
        self._pizzas = pizzas
        self._status = status
        self._total_price = 0.0

    def calculate_total(self):
        """Подсчитать стоимость заказа"""
        self._total_price = sum(p.get_price() for p in self._pizzas)
        return self._total_price

    def update_status(self, new_status: str):
        """Обновить статус: создан / готовится / доставляется / завершён"""
        if isinstance(new_status, str):
            self._status = new_status

    def apply_discount(self, percent: float):
        """Применить скидку к итоговой сумме"""
        if percent > 0:
            discount = self._total_price * (percent / 100)
            self._total_price -= discount
            if self._total_price < 0:
                self._total_price = 0

    def get_order_id(self) -> int:
        return self._order_id

    def get_customer(self) -> Customer:
        return self._customer

    def get_pizzas(self) -> list[Pizza]:
        return self._pizzas

    def get_status(self) -> str:
        return self._status

    def get_total_price(self) -> float:
        return self._total_price
