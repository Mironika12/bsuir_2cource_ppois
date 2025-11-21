class MenuItem:
    def __init__(self, name: str, price: float, description: str):
        self._name = name
        self._price = price
        self._description = description

    def get_name(self) -> str:
        return self._name

    def get_price(self) -> float:
        return self._price

    def get_description(self) -> str:
        return self._description

    def update_price(self, new_price: float):
        """Обновить цену позиции меню"""
        if new_price > 0:
            self._price = new_price