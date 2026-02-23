class CourseProject:
    def __init__(self, theme: str):
        if not isinstance(theme, str):
            raise TypeError("Тип данных не соответствует.")
        # тут можно потенциальную проверку на спецсимволы с уточннением
        self.__theme = theme
        self.__PM: ProjectManager = None
        self.__deadline: Deadline = None
        self.__student: Student = None
        self.__plan: WorkPlan = None
    
    @property
    def theme(self):
        return self.__theme
    
    @theme.setter
    def theme(self, theme: str):
        if not isinstance(theme, str):
            raise TypeError("Тип данных не соответствует.")
        self.__theme = theme

    @property
    def PM(self):
        return self.__PM
    
    @PM.setter
    def PM(self, PM: ProjectManager):
        if not isinstance(PM, ProjectManager):
            raise TypeError("Тип данных не соответствует.")
        self.__PM = PM

    @property
    def deadline(self):
        return self.__deadline
    
    @deadline.setter
    def deadline(self, deadline: Deadline):
        if not isinstance(deadline, Deadline):
            raise TypeError("Тип данных не соответствует.")
        self.__deadline = deadline

    @property
    def student(self):
        return self.__student
    
    @student.setter
    def student(self, student: Student):
        if not isinstance(student, Student):
            raise TypeError("Тип данных не соответствует.")
        self.__student = student
        
    @property
    def work_plan(self):
        return self.__plan
    
    @work_plan.setter # нужен только если я хочу заменять весь список, но я наверное этого не хочу
    def work_plan(self, plan: WorkPlan):
        if not isinstance(plan, WorkPlan):
            raise TypeError("Тип данных не соответствует.")
        self.__plan = plan

    def add_plan_item(self, item: Item):
        if not isinstance(item, Item):
            raise TypeError("Тип данных не соответствует.")
        self.__plan += item

    def remove_plan_item(self, item: Item):
        if not isinstance(item, Item):
            raise TypeError("Тип данных не соответствует.")
        self.__plan -= item


    # course_project.plan += {"11.05.2026": "Графические материалы проекта"}
