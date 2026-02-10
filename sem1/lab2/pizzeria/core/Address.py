class Address:
    def __init__(self, street: str, city: str, zip_code: str):
        self._street = street
        self._city = city
        self._zip_code = zip_code

    def format_address(self) -> str:
        """Вернуть адрес одной строкой"""
        return f"{self._street}, {self._city}, {self._zip_code}"

    def get_street(self) -> str:
        return self._street

    def get_city(self) -> str:
        return self._city

    def get_zip_code(self) -> str:
        return self._zip_code
