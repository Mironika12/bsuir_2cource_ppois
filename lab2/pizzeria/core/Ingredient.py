class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str, cost: float):
        self._name = name
        self._quantity = quantity
        self._unit = unit
        self._cost = cost

    def decrease_stock(self, amount: float):
        """Уменьшить количество ингредиента"""
        if amount < 0:
            return
        if amount > self._quantity:
            self._quantity = 0
        else:
            self._quantity -= amount

    def restock(self, amount: float):
        """Пополнить количество ингредиента"""
        if amount > 0:
            self._quantity += amount

    def get_name(self) -> str:
        return self._name

    def get_quantity(self) -> float:
        return self._quantity

    def get_unit(self) -> str:
        return self._unit

    def get_cost(self) -> float:
        return self._cost