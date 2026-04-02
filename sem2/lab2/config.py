import re

FIO_REGEX = re.compile(r"^[А-ЯЁ][а-яё]+ [А-ЯЁ]\.[А-ЯЁ]\.$")
GROUP_REGEX = re.compile(r"^\d{6}$")
SUBJECT_REGEX = re.compile(r"^[А-ЯЁа-яё]+$")

FIRST_BTN = "<<"
PREV_BTN = "<"
NEXT_BTN = ">"
LAST_BTN = ">>"
PAGE_SIZE_BOX = ["10", "20", "50"]

DB_PATH = "data/database.db"