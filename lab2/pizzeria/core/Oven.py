from datetime import datetime, timedelta

class Oven:
    """
    Описание печи — для истории приготовления и допустимой загрузки.
    """
    def __init__(self, oven_id: str, capacity: int = 4):
        self._oven_id = oven_id
        self._capacity = capacity
        self._loaded = 0
        self._running_tasks = []

    def load_pizza(self, pizza_name: str, bake_minutes: int = 10):
        if self._loaded >= self._capacity:
            from exceptions.exceptions import KitchenOverloadException
            raise KitchenOverloadException(self._loaded + 1, self._capacity)
        ready_time = datetime.now() + timedelta(minutes=bake_minutes)
        self._running_tasks.append((pizza_name, ready_time))
        self._loaded += 1
        return ready_time

    def unload_ready(self):
        now = datetime.now()
        ready = [p for p in self._running_tasks if p[1] <= now]
        self._running_tasks = [p for p in self._running_tasks if p[1] > now]
        self._loaded = len(self._running_tasks)
        return [p[0] for p in ready]

    def get_status(self):
        return {
            "oven_id": self._oven_id,
            "capacity": self._capacity,
            "loaded": self._loaded,
            "tasks": [(p, t.isoformat()) for p, t in self._running_tasks]
        }
