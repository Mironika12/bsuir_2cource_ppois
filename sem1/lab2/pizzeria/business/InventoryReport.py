from pizzeria.business.Report import Report

class InventoryReport(Report):
    def __init__(self, title, data):
        super().__init__(title, data)

    def summarize_stock(self):
        """
        Ожидается, что self.data = { 'ingredient': quantity, ... }
        """
        lines = ["Inventory Report:"]
        for ingredient, qty in self._data.items():
            lines.append(f" - {ingredient}: {qty} units")
        return "\n".join(lines)