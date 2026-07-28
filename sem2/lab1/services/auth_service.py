from __future__ import annotations

import config as cfg

from services.validate_service import ValidationService
from services.storage_service import StorageService


class AuthService:
    def __init__(self, storage: StorageService, validator: ValidationService):
        self.storage = storage
        self.validator = validator


    def login(self, student_id: str, pin: str) -> dict:
        users = self.storage.load_users()

        if not self.validator.validate_student_id(student_id):
            raise ValueError("Номер студенческого билета должен состоять из 8 цифр.")

        if users[student_id]["pin"] != pin:
            raise ValueError("Неверный PIN-код.")

        return users[student_id]


    def register(self, student_id: str, student_name: str, project_manager_name: str, pin: str) -> dict:
        users = self.storage.load_users()

        if not self.validator.validate_student_id(student_id):
            raise ValueError("Номер студенческого билета должен состоять из 8 цифр.")

        if not self.validator.validate_name(student_name):
            raise ValueError("Имя должно быть в формате: И. И. Иванов")

        if not self.validator.validate_name(project_manager_name):
            raise ValueError("Имя руководителя должно быть в формате: И. И. Иванов")

        if not self.validator.validate_pin(pin):
            raise ValueError("PIN должен состоять из 4 цифр.")

        project_file = cfg.PROJECT_FILE_BEGIN + student_id + cfg.PROJECT_FILE_END

        user_data = {
            "pin": pin,
            "student_name": student_name,
            "project_manager_name": project_manager_name,
            "project_file": project_file,
        }

        users[student_id] = user_data
        self.storage.save_users(users)

        return user_data