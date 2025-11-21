from pizzeria.core.Employee import Employee
from pizzeria.core.Customer import Customer
from pizzeria.core.Order import Order
from exceptions.exceptions import (
    OrderNotReadyException,
)

class Waiter(Employee):
    def take_order(self, customer: Customer):
        """
        Официант принимает заказ у клиента.
        """
        return (
            f"Официант {self.get_name()} принял заказ от клиента {customer.get_name()}."
        )

    def serve_order(self, order: Order):
        """
        Официант подаёт заказ, если он готов.
        """
        if order.get_status() != "ready":
            raise OrderNotReadyException(order.get_order_id())

        return (
            f"Официант {self.get_name()} подал заказ №{order.get_order_id()} клиенту."
        )
