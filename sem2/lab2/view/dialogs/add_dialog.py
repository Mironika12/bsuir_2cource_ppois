from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem,
    QMessageBox
)

from model.student import Student
from model.exam import Exam
from controller.controller import MainController
from config import FIO_REGEX, GROUP_REGEX, SUBJECT_REGEX


class AddDialog(QDialog):
    def __init__(self, controller: MainController):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Добавить студента")
        self.resize(500, 400)

        self.init_ui()


    def init_ui(self):
        self.create_widgets()
        self.setup_layouts()
        self.connect_signals()

    def create_widgets(self):
        # поля
        self.fio_input = QLineEdit()
        self.group_input = QLineEdit()

        # таблица экзаменов
        self.exam_table = QTableWidget()
        self.exam_table.setColumnCount(2)
        self.exam_table.setHorizontalHeaderLabels(["Предмет", "Балл"])

        # кнопки экзаменов
        self.add_exam_btn = QPushButton("Добавить экзамен")
        self.remove_exam_btn = QPushButton("Удалить экзамен")

        # кнопки формы
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")

    def setup_layouts(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("ФИО:"))
        layout.addWidget(self.fio_input)

        layout.addWidget(QLabel("Группа:"))
        layout.addWidget(self.group_input)

        layout.addWidget(QLabel("Экзамены:"))
        layout.addWidget(self.exam_table)

        exam_btn_layout = QHBoxLayout()
        exam_btn_layout.addWidget(self.add_exam_btn)
        exam_btn_layout.addWidget(self.remove_exam_btn)
        layout.addLayout(exam_btn_layout)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def connect_signals(self):
        self.add_exam_btn.clicked.connect(self.add_exam_row)
        self.remove_exam_btn.clicked.connect(self.remove_exam_row)
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)

    def add_exam_row(self):
        row = self.exam_table.rowCount()
        self.exam_table.insertRow(row)

    def remove_exam_row(self):
        row = self.exam_table.currentRow()
        if row >= 0:
            self.exam_table.removeRow(row)

    def save(self):
        fio = self.fio_input.text().strip()
        group = self.group_input.text().strip()

        if not fio or not group:
            QMessageBox.warning(self, "Ошибка", "Заполните ФИО и группу")
            return

        if not FIO_REGEX.match(fio):
            QMessageBox.warning(
                self,
                "Ошибка",
                "ФИО должно быть в формате: Иванов И.И."
            )
            return

        if not GROUP_REGEX.match(group):
            QMessageBox.warning(
                self,
                "Ошибка",
                "Группа должна содержать 6 цифр"
            )
            return

        exams = []

        for row in range(self.exam_table.rowCount()):
            subject_item = self.exam_table.item(row, 0)
            score_item = self.exam_table.item(row, 1)

            if not subject_item or not score_item:
                continue

            subject = subject_item.text().strip()
            score_text = score_item.text().strip()

            if not subject or not score_text:
                continue
            
            if not SUBJECT_REGEX.match(subject):
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Название предмета должно быть словом"
                )
                return

            try:
                score = int(score_text)
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Балл должен быть числом")
                return
            
            if not (0 <= score <= 10):
                QMessageBox.warning(self, "Ошибка", "Балл должен быть от 0 до 10")
                return

            exams.append(Exam(subject, score))

        if not exams:
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один экзамен")
            return

        student = Student(fio, group, exams)

        self.controller.add_student(student)

        self.accept()