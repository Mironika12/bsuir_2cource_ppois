from pizzeria.business.Report import Report

class DailySalesReport(Report):
    def __init__(self, title, data):
        super().__init__(title, data)

    def summarize_sales(self):
        """
        Ожидается, что self.data = { 'orders': [...], 'total_sales': float }
        """
        total_orders = len(self._data.get("orders", []))
        total_sales = self._data.get("total_sales", 0)

        return (
            f"Daily Sales Report:\n"
            f" - Orders processed: {total_orders}\n"
            f" - Total sales: {total_sales:.2f}"
        )