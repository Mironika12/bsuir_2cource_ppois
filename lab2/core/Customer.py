from Address import Address
from Order import Order

class Customer:
    def __init__(self, name: str, phone: str, email: str, address: Address):
        self._name = name
        self._phone = phone
        self._email = email
        self._address = address
        self._order_history = []

    def place_order(self, order: "Order"):
        """Добавить заказ в историю клиента"""
        if order:
            self._order_history.append(order)

    def cancel_order(self, order_id: int):
        """Отменить заказ по ID (удалить из истории)"""
        self._order_history = [
            order for order in self._order_history
            if order.get_order_id() != order_id
        ]

    def get_name(self) -> str:
        return self._name

    def get_phone(self) -> str:
        return self._phone

    def get_email(self) -> str:
        return self._email

    def get_address(self) -> Address:
        return self._address

    def get_order_history(self) -> list:
        return self._order_history
