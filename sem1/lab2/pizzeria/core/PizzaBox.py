class PizzaBox:
    """
    Упаковка для пиццы: размер, материал, стикер (событие/акция).
    """
    def __init__(self, size: str, material: str = "cardboard", printed_label: str | None = None):
        self._size = size
        self._material = material
        self._printed_label = printed_label
        self._sealed = False

    def seal(self):
        self._sealed = True

    def unseal(self):
        self._sealed = False

    def is_sealed(self) -> bool:
        return self._sealed

    def set_label(self, label: str):
        self._printed_label = label

    def get_info(self) -> dict:
        return {
            "size": self._size,
            "material": self._material,
            "label": self._printed_label,
            "sealed": self._sealed,
        }
