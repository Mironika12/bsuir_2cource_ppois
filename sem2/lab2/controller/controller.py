from __future__ import annotations

from model.repository import StudentRepository
from services.search_service import SearchService
from services.xml_service import XMLService, XMLReader
from PyQt6.QtWidgets import QFileDialog, QMessageBox


class MainController:
    def __init__(self, repo: StudentRepository, search_service: SearchService):
        self.repo = repo
        self.search_service = search_service

    def add_student(self, student):
        self.repo.add_student(student)

    def get_all_students(self):
        return self.repo.get_all_students()

    def search_by_group(self, group):
        return self.search_service.find_by_group(group)
    
    def export_xml(self):
        path, _ = QFileDialog.getSaveFileName(None, "Сохранить XML", "", "XML (*.xml)")
        if not path:
            return

        students = self.repo.get_all_students()
        XMLService.export_to_xml(path, students)

        QMessageBox.information(None, "XML", "Данные сохранены")

    def import_xml(self):
        path, _ = QFileDialog.getOpenFileName(None, "Открыть XML", "", "XML (*.xml)")
        if not path:
            return

        students = XMLReader.import_from_xml(path)

        self.repo.clear_all()

        for s in students:
            self.repo.add_student(s)

        QMessageBox.information(None, "XML", "Данные загружены")