class DiscountPolicy:
    def __init__(self, threshold: float, discount: float):
        """
        threshold — сумма, с которой начинается скидка
        discount — процент скидки (0.0–1.0)
        """
        self.threshold = threshold
        self.discount = discount

    def apply(self, amount: float):
        if amount >= self.threshold:
            return amount * (1 - self.discount)
        return amount