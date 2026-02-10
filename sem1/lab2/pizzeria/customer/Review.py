from pizzeria.core.Customer import Customer

class Review:
    def __init__(self, customer: Customer, rating: int, comment: str):
        self._customer = customer
        self._rating = rating
        self._comment = comment

    def get_customer(self):
        return self._customer

    def get_rating(self) -> int:
        return self._rating

    def get_comment(self) -> str:
        return self._comment

    def edit_comment(self, text: str):
        """Изменить текст комментария"""
        if text and len(text.strip()) > 0:
            self._comment = text.strip()
