from Courier import Courier
from Order import Order
from Address import Address

class Delivery:
    def __init__(self, delivery_id: int, order: 'Order', courier: 'Courier', address: 'Address', status: str):
        self._delivery_id = delivery_id
        self._order = order
        self._courier = courier
        self._address = address
        self._status = status
        self._estimated_time = None

    def calculate_estimated_time(self):
        """Простая оценка времени доставки"""
        if self._courier.get_vehicle_type() == "bike":
            self._estimated_time = 40
        elif self._courier.get_vehicle_type() == "scooter":
            self._estimated_time = 25
        else:
            self._estimated_time = 15
        return self._estimated_time

    def update_status(self, new_status: str):
        """Обновить статус доставки"""
        self._status = new_status
        if new_status == "delivered":
            self._courier.complete_delivery()

    def get_delivery_id(self) -> int:
        return self._delivery_id

    def get_order(self) -> 'Order':
        return self._order

    def get_courier(self) -> 'Courier':
        return self._courier

    def get_address(self) -> 'Address':
        return self._address

    def get_status(self) -> str:
        return self._status

    def get_estimated_time(self):
        return self._estimated_time