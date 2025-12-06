from typing import Dict, Any, List


class ReconciliationEngine:
    def __init__(self, engine_id: str, rules: Dict[str, Any], tolerance: float):
        self.engine_id: str = engine_id
        self.rules: Dict[str, Any] = rules
        self.tolerance: float = tolerance
        self.payment_batch: Any = None
        self.discrepancies: List[Dict[str, Any]] = []

    def reconcile_accounts(self, accounts: List[Dict[str, Any]]) -> bool:
        self.discrepancies = []
        for account in accounts:
            expected = float(account.get("expected", 0.0))
            actual = float(account.get("actual", 0.0))
            diff = abs(expected - actual)
            if diff > self.tolerance:
                self.discrepancies.append(
                    {
                        "account_id": account.get("account_id"),
                        "expected": expected,
                        "actual": actual,
                        "difference": diff
                    }
                )
        return len(self.discrepancies) == 0

    def generate_discrepancy_report(self) -> Dict[str, Any]:
        return {
            "engine_id": self.engine_id,
            "total_discrepancies": len(self.discrepancies),
            "details": self.discrepancies
        }
