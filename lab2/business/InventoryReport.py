from business.Report import Report

class InventoryReport(Report):
    def summarize_stock(self):
        """
        Ожидается, что self.data = { 'ingredient': quantity, ... }
        """
        lines = ["Inventory Report:"]
        for ingredient, qty in self.data.items():
            lines.append(f" - {ingredient}: {qty} units")
        return "\n".join(lines)