from core.Customer import Customer
from core.Employee import Employee

class Notification:
    def __init__(self, message: str, recipient: Customer | Employee):
        self._message = message
        self._recipient = recipient
        self._sent = False

    def get_message(self) -> str:
        return self._message

    def get_recipient(self):
        return self._recipient

    def is_sent(self) -> bool:
        return self._sent

    def send(self) -> bool:
        """
        Простая имитация отправки.
        """
        if not self._sent:
            self._sent = True
            return True
        return False
