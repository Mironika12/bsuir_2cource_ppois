# coupon.py
class Coupon:
    def __init__(self, code: str, discount_percent: int, active: bool):
        self._code = code
        self._discount_percent = discount_percent
        self._active = active

    def get_code(self) -> str:
        return self._code

    def get_discount_percent(self) -> int:
        return self._discount_percent

    def is_active(self) -> bool:
        """Проверка активности купона"""
        return self._active

    def validate(self) -> bool:
        """Проверить, можно ли использовать купон"""
        return self._active and 0 < self._discount_percent <= 100

    def deactivate(self):
        """Деактивировать купон"""
        self._active = False
