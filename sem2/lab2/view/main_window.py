from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QAbstractItemView, QMessageBox,
    QLabel, QTreeWidget, QTreeWidgetItem, QComboBox,
    QMenuBar, QMenu, QToolBar
)
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QTabWidget

from view.dialogs.add_dialog import AddDialog
from view.dialogs.search_dialog import SearchDialog
from view.dialogs.delete_dialog import DeleteDialog
from controller.controller import MainController
from model.student import Student
from config import (
    FIRST_BTN, PREV_BTN, NEXT_BTN, LAST_BTN,
    PAGE_SIZE_BOX
)


class MainWindow(QMainWindow):
    def __init__(self, controller: MainController):
        super().__init__()

        self.controller = controller

        self.setWindowTitle("Студенты")
        self.resize(800, 600)

        self.current_page: int = 0
        self.page_size: int = 10
        self.students: list[Student] = []

        self.create_menu_and_toolbar()
        self.init_ui()
        self.load_data()


    def init_ui(self):
        self.create_widgets()
        self.setup_layouts()
        self.connect_signals()

    def create_widgets(self):
        self.table: QTableWidget = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ФИО", "Группа", "Средний балл"])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.tree: QTreeWidget = QTreeWidget()
        self.tree.setHeaderLabels(["Студенты"])

        self.first_btn: QPushButton = QPushButton(FIRST_BTN)
        self.prev_btn: QPushButton = QPushButton(PREV_BTN)
        self.next_btn: QPushButton = QPushButton(NEXT_BTN)
        self.last_btn: QPushButton = QPushButton(LAST_BTN)

        self.page_label: QLabel = QLabel()
        self.total_label: QLabel = QLabel()

        self.page_size_box: QComboBox = QComboBox()
        self.page_size_box.addItems(PAGE_SIZE_BOX)
        self.page_size_box.setCurrentText(PAGE_SIZE_BOX[0])

    def setup_layouts(self):
        central_widget: QWidget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout: QVBoxLayout = QVBoxLayout()

        pagination_layout: QHBoxLayout = QHBoxLayout()
        pagination_layout.addWidget(self.first_btn)
        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_btn)
        pagination_layout.addWidget(self.last_btn)

        pagination_layout.addWidget(QLabel("На странице:"))
        pagination_layout.addWidget(self.page_size_box)
        pagination_layout.addWidget(self.total_label)

        # вкладки
        self.tabs: QTabWidget = QTabWidget()

        table_widget: QWidget = QWidget()
        table_layout: QVBoxLayout = QVBoxLayout()
        table_layout.addWidget(self.table)
        table_layout.addLayout(pagination_layout)
        table_widget.setLayout(table_layout)

        tree_widget: QWidget = QWidget()
        tree_layout: QVBoxLayout = QVBoxLayout()
        tree_layout.addWidget(self.tree)
        tree_widget.setLayout(tree_layout)

        self.tabs.addTab(table_widget, "Таблица")
        self.tabs.addTab(tree_widget, "Дерево")

        main_layout.addWidget(self.tabs)

        central_widget.setLayout(main_layout)

    def connect_signals(self):
        self.first_btn.clicked.connect(self.first_page)
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.last_btn.clicked.connect(self.last_page)

        self.page_size_box.currentTextChanged.connect(self.change_page_size)

        # --- MENU + TOOLBAR ---
        self.add_action.triggered.connect(self.on_add_clicked)
        self.search_action.triggered.connect(self.on_search_clicked)
        self.delete_action.triggered.connect(self.on_delete_clicked)

        self.export_action.triggered.connect(self.controller.export_xml)
        self.import_action.triggered.connect(self.on_import_xml)
        self.clear_action.triggered.connect(self.on_clear_db)
        

    def load_data(self):
        self.students = self.controller.get_all_students()
        self.current_page = 0
        self.show_page()
        self.load_tree()

    def show_page(self):
        self.table.clearContents()
        total = len(self.students)
        self.page_size = int(self.page_size_box.currentText())

        total_pages = (
            (total + self.page_size - 1) // self.page_size
            if total > 0 else 1
            )

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

    
    def create_menu_and_toolbar(self):
        # ===== MENU =====
        menu: QMenuBar | None = self.menuBar()
        assert menu is not None

        file_menu: QMenu | None = menu.addMenu("Файл")
        assert file_menu is not None
        actions_menu: QMenu | None = menu.addMenu("Действия")
        assert actions_menu is not None

        # ===== ACTIONS =====
        self.add_action = QAction("Добавить", self)
        self.search_action = QAction("Поиск", self)
        self.delete_action = QAction("Удалить", self)
        self.export_action = QAction("Экспорт XML", self)
        self.import_action = QAction("Импорт XML", self)
        self.clear_action = QAction("Очистить БД", self)

        # меню
        actions_menu.addAction(self.add_action)
        actions_menu.addAction(self.search_action)
        actions_menu.addAction(self.delete_action)

        file_menu.addAction(self.export_action)
        file_menu.addAction(self.import_action)
        file_menu.addAction(self.clear_action)

        # ===== TOOLBAR =====
        toolbar: QToolBar | None = self.addToolBar("Основные действия")
        assert toolbar is not None

        toolbar.addAction(self.add_action)
        toolbar.addAction(self.search_action)
        toolbar.addAction(self.delete_action)
        toolbar.addSeparator()
        toolbar.addAction(self.export_action)
        toolbar.addAction(self.import_action)
        toolbar.addAction(self.clear_action)

    # ===== handlers =====

    def on_add_clicked(self):
        dialog = AddDialog(self.controller)

        if dialog.exec():
            self.load_data()

    def on_search_clicked(self):
        dialog = SearchDialog(self.controller)
        dialog.exec()

    def on_delete_clicked(self):
        dialog = DeleteDialog(self.controller)

        if dialog.exec():
            self.load_data()

    def on_import_xml(self):
        reply = QMessageBox.question(
            self,
            "Импорт",
            "Очистить базу перед импортом?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No |
            QMessageBox.StandardButton.Cancel
        )
        
        if reply == QMessageBox.StandardButton.Cancel:
            return

        if reply == QMessageBox.StandardButton.Yes:
            self.controller.clear_database()

        self.controller.import_xml()
        self.load_data()

    def load_tree(self):
        self.tree.clear()

        students = self.controller.get_all_students()

        for s in students:
            student_text = f"{s.fio} ({s.group}) | ср: {s.get_average_score():.2f}"
            student_item = QTreeWidgetItem([student_text])

            for e in s.exams:
                exam_text = f"{e.subject}: {e.score}"
                exam_item = QTreeWidgetItem([exam_text])
                student_item.addChild(exam_item)

            self.tree.addTopLevelItem(student_item)

        self.tree.expandAll()

    def on_clear_db(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить ВСЕ данные?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.controller.clear_database()
            self.load_data()