from typing import Dict, Any, List


class PayrollAnalytics:
    def __init__(self, analytics_id: str, metrics: List[str], cached_results: Dict[str, Any]):
        self.analytics_id: str = analytics_id
        self.metrics: List[str] = metrics
        self.cached_results: Dict[str, Any] = cached_results

    def compute_kpi(self, payroll_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        total_net_pay: float = 0.0
        employee_count: int = 0

        for record in payroll_records:
            if "net_pay" in record:
                total_net_pay += float(record["net_pay"])
            employee_count += 1

        if "avg_net_pay" in self.metrics:
            results["avg_net_pay"] = total_net_pay / employee_count if employee_count > 0 else 0.0

        if "total_payroll" in self.metrics:
            results["total_payroll"] = total_net_pay

        if "employee_count" in self.metrics:
            results["employee_count"] = employee_count

        self.cached_results.update(results)
        return results

    def trend_analysis(self, period: Any) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if period in self.cached_results and isinstance(self.cached_results[period], list):
            values: List[float] = self.cached_results[period]
            if len(values) >= 2:
                trend = values[-1] - values[-2]
                direction = "up" if trend > 0 else "down" if trend < 0 else "flat"
                result = {"trend": trend, "direction": direction}
            else:
                result = {"trend": 0.0, "direction": "flat"}
        else:
            result = {"trend": 0.0, "direction": "flat"}
        return result
