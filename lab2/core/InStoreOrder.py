from core.Order import Order

class InStoreOrder(Order):
    def __init__(self, items=None):
        super().__init__(items)
        self.table = None

    def assign_table(self, table):
        self.table = table
        self.status = "table_assigned"
        return f"Assigned to table {table}"