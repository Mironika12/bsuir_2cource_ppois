from pizzeria.core.Ingredient import Ingredient
from exceptions.exceptions import (
    IngredientNotFoundException,
)

class Inventory:
    def __init__(self, items: list[Ingredient]):
        self.items = items

    def add_item(self, ingredient: Ingredient):
        """
        Добавить ингредиент в инвентарь.
        Если ингредиент уже есть — увеличивает количество.
        """
        for item in self.items:
            if item.get_name() == ingredient.get_name():
                item.restock(ingredient.get_quantity())
                return f"Количество ингредиента '{item.get_name()}' увеличено."

        self.items.append(ingredient)
        return f"Ингредиент '{ingredient.get_name()}' добавлен."

    def remove_item(self, name: str):
        """
        Удалить ингредиент полностью из списка.
        """
        for item in self.items:
            if item.get_name() == name:
                self.items.remove(item)
                return f"Ингредиент '{name}' удалён."
        raise IngredientNotFoundException(name)

    def check_stock(self, name: str):
        """
        Проверить количество ингредиента.
        Возвращает int или вызывает ошибку.
        """
        for item in self.items:
            if item.get_name() == name:
                return item.get_quantity()
        raise IngredientNotFoundException(name)
