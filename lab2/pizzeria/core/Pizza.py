from pizzeria.core.Ingredient import Ingredient

class Pizza:
    def __init__(self, name: str, size: str, crust: str, price: float, ingredients: list[Ingredient]):
        self._name = name
        self._size = size
        self._crust = crust
        self._price = price
        self._ingredients = ingredients

    def calculate_calories(self) -> float:
        """Простая имитация подсчёта калорий по количеству ингредиентов"""
        base = 200
        calories = base + len(self._ingredients) * 50
        return calories

    def add_ingredient(self, ingredient: Ingredient):
        """Добавить ингредиент в пиццу"""
        if ingredient:
            self._ingredients.append(ingredient)

    def remove_ingredient(self, ingredient_name: str):
        """Удалить ингредиент по имени"""
        self._ingredients = [
            ing for ing in self._ingredients 
            if ing.get_name() != ingredient_name
        ]

    def get_name(self) -> str:
        return self._name

    def get_size(self) -> str:
        return self._size

    def get_crust(self) -> str:
        return self._crust

    def get_price(self) -> float:
        return self._price

    def get_ingredients(self) -> list[Ingredient]:
        return self._ingredients
