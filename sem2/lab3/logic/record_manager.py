import json
import os
import config.config as cfg


class RecordManager:

    def __init__(
        self,
        path=cfg.RECORDS_PATH,
        max_records=5
    ):

        self.path = path
        self.max_records = max_records

        self.records = []

        self.load()

    def load(self):

        if not os.path.exists(self.path):
            return

        with open(self.path, "r") as file:

            self.records = json.load(file)

    def save(self):

        with open(self.path, "w") as file:

            json.dump(
                self.records,
                file,
                indent=4
            )

    def is_new_record(self, score):

        # если таблица ещё не заполнена
        if len(self.records) < self.max_records:
            return True

        # сравнение с последним рекордом
        return score > self.records[-1]["score"]

    def add_record(
        self,
        name,
        score
    ):

        new_record = {
            "name": name,
            "score": score
        }

        self.records.append(new_record)

        # сортировка по убыванию
        self.records.sort(
            key=lambda record: record["score"],
            reverse=True
        )

        # ограничение размера таблицы
        self.records = self.records[:self.max_records]

        self.save()

    def get_records(self):

        return self.records