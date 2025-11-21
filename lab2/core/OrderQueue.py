from core.Order import Order

class OrderQueue:
    def __init__(self, queue: list[Order]):
        self.queue = queue or []

    def enqueue(self, order):
        self.queue.append(order)

    def dequeue(self):
        if not self.queue:
            return None
        return self.queue.pop(0)