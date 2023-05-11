from influxdb_client.client.flux_table import FluxRecord

from attendance_app.models.data_access.models import Students, Classes
from ...schemas.models import LessonClass, Student, StudentData


def map_modelClass_into_class(my_class: Classes):
    leasson = LessonClass(my_class.id, my_class.duration, my_class.date)
    return leasson


def map_modelStudent_into_student(student: Students):
    student = Student(student.id, student.dni, student.name, student.lastName)
    return student


def map_record_into_student_object(record: FluxRecord) -> StudentData:
    """
    Map a Influx Record into a StudentData Obj
    """
    date_time = record["_time"]
    value = record["_value"]
    id_class = record["id_class"]
    id_person = record["id_person"]

    # Create a StudentData object and return it
    return StudentData(date_time, value, id_class, id_person)
