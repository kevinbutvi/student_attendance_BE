from datetime import timedelta, datetime

from attendance_app.schemas.models import LessonClass
from attendance_app.utils.summary import calc_attendance_percentage, get_total_hours, get_total_classes_duration, get_total_seconds_time_delta


def test_get_total_hours():
    HRS_EXAMPLE_1 = timedelta(hours=1, minutes=30)
    EXPECTED_1 = 1.50
    HRS_EXAMPLE_2 = timedelta(hours=2, minutes=10)
    EXPECTED_2 = 2.17
    HRS_EXAMPLE_3 = timedelta(hours=1, minutes=60)
    EXPECTED_3 = 2.00
    HRS_EXAMPLE_4 = timedelta(hours=0, minutes=15)
    EXPECTED_4 = 0.25
    assert EXPECTED_1 == get_total_hours(HRS_EXAMPLE_1)
    assert EXPECTED_2 == get_total_hours(HRS_EXAMPLE_2)
    assert EXPECTED_3 == get_total_hours(HRS_EXAMPLE_3)
    assert EXPECTED_4 == get_total_hours(HRS_EXAMPLE_4)


def test_get_total_seconds_time_delta():
    HOURS = 1
    MINUTES = 40
    SECONDS = 15

    assert timedelta(seconds=6015) == get_total_seconds_time_delta(
        HOURS, MINUTES, SECONDS)


def test_calc_attended_percentage():
    STAY_1 = timedelta(seconds=500)
    STAY_2 = timedelta(seconds=2000)
    STAY_3 = timedelta(seconds=5000)
    STAY_4 = timedelta(seconds=0)
    DURATION = timedelta(seconds=2000)

    # Stay <= Duration
    assert calc_attendance_percentage(STAY_1, DURATION) == 25
    assert calc_attendance_percentage(STAY_2, DURATION) == 100
    # Stay > Duration
    assert calc_attendance_percentage(STAY_3, DURATION) == 100
    # Stay == 0
    assert calc_attendance_percentage(STAY_4, DURATION) == 0


def test_get_total_classes_duration():
    TIME_FORMAT = "%H:%M:%S"
    DATE_FORMAT = "%Y-%m-%d"

    DATE = datetime.strptime("2023-01-13", DATE_FORMAT)
    TIME_1 = datetime.strptime("1:22:00", TIME_FORMAT)
    TIME_2 = datetime.strptime("0:11:02", TIME_FORMAT)
    TIME_3 = datetime.strptime("0:47:10", TIME_FORMAT)

    SPECTED = datetime.strptime("2:20:12", TIME_FORMAT)
    hours, minutes, seconds = SPECTED.hour, SPECTED.minute, SPECTED.second
    SPECTED_SECONDS = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    registry_1 = LessonClass(1, TIME_1, DATE)
    registry_2 = LessonClass(1, TIME_2, DATE)
    registry_3 = LessonClass(1, TIME_3, DATE)

    registries_list = [registry_1, registry_2, registry_3]
    result = get_total_classes_duration(registries_list)

    assert result == SPECTED_SECONDS
