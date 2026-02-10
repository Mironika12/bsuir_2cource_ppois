from pizzeria.restaurant.MenuItem import MenuItem

class Menu:
    def __init__(self, items: list[MenuItem]):
        self._items = items or []

    def add_item(self, item):
        """Добавить пункт меню"""
        if item not in self._items:
            self._items.append(item)

    def remove_item(self, name: str):
        """Удалить пункт меню по имени"""
        for item in self._items:
            if item.get_name() == name:
                self._items.remove(item)
                return True
        return False

    def find_item(self, name: str):
        """Найти пункт меню по имени"""
        for item in self._items:
            if item.get_name() == name:
                return item
        return None
