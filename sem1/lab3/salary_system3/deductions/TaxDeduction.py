class TaxDeduction:
    def __init__(self, tax_code: int, rate: float, threshold: float):
        self.tax_code = tax_code
        self.rate = rate
        self.threshold = threshold

    def calculate(self, amount):
        if amount <= self.threshold:
            return 0
        return (amount - self.threshold) * self.rate

    def withhold(self, amount):
        tax = self.calculate(amount)
        return max(0, amount - tax)
