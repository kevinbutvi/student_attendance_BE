from datetime import datetime

from attendance_app.schemas.models import LessonClass, Student, StudentData

TIME_FORMAT = "%H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

DATE = datetime.strptime("2023-01-13", DATE_FORMAT)
TIME = datetime.strptime("1:22:00", TIME_FORMAT)
DATETIME = datetime.strptime("2023-01-13 14:22:00", DATE_TIME_FORMAT)


def test_create_Student():
    lesson = LessonClass(1, TIME, DATE)
    assert lesson.id == 1
    assert lesson.duration == TIME
    assert lesson.date == DATE


def test_create_student():
    student = Student(1, 112233, "Juan", "Perez")
    assert student.id == 1
    assert student.dni == 112233
    assert student.name == "Juan"
    assert student.last_name == "Perez"


def test_create_StudentData():
    student_data = StudentData(DATETIME, 1, 1, 1)
    assert student_data.date_time == DATETIME
    assert student_data.value == 1
    assert student_data.id_class == 1
    assert student_data.id_person == 1
