

# Лабораторная работа №1

**Система управления курсовым проектом**

## Важные сущности

* студент
* научный руководитель
* курсовой проект
* состояние проекта
* дедлайн
* план работы
* пункт плана
* исследование
* источник
* консультация

---

## Описание проекта

Консольная система управления жизненным циклом курсового проекта.

Пользователь может:

* зарегистрироваться и авторизоваться по номеру студенческого билета и PIN
* создать курсовой проект
* выбрать тему
* формировать план выполнения
* добавлять источники и отмечать их как прочитанные
* писать текст работы
* назначать дедлайн
* проводить консультации с руководителем
* сдавать проект
* сохранять и загружать состояние проекта (JSON-файл)

Проект реализован с соблюдением принципов предметно-ориентированного проектирования (DDD).
Центральным агрегатом является `CourseProject`.

---

## Основные классы

### `domain.project_state.ProjectState` (Enum)

```python
CREATED
TOPIC_SELECTED
PLANNING
RESEARCH
WRITING
CONSULTING
SUBMITTED
```

Определяет этап жизненного цикла проекта.

---

### `domain.deadline.Deadline`

**Атрибуты**

* `deadline_date: date` — установленный дедлайн
* `semester_end_date: date` — автоматически вычисляемый конец семестра

**Логика**

* вычисляет конец семестра относительно текущей даты
* запрещает устанавливать дедлайн позже конца семестра

**Свойства**

* `deadline_date`
* `semester_end_date`

---

### `domain.item.Item` (TypedDict)

```python
num: int
task: str
deadline: Deadline
notes: Optional[str]
```

Структура одного пункта плана.

---

### `domain.reference.Reference` (TypedDict)

```python
reference: str
is_read: bool
```

Структура источника исследования.

---

### `domain.work_plan.WorkPlan`

Отвечает за хранение и валидацию пунктов плана.

**Атрибуты**

* `items: List[Item]` — список пунктов (возвращается копия)

**Методы**

* `__iadd__(item)` — добавить пункт
* `__isub__(item)` — удалить пункт

Проверяет:

* корректность структуры
* типы полей
* положительный номер
* непустое описание задачи
* корректный объект `Deadline`

---

### `domain.research.Research`

Управляет источниками исследования.

**Атрибуты**

* `references: List[Reference]`

**Методы**

* `add_reference(reference)` — добавление источника
* `mark_as_read(index)` — отметить как прочитанный
* `get_unread()` — вернуть список непрочитанных источников

Выполняет строгую валидацию структуры источника.

---

### `domain.consultation.Consultation`

Консультация по конкретному проекту.

**Атрибуты**

* `consultation_date: date`
* `project: CourseProject`
* `project_manager: ProjectManager`
* `student: Student`

При создании автоматически регистрируется у руководителя.

Проверяет согласованность:

* руководитель закреплён за проектом
* студент связан с проектом

---

### `domain.project_manager.ProjectManager`

Научный руководитель.

**Атрибуты**

* `name: str` — формат: `И. И. Фамилия`
* `projects: List[CourseProject]`
* `consultations: List[Consultation]`

**Методы**

* `assign_project(project)` — закрепить проект
* `remove_project(project)`
* `register_consultation(consultation)`
* `remove_consultation(consultation)`

---

### `domain.student.Student`

Студент.

**Атрибуты**

* `name: str`
* `student_id: str`
* `course_project: Optional[CourseProject]`

**Методы**

* `create_project()` — создать курсовой проект
* `remove_project()` — удалить проект

Один студент может иметь только один проект.

---

### `domain.course_project.CourseProject`

Центральный агрегат предметной области.

**Атрибуты**

* `theme: Optional[str]`
* `student: Optional[Student]`
* `supervisor: Optional[ProjectManager]`
* `deadline: Optional[Deadline]`
* `work_plan: WorkPlan`
* `research: Research`
* `consultations: List[Consultation]`
* `text_sections: List[str]`
* `state: ProjectState`

---

### Жизненный цикл проекта

#### 1. CREATED

Проект создан, тема не выбрана.

#### 2. TOPIC_SELECTED

Тема выбрана.

Метод:

* `choose_theme(theme)`

---

#### 3. PLANNING

Формирование плана.

Методы:

* `add_plan_item(item)`
* `remove_plan_item(item)`

---

#### 4. RESEARCH

Добавление источников.

Метод:

* `add_reference(reference)`

---

#### 5. WRITING

Написание текста.

Метод:

* `write_section(text)`

---

#### 6. CONSULTING

Проведение консультации.

Метод:

* `add_consultation(date)`

---

#### 7. SUBMITTED

Проект сдан.

Метод:

* `submit()`

Условия сдачи:

* состояние `WRITING`
* установлен дедлайн
* написан текст

---

## CLI-интерфейс

Файл: `cli.py`

Возможности:

1. Выбрать тему
2. Добавить пункт плана
3. Добавить источник
4. Отметить источник как прочитанный
5. Написать текст
6. Назначить дедлайн
7. Провести консультацию
8. Сдать проект
9. Показать состояние
10. Сохранить и выйти

---

## Хранение данных

* Пользователи: `users.json`
* Проекты: `project_<student_id>.json`

Сохраняются:

* тема
* состояние
* дедлайн
* план
* источники
* текст
* консультации

---

## Исключения

Используются стандартные исключения Python:

* `ValueError` — нарушение бизнес-логики
* `TypeError` — неверный тип данных

Валидация реализована на уровне доменной модели.
