from pizzeria.core.Order import Order

class InStoreOrder(Order):
    def __init__(self, order_id, customer, pizzas, status):
        super().__init__(order_id, customer, pizzas, status)
        self._table = None

    def assign_table(self, table):
        self._table = table
        self._status = "table_assigned"
        return f"Assigned to table {table}"