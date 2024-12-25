from peewee import *
import os


db = SqliteDatabase("university.db")

class BaseModel(Model):
    class Meta:
        database = db

class Student(BaseModel):
    id = AutoField()
    name = CharField()
    surname = CharField()
    age = IntegerField()
    city = CharField()

class Course(BaseModel):
    id = AutoField()
    name = CharField()
    time_start = DateField()
    time_end = DateField()

class StudentCourse(BaseModel):
    student = ForeignKeyField(Student, backref='courses')
    course = ForeignKeyField(Course, backref='students')

class UniversityDatabase:
    def __init__(self):
        if not os.path.exists("university.db"):
            self._initialize_database()

    def _initialize_database(self):
        db.connect()
        db.create_tables([Student, Course, StudentCourse])

        # Заполняем данные, если таблицы пустые
        if not Course.select().exists():
            Course.create(id=1, name='python', time_start='2021-07-21', time_end='2021-08-21')
            Course.create(id=2, name='java', time_start='2021-07-13', time_end='2021-08-16')

        if not Student.select().exists():
            Student.create(id=1, name='Max', surname='Brooks', age=24, city='Spb')
            Student.create(id=2, name='John', surname='Stones', age=15, city='Spb')
            Student.create(id=3, name='Andy', surname='Wings', age=45, city='Manhester')
            Student.create(id=4, name='Kate', surname='Brooks', age=34, city='Spb')

        if not StudentCourse.select().exists():
            StudentCourse.create(student=1, course=1)
            StudentCourse.create(student=2, course=1)
            StudentCourse.create(student=3, course=1)
            StudentCourse.create(student=4, course=2)

    def execute_query(self, query_function):
        db.connect()
        result = query_function()
        db.close()
        return result

    def get_students_over_30(self):
        return self.execute_query(lambda: list(Student.select().where(Student.age > 30)))

    def get_students_in_python(self):
        return self.execute_query(lambda: list(
            Student.select().join(StudentCourse).join(Course).where(Course.name == 'python')
        ))

    def get_students_in_python_from_spb(self):
        return self.execute_query(lambda: list(
            Student.select().join(StudentCourse).join(Course).where(
                (Course.name == 'python') & (Student.city == 'Spb')
            )
        ))


if __name__ == "__main__":
    db_instance = UniversityDatabase()

    print("Студенты старше 30 лет:", [student.name for student in db_instance.get_students_over_30()])
    print("Студенты, проходящие курс по python:", [student.name for student in db_instance.get_students_in_python()])
    print("Студенты, проходящие курс по python и из Spb:", [student.name for student in db_instance.get_students_in_python_from_spb()])
