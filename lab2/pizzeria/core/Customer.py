from pizzeria.core.Address import Address

class Customer:
    def __init__(self, name: str, phone: str, email: str, address: Address):
        self._name = name
        self._phone = phone
        self._email = email
        self._address = address

    def get_name(self) -> str:
        return self._name

    def get_phone(self) -> str:
        return self._phone

    def get_email(self) -> str:
        return self._email

    def get_address(self) -> Address:
        return self._address
