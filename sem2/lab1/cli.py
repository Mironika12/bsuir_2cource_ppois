import json
import os
from datetime import datetime, date

from domain.student import Student
from domain.project_manager import ProjectManager
from domain.deadline import Deadline
from domain.project_state import ProjectState


USERS_FILE = "users.json"


# -------------------- ВСПОМОГАТЕЛЬНЫЕ --------------------

def input_date(prompt: str) -> date:
    return datetime.strptime(input(prompt), "%Y-%m-%d").date()


def load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def validate_student_id(student_id: str) -> bool:
    return student_id.isdigit() and len(student_id) == 8


def validate_pin(pin: str) -> bool:
    return pin.isdigit() and len(pin) == 4


# -------------------- СЕРИАЛИЗАЦИЯ ПРОЕКТА --------------------

def save_project(project_file: str, project) -> None:
    data = {
        "theme": project.theme,
        "state": project.state.name,
        "deadline": None,
        "plan": [],
        "references": project.research.references,
        "text_sections": project.text_sections,
        "consultations": [
            c.consultation_date.isoformat()
            for c in project.consultations
        ],
    }

    if project.deadline:
        data["deadline"] = {
            "deadline_date": project.deadline.deadline_date.isoformat(),
            # "semester_end_date": project.deadline.semester_end_date.isoformat(),
        }

    for item in project.work_plan.items:
        data["plan"].append({
            "num": item["num"],
            "task": item["task"],
            "deadline_date": item["deadline"].deadline_date.isoformat(),
            # "semester_end_date": item["deadline"].semester_end_date.isoformat(),
            "notes": item["notes"],
        })

    with open(project_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_project(project_file: str, student: Student, supervisor: ProjectManager):
    project = student.create_project()
    supervisor.assign_project(project)

    if not os.path.exists(project_file):
        return project

    with open(project_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data["theme"]:
        project.choose_theme(data["theme"])

    if data["deadline"]:
        deadline = Deadline(
            datetime.fromisoformat(data["deadline"]["deadline_date"]).date()
        )
        project.set_deadline(deadline)

    for item in data["plan"]:
        deadline = Deadline(
            datetime.fromisoformat(item["deadline_date"]).date()
        )
        project.add_plan_item({
            "num": item["num"],
            "task": item["task"],
            "deadline": deadline,
            "notes": item["notes"],
        })

    for ref in data["references"]:
        project.add_reference(ref)

    for text in data["text_sections"]:
        project.write_section(text)

    for c_date in data["consultations"]:
        project.add_consultation(datetime.fromisoformat(c_date).date())

    if data["state"] == "SUBMITTED":
        project.submit()

    return project


# -------------------- АВТОРИЗАЦИЯ --------------------

def authenticate():
    users = load_users()

    student_id = input("Введите номер студенческого билета (8 цифр): ")

    if not validate_student_id(student_id):
        print("Номер должен состоять из 8 цифр.")
        return None

    # Новый студент
    if student_id not in users:
        print("Студент не найден. Создание нового пользователя.")
        name = input("Введите ваше имя: ")
        supervisor_name = input("Введите имя руководителя (И. И. Фамилия): ")

        pin = input("Создайте 4-значный PIN-код: ")
        if not validate_pin(pin):
            print("PIN должен состоять из 4 цифр.")
            return None

        project_file = f"project_{student_id}.json"

        users[student_id] = {
            "pin": pin,
            "student_name": name,
            "supervisor_name": supervisor_name,
            "project_file": project_file
        }

        save_users(users)
        print("Пользователь создан.")

    else:
        pin = input("Введите PIN-код: ")
        if users[student_id]["pin"] != pin:
            print("Неверный PIN.")
            return None

    return student_id, users


# -------------------- CLI --------------------

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


def main():
    auth = authenticate()
    if not auth:
        return

    student_id, users = auth
    user_data = users[student_id]

    student = Student(user_data["student_name"], student_id)
    supervisor = ProjectManager(user_data["supervisor_name"])

    project = load_project(user_data["project_file"], student, supervisor)

    while True:
        print_menu()
        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                project.choose_theme(input("Тема: "))

            elif choice == "2":
                num = int(input("Номер: "))
                task = input("Задача: ")
                d = input_date("Дедлайн (YYYY-MM-DD): ")
                project.add_plan_item({
                    "num": num,
                    "task": task,
                    "deadline": Deadline(d),
                    "notes": None,
                })

            elif choice == "3":
                project.add_reference({
                    "reference": input("Источник: "),
                    "is_read": False
                })

            elif choice == "4":
                project.research.mark_as_read(int(input("Индекс: ")))

            elif choice == "5":
                project.write_section(input("Текст: "))

            elif choice == "6":
                d = input_date("Дедлайн (YYYY-MM-DD): ")
                project.set_deadline(Deadline(d))

            elif choice == "7":
                project.add_consultation(input_date("Дата (YYYY-MM-DD): "))

            elif choice == "8":
                project.submit()

            elif choice == "9":
                print("Тема:", project.theme)
                print("Состояние:", project.state.name)

                if project.deadline:
                    print("Дедлайн:", project.deadline.deadline_date)
                    print("Конец семестра (авто):", project.deadline.semester_end_date)

            elif choice == "0":
                save_project(user_data["project_file"], project)
                print("Проект сохранён. Выход.")
                break

        except Exception as e:
            print("Ошибка:", e)


if __name__ == "__main__":
    main()