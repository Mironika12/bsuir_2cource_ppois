from typing import Any, List, Dict


class PayrollFileImporter:
    def __init__(self, import_id: str, source_type: str, mapping: Dict[str, str]):
        self.import_id: str = import_id
        self.source_type: str = source_type
        self.mapping: Dict[str, str] = mapping
        self.records: List[Dict[str, Any]] = []

    def parse_file(self, file_content: Any) -> List[Dict[str, Any]]:
        parsed_records: List[Dict[str, Any]] = []
        for line in file_content:
            record = {target: line.get(source) for source, target in self.mapping.items()}
            parsed_records.append(record)
        self.records = parsed_records
        return self.records

    def validate_records(self) -> bool:
        for record in self.records:
            if "employee_id" not in record or record["employee_id"] is None:
                return False
        return True
