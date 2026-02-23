from datetime import date, timedelta

class Deadline:
    def __init__(self, deadline_date: date, semester_end_date: date):
        if not isinstance(deadline_date, date) or not isinstance(semester_end_date, date):
            raise TypeError("Тип данных не соответствует.")
        if (semester_end_date - deadline_date) > timedelta(weeks=17):
            raise ValueError("Слишком большой период между дедлайном и датой окончания семестра.")
        self.__deadline_date = deadline_date
        self.__semester_end_date = semester_end_date

    @property
    def deadline_date(self):
        return self.__deadline_date
    
    @deadline_date.setter
    def deadline_date(self, deadline: date):
        if not isinstance(deadline, date):
            raise TypeError("Тип данных не соответствует.")
        if (self.__semester_end_date - deadline) < 0:
            raise ValueError("Нельзя поставить дедлайн после даты окончания семестра.")
        self.__deadline_date = deadline

    @property
    def semester_end_date(self):
        return self.__semester_end_date