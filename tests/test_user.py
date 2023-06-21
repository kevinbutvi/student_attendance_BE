import pydantic
import pytest
from datetime import datetime
from attendance_app.schemas.influx_db import AttendanceInputData

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
WRONG_STATUS = 99
STATUS = 1
DATE = "2023-01-13 14:22:00"
WRONG_DATE = "2023/05/12 12:41:44"
ID_PERSON, ID_CLASS = 1, 2


def test_student_input():
    student = AttendanceInputData(status=STATUS, id_person=ID_PERSON,
                                  id_class=ID_CLASS, datetime=DATE)
    assert isinstance(student, AttendanceInputData)
    assert (student.status == STATUS)
    assert (student.id_person == ID_PERSON)
    assert (student.id_class == ID_CLASS)
    assert (student.datetime == datetime.strptime(DATE, DATE_FORMAT))


def test_status():
    # Attempt to create an instance of the Student with an invalid Status

    with pytest.raises(pydantic.ValidationError):
        AttendanceInputData(status=WRONG_STATUS, id_person=ID_PERSON,
                            id_class=ID_CLASS, datetime=DATE)


def test_date():
    # Attempt to create an instance of the Student with an invalid DATE

    with pytest.raises(pydantic.ValidationError):
        AttendanceInputData(status=STATUS, id_person=ID_PERSON,
                            id_class=ID_CLASS, datetime=WRONG_DATE)
