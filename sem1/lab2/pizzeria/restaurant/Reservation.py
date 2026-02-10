from pizzeria.core.Customer import Customer
from pizzeria.restaurant.Table import Table

class Reservation:
    def __init__(self, customer: Customer, table: Table, time: str):
        self._customer = customer
        self._table = table
        self._time = time
        self._confirmed = False

    def get_customer(self):
        return self._customer

    def get_table(self):
        return self._table

    def get_time(self) -> str:
        return self._time

    def is_confirmed(self) -> bool:
        return self._confirmed

    def confirm(self):
        """Подтвердить бронь, если стол свободен"""
        if not self._table.is_reserved():
            self._table.reserve()
            self._confirmed = True
            return True
        return False

    def cancel(self):
        """Отменить бронь"""
        if self._confirmed:
            self._table.free_table()
            self._confirmed = False
            return True
        return False