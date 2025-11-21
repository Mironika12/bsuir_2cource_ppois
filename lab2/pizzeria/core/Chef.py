from pizzeria.core.Employee import Employee
from pizzeria.core.Pizza import Pizza
from exceptions.exceptions import InvalidIngredientException

class Chef(Employee):
    def prepare_pizza(self, pizza: Pizza):
        """
        Повар готовит пиццу.
        Проверяет наличие ингредиентов и возвращает результат.
        """
        missing = []

        for ingredient in pizza.get_ingredients():
            if ingredient.get_quantity() <= 0:
                missing.append(ingredient.get_name())

        if missing:
            raise InvalidIngredientException(", ".join([ing.get_name() for ing in missing]))

        return f"Повар {self.get_name()} приготовил пиццу '{pizza.get_name()}'."

    def check_ingredients(self):
        """
        Имитация проверки ингредиентов поваром.
        """
        return f"Повар {self.get_name()} проверяет остатки ингредиентов на кухне."
