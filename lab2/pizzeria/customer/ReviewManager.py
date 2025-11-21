from pizzeria.customer.Review import Review

class ReviewManager:
    def __init__(self, reviews: list[Review]):
        self.reviews = reviews or []

    def add_review(self, review: Review):
        self.reviews.append(review)

    def get_average_rating(self):
        if not self.reviews:
            return 0.0
        return sum(r.get_rating() for r in self.reviews) / len(self.reviews)