from core.Ingredient import Ingredient
from exceptions.exceptions import (
    SupplierProductException,
    NegativeAmountException,
)

class Supplier:
    def __init__(self, name: str, contact: str, products: list[Ingredient]):
        self._name = name
        self._contact = contact
        self._products = products

    def get_name(self) -> str:
        return self._name

    def get_contact(self) -> str:
        return self._contact

    def get_products(self):
        return self._products

    def place_order(self, ingredient: Ingredient, amount: int) -> dict:
        """
        Имитирует размещение заказа у поставщика.
        Возвращает словарь с подтверждением заказа.
        """
        if ingredient.get_name() not in self._products:
            raise SupplierProductException(ingredient.get_name(), self._name)

        if amount <= 0:
            raise NegativeAmountException(amount)

        return {
            "supplier": self._name,
            "ingredient": ingredient.get_name(),
            "amount": amount,
            "status": "ordered"
        }
