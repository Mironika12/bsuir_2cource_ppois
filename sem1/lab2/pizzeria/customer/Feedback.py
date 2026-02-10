class Feedback:
    def __init__(self, text: str, category: str):
        self._text = text
        self._category = category

    def get_text(self) -> str:
        return self._text

    def get_category(self) -> str:
        return self._category

    def analyze_sentiment(self) -> str:
        """
        Простейший анализ тональности.
        Возвращает: "positive", "neutral", "negative"
        """
        text = self._text.lower()

        positive_keywords = ["good", "nice", "tasty", "love", "great"]
        negative_keywords = ["bad", "awful", "poor", "hate", "cold"]

        if any(word in text for word in positive_keywords):
            return "positive"
        if any(word in text for word in negative_keywords):
            return "negative"
        return "neutral"
