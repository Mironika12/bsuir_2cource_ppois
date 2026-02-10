class PerformanceReview:
    def __init__(self, review_id: str, employee_id: str, score: float):
        self.review_id: str = review_id
        self.employee_id: str = employee_id
        self.score: float = score
        self.submitted: bool = False

    def submit(self) -> bool:
        self.submitted = True
        return self.submitted

    def get_summary(self) -> dict:
        return {
            "review_id": self.review_id,
            "employee_id": self.employee_id,
            "score": self.score,
            "submitted": self.submitted
        }
