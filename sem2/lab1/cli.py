import json
from datetime import datetime, date
from pathlib import Path

from course_project import CourseProject
from student import Student
from project_manager import ProjectManager
from deadline import Deadline


DATA_FILE = Path("project_data.json")


# ==========================
# СЕРИАЛИЗАЦИЯ
# ==========================

def save_project(project: CourseProject) -> None:
    data = {
        "theme": project._CourseProject__theme,
        "state": project.state.name,
        "text": project._CourseProject__text_sections,
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_project(student: Student) -> CourseProject | None:
    if not DATA_FILE.exists():
        return None

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    project = student.create_project()
    project.choose_topic(data["theme"])

    for section in data["text"]:
        project.add_text_section(section)

    return project


# ==========================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================

def input_date(prompt: str) -> date:
    value = input(prompt)
    return datetime.strptime(value, "%Y-%m-%d").date()


def pause() -> None:
    input("\nНажмите Enter для продолжения...")


# ==========================
# CLI
# ==========================

def main() -> None:
    print("=== Система управления курсовым проектом ===\n")

    student_name = input("Введите имя студента: ")
    supervisor_name = input("Введите имя руководителя: ")

    student = Student(student_name)
    supervisor = ProjectManager(supervisor_name)

    project = load_project(student)

    if project is None:
        project = student.create_project()

    while True:
        print(f"\nТекущее состояние: {project.state.name}")
        print("""
1. Выбрать тему
2. Добавить пункт плана
3. Добавить источник
4. Написать текст
5. Запросить консультацию
6. Установить дедлайн
7. Сдать проект
8. Сохранить
0. Выход
""")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                theme = input("Введите тему: ")
                project.choose_topic(theme)

            elif choice == "2":
                task = input("Описание задачи: ")
                project.add_plan_item({
                    "num": 1,
                    "task": task,
                    "deadline": None,
                    "notes": None
                })

            elif choice == "3":
                ref = input("Введите источник: ")
                project.add_reference(ref)

            elif choice == "4":
                text = input("Введите текст раздела: ")
                project.add_text_section(text)

            elif choice == "5":
                d = input_date("Дата консультации (YYYY-MM-DD): ")
                project.request_consultation(d)

            elif choice == "6":
                deadline_date = input_date("Дедлайн (YYYY-MM-DD): ")
                semester_end = input_date("Окончание семестра (YYYY-MM-DD): ")
                deadline = Deadline(deadline_date, semester_end)
                project._CourseProject__deadline = deadline

            elif choice == "7":
                project.submit()
                print("Проект успешно сдан.")

            elif choice == "8":
                save_project(project)
                print("Сохранено.")

            elif choice == "0":
                save_project(project)
                print("Выход.")
                break

            else:
                print("Неверный выбор.")

        except Exception as e:
            print(f"Ошибка: {e}")

        pause()


if __name__ == "__main__":
    main()