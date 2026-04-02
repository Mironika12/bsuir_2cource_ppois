from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QComboBox, QMessageBox, QTableWidget, QTableWidgetItem
)

from controller.controller import MainController
from model.student import Student
from config import (
    FIRST_BTN, PREV_BTN, LAST_BTN, NEXT_BTN,
    PAGE_SIZE_BOX
)


class SearchDialog(QDialog):
    def __init__(self, controller: MainController):
        super().__init__()
        self.controller = controller

        self.current_page: int = 0
        self.page_size: int = 10
        self.students: list[Student] = []

        self.setWindowTitle("Поиск")
        self.resize(600, 400)

        self.init_ui()


    def init_ui(self):
        self.create_widgets()
        self.setup_layouts()
        self.connect_signals()

    def create_widgets(self):
        self.group_input = QLineEdit()

        self.subject_combo = QComboBox()
        self.subject_combo.addItems(self.controller.repo.get_subjects())

        self.min_score = QLineEdit()
        self.max_score = QLineEdit()

        self.min_avg = QLineEdit()
        self.max_avg = QLineEdit()

        self.search_btn = QPushButton("Найти")

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ФИО", "Группа", "Средний балл"])

        self.first_btn = QPushButton(FIRST_BTN)
        self.prev_btn = QPushButton(PREV_BTN)
        self.next_btn = QPushButton(NEXT_BTN)
        self.last_btn = QPushButton(LAST_BTN)

        self.page_label = QLabel()
        self.total_label = QLabel()

        self.page_size_box = QComboBox()
        self.page_size_box.addItems(PAGE_SIZE_BOX)
        self.page_size_box.setCurrentText(PAGE_SIZE_BOX[0])

    def setup_layouts(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Группа:"))
        layout.addWidget(self.group_input)

        layout.addWidget(QLabel("Предмет:"))
        layout.addWidget(self.subject_combo)

        score_layout = QHBoxLayout()
        score_layout.addWidget(QLabel("Балл от:"))
        score_layout.addWidget(self.min_score)
        score_layout.addWidget(QLabel("до:"))
        score_layout.addWidget(self.max_score)
        layout.addLayout(score_layout)

        avg_layout = QHBoxLayout()
        avg_layout.addWidget(QLabel("Средний от:"))
        avg_layout.addWidget(self.min_avg)
        avg_layout.addWidget(QLabel("до:"))
        avg_layout.addWidget(self.max_avg)
        layout.addLayout(avg_layout)

        layout.addWidget(self.search_btn)

        layout.addWidget(self.table)

        pagination_layout = QHBoxLayout()

        pagination_layout.addWidget(self.first_btn)
        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_btn)
        pagination_layout.addWidget(self.last_btn)

        pagination_layout.addWidget(QLabel("На странице:"))
        pagination_layout.addWidget(self.page_size_box)
        pagination_layout.addWidget(self.total_label)

        layout.addLayout(pagination_layout)

        self.setLayout(layout)

    def connect_signals(self):
        self.search_btn.clicked.connect(self.search)

        self.first_btn.clicked.connect(self.first_page)
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.last_btn.clicked.connect(self.last_page)

        self.page_size_box.currentTextChanged.connect(self.change_page_size)

    def search(self):
        group = self.group_input.text().strip()
        subject = self.subject_combo.currentText()

        min_score = self.min_score.text().strip()
        max_score = self.max_score.text().strip()

        min_avg = self.min_avg.text().strip()
        max_avg = self.max_avg.text().strip()

        try:
            students = self.controller.get_all_students()
            
            if not group and not min_score and not min_avg:
                QMessageBox.warning(self, "Ошибка", "Введите хотя бы одно условие")
                return

            if group:
                students = [s for s in students if s.group == group]

            if min_score or max_score:
                min_score = int(min_score) if min_score else 0
                max_score = int(max_score) if max_score else 10

                students = [
                    s for s in students
                    if any(
                        e.subject == subject and min_score <= e.score <= max_score
                        for e in s.exams
                    )
                ]

            if min_avg or max_avg:
                min_avg = float(min_avg) if min_avg else 0.0
                max_avg = float(max_avg) if max_avg else 10.0

                students = [
                    s for s in students
                    if min_avg <= s.get_average_score() <= max_avg
                ]

            if not students:
                QMessageBox.information(self, "Результат", "Ничего не найдено")

            self.students = students
            self.current_page = 0
            self.show_page()

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректные числа")
            
    def show_page(self):
        total = len(self.students)
        self.page_size = int(self.page_size_box.currentText())

        total_pages = max(1, (total + self.page_size - 1) // self.page_size)

        if self.current_page >= total_pages:
            self.current_page = total_pages - 1

        start = self.current_page * self.page_size
        end = start + self.page_size

        page_students = self.students[start:end]

        self.table.setRowCount(len(page_students))

        for row, student in enumerate(page_students):
            self.table.setItem(row, 0, QTableWidgetItem(student.fio))
            self.table.setItem(row, 1, QTableWidgetItem(student.group))
            self.table.setItem(
                row, 2,
                QTableWidgetItem(f"{student.get_average_score():.2f}")
            )

        self.page_label.setText(
            f"Страница {self.current_page + 1} из {total_pages}"
            )

        self.total_label.setText(
            f"Записей: {total}"
            )
        
    def first_page(self):
        self.current_page = 0
        self.show_page()


    def last_page(self):
        total_pages = (len(self.students) + self.page_size - 1) // self.page_size
        self.current_page = max(0, total_pages - 1)
        self.show_page()


    def next_page(self):
        total_pages = (len(self.students) + self.page_size - 1) // self.page_size
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.show_page()


    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()


    def change_page_size(self):
        self.current_page = 0
        self.show_page()