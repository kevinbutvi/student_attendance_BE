from sqlalchemy import select, join, and_
from datetime import datetime

from attendance_app.models.connection.my_sql import with_session
from .models import Students, Classes, Student_Subject
from attendance_app.models.data_access.mappers import map_modelClass_into_class, map_modelStudent_into_student


@with_session
def get_students(session, id: int = None):
    stmt = select(Students.id, Students.name, Students.lastName,
                  Students.dni)
    if (id is None):
        student_list = session.execute(stmt).all()
        return [map_modelStudent_into_student(student) for student in student_list]
    student = session.execute(stmt.where(Students.id == id)).first()
    return map_modelStudent_into_student(student)


@with_session
def get_classes_data_from_student_id(session, student_id, start_date, end_date):
    stmt = select(Classes.id, Classes.duration, Classes.date).where(
        and_(Student_Subject.studentId == student_id,
             Classes.date.between(start_date, end_date))).select_from(join(Students, Student_Subject, Students.id == Student_Subject.studentId))
    response = session.execute(stmt).all()

    if len(response) == 0:
        return None
    return [map_modelClass_into_class(item) for item in response]


@with_session
def get_duration_by_class(session, classes_list):
    classes_id_list = [my_class.id for my_class in classes_list]
    stmt = select(Classes.id, Classes.duration, Classes.date).filter(
        Classes.id.in_(classes_id_list))
    response = session.execute(stmt).all()
    return [map_modelClass_into_class(lesson) for lesson in response]


@with_session
def get_classes_by_subject_id(session, subject_id: int, start_date: datetime, end_date: datetime):
    stmt = select(Classes.id, Classes.duration, Classes.date).where(
        Classes.subjectId == subject_id, Classes.date.between(start_date, end_date))
    response = session.execute(stmt).all()
    return [map_modelClass_into_class(item) for item in response]
