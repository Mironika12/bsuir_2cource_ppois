from xml.dom.minidom import Document
import xml.sax as sax

from model.student import Student
from model.exam import Exam


class XMLService:
    @staticmethod
    def export_to_xml(file_path: str, students: list[Student]):
        doc = Document()
        root = doc.createElement("students")
        doc.appendChild(root)

        for s in students:
            student_node = doc.createElement("student")

            student_node.setAttribute("fio", s.fio)
            student_node.setAttribute("group", s.group)

            exams_node = doc.createElement("exams")

            for e in s.exams:
                exam_node = doc.createElement("exam")
                exam_node.setAttribute("subject", e.subject)
                exam_node.setAttribute("score", str(e.score))
                exams_node.appendChild(exam_node)

            student_node.appendChild(exams_node)
            root.appendChild(student_node)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(doc.toprettyxml(indent="  "))


class StudentHandler(sax.ContentHandler):
    def __init__(self):
        self.students: list[Student] = []
        self.current_student: Student | None = None

    def startElement(self, name, attrs):
        if name == "student":
            if self.current_student is not None:
                return
            
            fio = attrs.get("fio", "").strip()
            group = attrs.get("group", "").strip()

            if not fio or not group:
                return
            self.current_student = Student(fio, group, exams=[])
            

        elif name == "exam":
            if self.current_student is None:
                return
            
            subject = attrs.get("subject")
            score = attrs.get("score")

            if subject is None or score is None:
                return
            
            try:
                score = int(score)
            except (ValueError, TypeError):
                return

            exam = Exam(subject, int(score))
            self.current_student.exams.append(exam)

    def endElement(self, name):
        if name == "student":
            assert self.current_student is not None
            self.students.append(self.current_student)
            self.current_student = None


class XMLReader:
    @staticmethod
    def import_from_xml(file_path: str):
        handler = StudentHandler()
        try:
            sax.parse(file_path, handler)
        except Exception:
            return []
        return handler.students