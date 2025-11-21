from pizzeria.core.Order import Order
from pizzeria.core.Address import Address

class OnlineOrder(Order):
    def __init__(self, order_id, customer, pizzas, status, address: Address):
        super().__init__(order_id, customer, pizzas, status)
        self._address = address

    def request_delivery(self):
        self._status = "delivery_requested"
        return "Заказ оформлен."

    def track_order(self):
        return f"Текущий статус: {self._status}"