import re

class ProjectManager:
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError()
        self.__name = name
        self.__course_projects: list[CourseProject] = []
        self.__consultations: list[Consultation] = []

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError()
        if not re.fullmatch(r"[А-Я]\. *[А-Я]\. *[А-Я]+", name):
            raise ValueError("Имя не соответствует формату (И. И. Иванов).")
        self.__name = name

    def add_project(self, project: CourseProject):
        if not isinstance(project, CourseProject):
            raise TypeError("Тип данных не соответствует.")
        return self.__course_projects.append(project)
    
    def remove_project(self, project: CourseProject):
        if not isinstance(project, CourseProject):
            raise TypeError("Тип данных не соответствуетю")
        return self.__course_projects.remove(project)
    
    def add_consultation(self, consultation: Consultation):
        # проверка
        self.__consultations.append(consultation)
    
    def remove_consultation(self, consultation: Consultation):
        # проверка, try except
        self.__consultations.remove(consultation)