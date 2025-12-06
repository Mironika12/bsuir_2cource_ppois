from typing import List, Dict, Any


class AuditLogger:
    def __init__(self, logger_id: str, destination: str, level: str):
        self.logger_id: str = logger_id
        self.destination: str = destination
        self.level: str = level
        self.logs: List[Dict[str, Any]] = []

    def log(self, action: str, payroll_record: Any = None) -> bool:
        log_entry: Dict[str, Any] = {
            "action": action,
            "payroll_record": payroll_record
        }
        self.logs.append(log_entry)
        return True

    def query_logs(self, level_filter: str = None) -> List[Dict[str, Any]]:
        if level_filter:
            return [log for log in self.logs if log.get("level") == level_filter]
        return self.logs
