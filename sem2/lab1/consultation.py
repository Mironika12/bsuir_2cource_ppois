from datetime import date

class Consultation:
    def __init__(self, consultation_date: date, project_manager: ProjectManager, student: Student):
        if not isinstance(consultation_date, date):
            raise TypeError("Тип данных не соответствует.")
        # проверки
        self.__consultation_date = consultation_date
        self.__PM = project_manager
        self.__student = student

    @property
    def consultation_date(self):
        return self.__consultation_date
    
    @consultation_date.setter
    def consultation_date(self, consultation_date: date):
        if not isinstance(consultation_date, date):
            raise TypeError()
        self.__consultation_date = consultation_date
    
    @property
    def PM(self):
        return self.__PM
    
    @PM.setter
    def PM(self, PM: ProjectManager):
        if not isinstance(PM, ProjectManager):
            raise TypeError()
        self.__PM = PM

    @property
    def student(self):
        return self.__student
    
    @student.setter
    def student(self, student: Student):
        if not isinstance(student, Student):
            raise TypeError()
        self.__student = student