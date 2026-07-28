from __future__ import annotations

from domain.student import Student
from domain.project_manager import ProjectManager
from domain.deadline import Deadline

from services.auth_service import AuthService
from services.storage_service import StorageService
from services.validate_service import ValidationService


def print_auth_menu():
    print("""
1. Войти
2. Зарегистрироваться
0. Выход
""")


def print_menu():
    print("""
1. Выбрать тему
2. Добавить пункт плана
3. Добавить источник
4. Отметить источник как прочитанный
5. Написать текст
6. Назначить дедлайн
7. Провести консультацию
8. Сдать проект
9. Показать состояние
0. Выход
""")


def auth_menu(auth_service: AuthService) -> tuple[str, dict] | None:
    while True:
        print_auth_menu()
        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                student_id = input("Номер студенческого билета: ").strip()
                pin = input("PIN-код: ").strip()
                user_data = auth_service.login(student_id, pin)

                print("Вход выполнен успешно.")
                return student_id, user_data

            elif choice == "2":
                student_id = input("Номер студенческого билета: ").strip()

                student_name = input("ФИО студента (И. И. Иванов): ").strip()

                project_manager_name = input("ФИО руководителя (И. И. Иванов): ").strip()

                pin = input("PIN-код: ").strip()

                user_data = auth_service.register(
                    student_id,
                    student_name,
                    project_manager_name,
                    pin,
                )

                print("Регистрация завершена.")
                return student_id, user_data

            elif choice == "0":
                return None

            else:
                print("Неизвестная команда.")

        except Exception as e:
            print("Ошибка:", e)


def main():
    storage = StorageService()
    validator = ValidationService()
    auth_service = AuthService(storage, validator)

    auth = auth_menu(auth_service)

    if not auth:
        print("Выход из программы.")
        return

    student_id, user_data = auth

    student = Student(user_data["student_name"], student_id)
    supervisor = ProjectManager(user_data["project_manager_name"])

    project = storage.load_project(
        user_data["project_file"],
        student,
        supervisor,
    )

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                project.choose_theme(input("Тема: "))

            elif choice == "2":
                num = int(input("Номер: "))
                task = input("Задача: ")
                d = validator.parse_date(input("Дедлайн (YYYY-MM-DD): "))

                project.add_plan_item({
                    "num": num,
                    "task": task,
                    "deadline": Deadline(d),
                    "notes": None,
                })

            elif choice == "3":
                project.add_reference({
                    "reference": input("Источник: "),
                    "is_read": False,
                })

            elif choice == "4":
                index = int(input("Индекс: "))
                project.research.mark_as_read(index)

            elif choice == "5":
                project.write_section(input("Текст: "))

            elif choice == "6":
                d = validator.parse_date(input("Дедлайн (YYYY-MM-DD): "))
                project.set_deadline(Deadline(d))

            elif choice == "7":
                consultation_date = validator.parse_date(input("Дата (YYYY-MM-DD): "))

                project.add_consultation(consultation_date)

            elif choice == "8":
                project.submit()
                print("Проект отправлен.")

            elif choice == "9":
                print(f"Тема: {project.theme}")
                print(f"Состояние: {project.state.name}")
                if project.deadline:
                    print(f"Дедлайн: {project.deadline.deadline_date}")
                    print(f"Конец семестра: {project.deadline.semester_end_date}")

            elif choice == "0":
                storage.save_project(
                    user_data["project_file"],
                    project,
                )

                print("Проект сохранён. Выход.")
                break

            else:
                print("Неизвестная команда.")

        except Exception as e:
            print("Ошибка:", e)


if __name__ == "__main__":
    main()