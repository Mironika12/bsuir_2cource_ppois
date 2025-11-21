from exceptions.exceptions import OutOfStockException

class CutlerySet:
    """
    Набор приборов для столов: вид, количество комплектов, состояние.
    """
    def __init__(self, set_id: str, pieces: int = 3, in_stock: int = 10):
        self._set_id = set_id
        self._pieces = pieces
        self._in_stock = in_stock

    def take_set(self) -> bool:
        """Взять один комплект (например, для выдачи)"""
        if self._in_stock <= 0:
            raise OutOfStockException(self._set_id, 1, 0)
        self._in_stock -= 1
        return True

    def return_set(self):
        self._in_stock += 1

    def get_stock(self) -> int:
        return self._in_stock
