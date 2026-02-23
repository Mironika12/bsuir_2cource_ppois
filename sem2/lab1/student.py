class Student:
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Тип данных не соответствует.")
        self.__name = name
        self.__course_project: CourseProject = None
        