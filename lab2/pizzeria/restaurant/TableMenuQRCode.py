class TableMenuQRCode:
    """
    QR-код на столе, который направляет пользователя на меню / опции заказа.
    Хранит короткий код (символическое представление).
    """
    def __init__(self, table_number: int, code: str):
        self._table_number = table_number
        self._code = code
        self._active = True

    def deactivate(self):
        self._active = False

    def activate(self):
        self._active = True

    def is_active(self) -> bool:
        return self._active

    def get_code(self) -> str:
        return self._code

    def get_table(self) -> int:
        return self._table_number
