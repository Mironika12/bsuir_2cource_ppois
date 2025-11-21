from Supplier import Supplier
from core.Ingredient import Ingredient

class SupplyOrder:
    def __init__(self, supplier: Supplier, items: list[dict[Ingredient, int]], status: str = "pending"):
        self._supplier = supplier
        self._items = items
        self._status = status

    def get_supplier(self):
        return self._supplier

    def get_items(self):
        return self._items

    def get_status(self) -> str:
        return self._status

    def mark_received(self):
        """Помечает заказ как полученный."""
        self._status = "received"
        return f"Поставка от {self._supplier.get_name()} получена"
