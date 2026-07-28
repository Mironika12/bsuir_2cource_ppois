from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

import config as cfg

from domain.student import Student
from domain.project_manager import ProjectManager
from domain.course_project import CourseProject
from domain.deadline import Deadline


class StorageService:
    def __init__(self):
        self.users_file = Path(cfg.USERS_FILE)


    def load_users(self) -> dict[str, dict]:
        if not self.users_file.exists():
            return {}

        with self.users_file.open("r",encoding="utf-8") as f:
            return json.load(f)


    def save_users(self, users: dict) -> None:
        with self.users_file.open("w",encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)


    def save_project(self, project_file: str, project: CourseProject) -> None:
        data = self.project_to_dict(project)

        with open(project_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def load_project(self, project_file: str, student: Student, project_manager: ProjectManager) -> CourseProject:
        project = student.create_project()
        project_manager.assign_project(project)

        file_path = Path(project_file)

        if not file_path.exists():
            return project

        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        self.dict_to_project(data, project)
        return project
    

    def project_to_dict(self, project: CourseProject) -> dict:
        return {
            "theme": project.theme,
            "state": project.state.name,
            "deadline": (
                {
                    "deadline_date":
                        project.deadline.deadline_date.isoformat()
                }
                if project.deadline
                else None
            ),
            "plan": [
                {
                    "num": item["num"],
                    "task": item["task"],
                    "deadline_date":
                        item["deadline"].deadline_date.isoformat(),
                    "notes": item["notes"],
                }
                for item in project.work_plan.items
            ],
            "references": project.research.references,
            "text_sections": project.text_sections,
            "consultations": [
                consultation.consultation_date.isoformat()
                for consultation in project.consultations
            ],
        }


    def dict_to_project(self, data: dict, project: CourseProject) -> None:
        if data.get("theme"):
            project.choose_theme(data["theme"])

        if data.get("deadline"):
            project.set_deadline(
                Deadline(
                    datetime.fromisoformat(
                        data["deadline"]["deadline_date"]
                    ).date()
                )
            )

        for item in data.get("plan", []):
            project.add_plan_item({
                "num": item["num"],
                "task": item["task"],
                "deadline": Deadline(
                    datetime.fromisoformat(
                        item["deadline_date"]
                    ).date()
                ),
                "notes": item.get("notes"),
            })

        for reference in data.get("references", []):
            project.add_reference(reference)

        for text in data.get("text_sections", []):
            project.write_section(text)

        for consultation_date in data.get(
            "consultations",
            []
        ):
            project.add_consultation(
                datetime.fromisoformat(
                    consultation_date
                ).date()
            )

        if data.get("state") == "SUBMITTED":
            project.submit()