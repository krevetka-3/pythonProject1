from peewee import Model, SqliteDatabase, ForeignKeyField, CharField, IntegerField, DateField

# Подключение к базе данных
db = SqliteDatabase('students_courses.db')

# Создание моделей для таблиц
class BaseModel(Model):
    class Meta:
        database = db

class Students(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    surname = CharField()
    age = IntegerField()
    city = CharField()

class Courses(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    time_start = DateField()
    time_end = DateField()

class Student_courses(BaseModel):
    student_id = ForeignKeyField(Students, backref='student_courses')
    course_id = ForeignKeyField(Courses, backref='student_courses')

# Связь моделей с базой данных
db.connect()
db.create_tables([Students, Courses, Student_courses])

# Добавление объектов
courses_data = [
    (1, 'python', '2021-07-21', '2021-08-21'),
    (2, 'java', '2021-07-13', '2021-08-16')
]

students_data = [
    (1, 'Max', 'Brooks', 24, 'Spb'),
    (2, 'John', 'Stones', 15, 'Spb'),
    (3, 'Andy', 'Wings', 45, 'Manchester'),
    (4, 'Kate', 'Brooks', 34, 'Spb')
]

student_courses_data = [
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 2)
]

Courses.insert_many(courses_data).execute()
Students.insert_many(students_data).execute()
Student_courses.insert_many(student_courses_data).execute()

# Запросы
# 1. Все студенты старше 30 лет
students_over_30 = Students.select().where(Students.age > 30)
for student in students_over_30:
    print(student.name, student.surname)

# 2. Все студенты, которые проходят курс по python
students_python_course = (Students
                          .select()
                          .join(Student_courses)
                          .join(Courses)
                          .where(Courses.name == 'python'))
for student in students_python_course:
    print(student.name, student.surname)

# 3. Все студенты, которые проходят курс по python и из Spb
students_python_spb = (Students
                      .select()
                      .join(Student_courses)
                      .join(Courses)
                      .where((Courses.name == 'python') & (Students.city == 'Spb')))
for student in students_python_spb:
    print(student.name, student.surname)
