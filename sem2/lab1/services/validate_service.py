import re
from datetime import datetime, date
import config as cfg


class ValidationService:
    @staticmethod
    def validate_name(name: str) -> bool:
        return bool(re.fullmatch(cfg.FIO_TEMPLATE, name))

    @staticmethod
    def validate_student_id(student_id: str) -> bool:
        return student_id.isdigit() and len(student_id) == cfg.STUDENT_ID_LEN

    @staticmethod
    def validate_pin(pin: str) -> bool:
        return pin.isdigit() and len(pin) == cfg.PIN_LEN

    @staticmethod
    def parse_date(value: str) -> date:
        return datetime.strptime(value, "%Y-%m-%d").date()