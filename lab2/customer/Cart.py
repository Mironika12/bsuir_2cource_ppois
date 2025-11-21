from core.Customer import Customer
from restaurant.MenuItem import MenuItem
class Cart:
    def __init__(self, customer: Customer, items: list[MenuItem]):
        self._customer = customer
        self._items = items or []

    def get_customer(self):
        return self._customer

    def get_items(self) -> list:
        return self._items

    def add_item(self, item: MenuItem):
        """Добавить позицию в корзину."""
        self._items.append(item)

    def clear_cart(self):
        """Очистить корзину полностью."""
        self._items.clear()
