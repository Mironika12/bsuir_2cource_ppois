from typing import List, Any, Dict
from datetime import datetime


class ExportService:
    def __init__(self, export_id: str, formats: List[str], last_export: datetime):
        self.export_id: str = export_id
        self.formats: List[str] = formats
        self.last_export: datetime = last_export
        self.scheduled_tasks: List[Dict[str, Any]] = []

    def export_to_format(self, report: Dict[str, Any], format: str) -> Any:
        if format not in self.formats:
            raise ValueError(f"Format '{format}' is not supported")
        if format == "json":
            return dict(report)
        if format == "text":
            return "\n".join(f"{k}: {v}" for k, v in report.items())
        if format == "dict":
            return report
        raise ValueError(f"Unknown format '{format}'")

    def schedule_export(self, report_generator: Any, schedule_time: datetime) -> None:
        task: Dict[str, Any] = {
            "report_generator": report_generator,
            "schedule_time": schedule_time,
            "created_at": datetime.now()
        }
        self.scheduled_tasks.append(task)
