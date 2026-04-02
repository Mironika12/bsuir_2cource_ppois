import sys
from PyQt6.QtWidgets import QApplication

from model.database import Database
from model.repository import StudentRepository
from services.search_service import SearchService
from view.main_window import MainWindow
from controller.controller import MainController


def main():
    app = QApplication(sys.argv)

    # модель
    db = Database()
    db.create_tables()

    repo = StudentRepository(db)
    search_service = SearchService(repo)

    controller = MainController(repo, search_service)

    # GUI
    window = MainWindow(controller)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()