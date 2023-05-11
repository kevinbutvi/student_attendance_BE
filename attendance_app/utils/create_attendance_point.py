from influxdb_client import Point


def create_attendance_point(data):
    record = (
        Point("student_attendance")
        .tag("id_person", data.id_person)
        .tag("id_class", data.id_class)
        .field("attendance", data.status)
        .time(data.datetime)
    )
    return record
