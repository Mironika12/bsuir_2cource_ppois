from Employee import Employee
from Pizza import Pizza
from exceptions.exceptions import InvalidIngredientException

class Chef(Employee):
    def prepare_pizza(self, pizza: Pizza):
        """
        Повар готовит пиццу.
        Проверяет наличие ингредиентов и возвращает результат.
        """
        missing = []

        for ingredient in pizza.ingredients:
            if ingredient.quantity <= 0:
                missing.append(ingredient.name)

        if missing:
            raise InvalidIngredientException(", ".join([ing.name for ing in missing]))

        return f"Повар {self.get_name()} приготовил пиццу '{pizza.name}'."

    def check_ingredients(self):
        """
        Имитация проверки ингредиентов поваром.
        """
        return f"Повар {self.get_name()} проверяет остатки ингредиентов на кухне."
