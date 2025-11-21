from pizzeria.core.Ingredient import Ingredient
from exceptions.exceptions import InvalidOperationException

class PizzaBuilder:
    def __init__(self, ingredients: list[Ingredient]):
        self.ingredients = ingredients or []

    def add_base(self, base: Ingredient):
        self.ingredients.append(base)
        return self

    def add_topping(self, topping: Ingredient):
        self.ingredients.append(topping)
        return self

    def build(self):
        if not self.ingredients:
            raise InvalidOperationException("Пицца должна иметь хотя бы тесто!")
        return "Пицца готова!"