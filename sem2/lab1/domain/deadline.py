from datetime import date, timedelta


class Deadline:
    def __init__(self, deadline_date: date):
        if not isinstance(deadline_date, date):
            raise TypeError("Тип данных не соответствует.")

        self.__deadline_date = deadline_date
        self.__semester_end_date = self.__calculate_semester_end()

        if deadline_date > self.__semester_end_date:
            raise ValueError("Дедлайн не может быть позже конца семестра.")

    # -------------------- ЛОГИКА РАСЧЁТА --------------------

    def __calculate_semester_end(self) -> date:
        today = date.today()

        # Определяем учебный год
        if today.month >= 9:
            academic_year_start = today.year
            is_autumn = True
        else:
            academic_year_start = today.year - 1
            is_autumn = False

        september_first = date(academic_year_start, 9, 1)

        # Понедельник недели, на которой начинается сентябрь
        week_start = september_first - timedelta(days=september_first.weekday())

        # Определяем номер недели конца семестра
        if is_autumn:
            weeks_to_add = 16   # 17-я неделя
        else:
            weeks_to_add = 39   # 40-я неделя

        semester_week_start = week_start + timedelta(weeks=weeks_to_add)

        # Суббота этой недели
        semester_end = semester_week_start + timedelta(days=5)

        return semester_end

    # -------------------- PROPERTIES --------------------

    @property
    def deadline_date(self) -> date:
        return self.__deadline_date

    @property
    def semester_end_date(self) -> date:
        return self.__semester_end_date