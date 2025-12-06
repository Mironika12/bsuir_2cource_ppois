from typing import Dict, Any


class GLMapper:
    def __init__(self, mapping_id: str, gl_account: str, rules: Dict[str, Any]):
        self.mapping_id: str = mapping_id
        self.gl_account: str = gl_account
        self.rules: Dict[str, Any] = rules
        self.payroll_record: Any = None

    def map_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        mapped: Dict[str, Any] = {}
        for source_key, rule in self.rules.items():
            if source_key in transaction:
                value = transaction[source_key]
                if isinstance(rule, dict) and "multiplier" in rule:
                    value = value * rule["multiplier"]
                mapped_key = rule["target"] if isinstance(rule, dict) and "target" in rule else source_key
                mapped[mapped_key] = value
        mapped["gl_account"] = self.gl_account
        return mapped

    def validate_mapping(self) -> bool:
        if not isinstance(self.rules, dict):
            return False
        for source_key, rule in self.rules.items():
            if not isinstance(source_key, str):
                return False
            if isinstance(rule, dict):
                if "target" not in rule or not isinstance(rule["target"], str):
                    return False
        return True
