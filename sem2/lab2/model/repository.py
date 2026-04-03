from model.database import Database
from model.student import Student
from model.exam import Exam


class StudentRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_student(self, student: Student):
        cursor = self.db.conn.cursor()

        cursor.execute(
            "INSERT INTO students (fio, group_name) VALUES (?, ?)",
            (student.fio, student.group)
        )

        student_id = cursor.lastrowid

        for exam in student.exams:
            cursor.execute(
                "INSERT INTO exams (student_id, subject, score) VALUES (?, ?, ?)",
                (student_id, exam.subject, exam.score)
            )

        self.db.conn.commit()

    def get_all_students(self) -> list[Student]:
        cursor = self.db.conn.cursor()

        cursor.execute("SELECT * FROM students")
        students_rows = cursor.fetchall()

        students = []

        for row in students_rows:
            student_id = row["id"]

            cursor.execute(
                "SELECT subject, score FROM exams WHERE student_id = ?",
                (student_id,)
            )
            exams_rows = cursor.fetchall()

            exams = [Exam(e["subject"], e["score"]) for e in exams_rows]

            student = Student(row["fio"], row["group_name"], exams)
            student.id = student_id

            students.append(student)

        return students
    

    def delete_by_group(self, group: str) -> int:
        cursor = self.db.conn.cursor()

        cursor.execute("SELECT id FROM students WHERE group_name = ?", (group,))
        ids = [row["id"] for row in cursor.fetchall()]

        for sid in ids:
            cursor.execute("DELETE FROM exams WHERE student_id = ?", (sid,))
            cursor.execute("DELETE FROM students WHERE id = ?", (sid,))

        self.db.conn.commit()
        return len(ids)

    def get_groups(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT DISTINCT group_name FROM students")
        return [row[0] for row in cursor.fetchall()]

    def get_subjects(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT DISTINCT subject FROM exams")
        return [row[0] for row in cursor.fetchall()]
    

    def delete_by_id(self, student_id: int):
        cursor = self.db.conn.cursor()

        cursor.execute("DELETE FROM exams WHERE student_id = ?", (student_id,))
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

        self.db.conn.commit()

    def clear_all(self):
        cursor = self.db.conn.cursor()

        cursor.execute("DELETE FROM exams")
        cursor.execute("DELETE FROM students")

        self.db.conn.commit()

    def get_by_fio(self, fio: str):
        cursor = self.db.conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE fio = ?",
            (fio,)
        )
        row = cursor.fetchone()

        if not row:
            return None

        student_id = row["id"]

        cursor.execute(
            "SELECT subject, score FROM exams WHERE student_id = ?",
            (student_id,)
        )
        exams_rows = cursor.fetchall()

        exams = [Exam(e["subject"], e["score"]) for e in exams_rows]

        student = Student(row["fio"], row["group_name"], exams)
        student.id = student_id

        return student
    
    def update_student(self, student: Student):
        cursor = self.db.conn.cursor()

        assert student.id is not None

        # обновляем группу
        cursor.execute(
            "UPDATE students SET group_name = ? WHERE id = ?",
            (student.group, student.id)
        )

        # удаляем старые экзамены
        cursor.execute(
            "DELETE FROM exams WHERE student_id = ?",
            (student.id,)
        )

        # добавляем новые
        for exam in student.exams:
            cursor.execute(
                "INSERT INTO exams (student_id, subject, score) VALUES (?, ?, ?)",
                (student.id, exam.subject, exam.score)
            )

        self.db.conn.commit()