from typing import Dict, Any
from .GLMapper import GLMapper

class ReportGenerator:
    def __init__(self, report_id: str, type: str, parameters: Dict[str, Any]):
        self.report_id: str = report_id
        self.type: str = type
        self.parameters: Dict[str, Any] = parameters
        self.gl_mapper: GLMapper = None
        self.generated_report: Any = None

    def generate(self) -> Any:
        base_data: Dict[str, Any] = {
            "report_id": self.report_id,
            "type": self.type,
            "parameters": self.parameters
        }

        if self.gl_mapper is not None and "transaction" in self.parameters:
            mapped = self.gl_mapper.map_transaction(self.parameters["transaction"])
            base_data["mapped_gl"] = mapped

        self.generated_report = base_data
        return base_data

    def export(self, format: str) -> Any:
        if self.generated_report is None:
            raise ValueError("Report not generated")

        if format == "dict":
            return self.generated_report

        if format == "json":
            return dict(self.generated_report)

        if format == "text":
            return "\n".join(f"{k}: {v}" for k, v in self.generated_report.items())

        raise ValueError(f"Unsupported export format: {format}")
