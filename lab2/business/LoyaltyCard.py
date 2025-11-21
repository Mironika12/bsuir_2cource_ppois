from exceptions.exceptions import (
    NegativeAmountException,
    ValidationException,
)
from core.Customer import Customer

class LoyaltyCard:
    """
    Карта лояльности клиента.
    Хранит:
      - владельца
      - количество бонусных баллов
      - уровень (tier)
      - историю операций
    """

    def __init__(self, owner: Customer, points: int = 0):
        self._owner = owner               # объект Customer
        self._points = max(points, 0)     # нельзя иметь отрицательные
        self._tier = self._calculate_tier()
        self._history = []                # история операций с баллами

    def _calculate_tier(self) -> str:
        """Определение уровня клиента по количеству баллов."""
        if self._points >= 1000:
            return "gold"
        if self._points >= 500:
            return "silver"
        if self._points >= 200:
            return "bronze"
        return "standard"

    def _update_tier(self):
        self._tier = self._calculate_tier()

    def add_points(self, amount: int, reason: str = "purchase"):
        """Начислить баллы."""
        if amount <= 0:
            raise NegativeAmountException(amount)

        self._points += amount
        self._history.append(("add", amount, reason))
        self._update_tier()

    def redeem_points(self, amount: int) -> bool:
        """
        Списать баллы (например, в обмен на скидку).
        Возвращает True, если списание удалось.
        """

        if amount <= 0:
            raise NegativeAmountException(amount)

        if amount > self._points:
            raise ValidationException(
                f"Недостаточно баллов: нужно {amount}, доступно {self._points}"
            )

        self._points -= amount
        self._history.append(("redeem", amount))
        self._update_tier()
        return True

    def get_owner(self):
        return self._owner

    def get_points(self) -> int:
        return self._points

    def get_tier(self) -> str:
        return self._tier

    def get_history(self) -> list:
        return list(self._history)

    def get_summary(self) -> dict:
        """Описание карты для отображения."""
        return {
            "owner": self._owner.get_name() if self._owner else None,
            "points": self._points,
            "tier": self._tier,
            "history": self._history.copy(),
        }
