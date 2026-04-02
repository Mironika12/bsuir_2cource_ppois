from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QComboBox, QMessageBox
)

from controller.controller import MainController


class DeleteDialog(QDialog):
    def __init__(self, controller: MainController):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Удаление")
        self.resize(500, 300)

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

        self.delete_btn = QPushButton("Удалить")

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

        layout.addWidget(self.delete_btn)

        self.setLayout(layout)

    def connect_signals(self):
        self.delete_btn.clicked.connect(self.delete)


    def delete(self):
        group = self.group_input.text().strip()
        subject = self.subject_combo.currentText()

        min_score = self.min_score.text().strip()
        max_score = self.max_score.text().strip()

        min_avg = self.min_avg.text().strip()
        max_avg = self.max_avg.text().strip()

        try:
            students = self.controller.get_all_students()

            if group:
                students = [s for s in students if s.group == group]

            if min_score or max_score:
                min_score = int(min_score) if min_score else 0
                max_score = int(max_score) if max_score else 10

                students = [
                    s for s in students
                    if any(
                        e.subject == subject and (min_score <= e.score and e.score <= max_score)
                        for e in s.exams
                    )
                ]

            if min_avg or max_avg:
                min_avg = float(min_avg) if min_avg else 0.0
                max_avg = float(max_avg) if max_avg else 10.0

                students = [
                    s for s in students
                    if min_avg <= s.get_average_score() and s.get_average_score() <= max_avg
                ]

            if not students:
                QMessageBox.information(self, "Результат", "Ничего не найдено")
                return

            count = 0
            for student in students:
                assert student.id is not None
                self.controller.repo.delete_by_id(student.id)
                count += 1

            QMessageBox.information(
                self,
                "Удаление",
                f"Удалено записей: {count}"
            )

            self.accept()

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректные числа")