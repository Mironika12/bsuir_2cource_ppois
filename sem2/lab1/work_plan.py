class WorkPlan:
    def __init__(self, course_project: CourseProject):
        if not isinstance(course_project, CourseProject):
            raise TypeError("Тип данных не соответствует.")
        self.__course_project = course_project
        self.__work_plan: list[Item] = []

    @property
    def course_project(self):
        return self.__course_project
    
    @property
    def work_plan(self):
        return self.__work_plan

    def __iadd__(self, other: Item):
        if not isinstance(other, Item):
            raise TypeError("Тип данных не соответствует.")
        self.__work_plan.append(other)
        return self
    
    def __isub__(self, other: Item):
        if not isinstance(other, Item):
            raise TypeError("Тип данных не соответствует.")
        # try except
        self.__work_plan.remove(other)
        return self
    
    def print_plan(self):
        for item in self.__work_plan:
            print(f"""
                {item["num"]}. {item["task"]}\n
                Дедлайн: {item["deadline"]}\n
                Заметки: {item["notes"]}\n
            """)

    # 1. {"num": int, "task": "...", "deadile": Deadline, "notes": "..."}
    # 2. ...