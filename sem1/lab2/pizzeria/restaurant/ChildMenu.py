from pizzeria.restaurant.Menu import Menu

class ChildMenu(Menu):
    def __init__(self, items, colour: str, with_coloring_book: bool = False):
        super().__init__(items)
        self._colour = colour
        self._with_coloring_book = with_coloring_book

    def ask_for_coloring_book(self):
        if self._with_coloring_book == False:
            self._with_coloring_book = True
    
    def get_colour(self) -> str:
        return self._colour
    
    def with_coloring_book(self) -> bool:
        return self._with_coloring_book