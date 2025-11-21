class ToySet:
    """
    Небольшой игровой набор для детей (временно выдается вместе с заказом).
    """
    def __init__(self, toy_id: str, description: str, in_stock: int = 5):
        self._toy_id = toy_id
        self._description = description
        self._in_stock = in_stock

    def checkout(self):
        if self._in_stock <= 0:
            from exceptions.exceptions import OutOfStockException
            raise OutOfStockException(self._toy_id, 1, 0)
        self._in_stock -= 1
        return True

    def return_toy(self):
        self._in_stock += 1

    def get_stock(self) -> int:
        return self._in_stock
