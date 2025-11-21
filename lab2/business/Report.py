# report.py
class Report:
    def __init__(self, title: str, data: dict):
        self._title = title
        self._data = data

    def get_title(self) -> str:
        return self._title

    def get_data(self) -> dict:
        return self._data

    def generate_pdf(self) -> str:
        """
        Имитация генерации PDF: возвращает строку-отчёт.
        (Файлы создавать нельзя — лабораторная ограничена)
        """
        content = f"=== {self._title} ===\n"
        for key, value in self._data.items():
            content += f"{key}: {value}\n"
        return content
