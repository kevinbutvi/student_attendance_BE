from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

from attendance_app.models.data_access.utils import get_students, get_duration_by_class


def get_total_classes_duration(class_duration_list):
    total_duration = timedelta(seconds=0)
    for class_duration in class_duration_list:
        hours, minutes, seconds = class_duration.duration.hour, class_duration.duration.minute, class_duration.duration.second
        duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        total_duration += duration
    return total_duration


def calc_attendance_percentage(stay_time, duration):
    if stay_time == 0:
        return 0
    if stay_time >= duration:
        return 100
    return int(stay_time * 100 / duration)


def get_class_summary(total_attendance, classes_duration):
    today = date.today()
    thirty_days_ago = today - relativedelta(months=1)
    one_year_ago = today - relativedelta(years=1)
    thirtyDaysSummary, yearSummary = dict(), dict()
    summary = list()
    total_classes_duration, total_attended_seconds = timedelta(
        seconds=0), timedelta(seconds=0)
    total_passes = 0
    total_classes = len(classes_duration)

    for class_data in classes_duration:
        class_duration = class_data.duration
        total_seconds = class_duration.hour * 3600 + \
            class_duration.minute * 60 + class_duration.second
        class_duration = timedelta(seconds=total_seconds)
        student_attended_class_data = total_attendance.get(str(class_data.id))
        if student_attended_class_data:
            attended = student_attended_class_data.get("attended_seg")
        else:
            attended = timedelta(seconds=0)
        attended_percentage = calc_attendance_percentage(
            attended, class_duration)
        if (attended_percentage >= 80):
            total_passes += 1

        total_attended_seconds += attended
        total_classes_duration += class_duration

        if (class_data.date >= thirty_days_ago):
            thirtyDaysSummary["totalHours"] = "{:.1f}".format(
                total_classes_duration.total_seconds() / 3600)
            thirtyDaysSummary["attendedHours"] = "{:.1f}".format(
                total_attended_seconds.total_seconds() / 3600)
            thirtyDaysSummary["totalClasses"] = total_classes
            thirtyDaysSummary["attendedClasses"] = total_passes
        if (class_data.date >= one_year_ago):
            yearSummary["totalHours"] = "{:.1f}".format(
                total_classes_duration.total_seconds() / 3600)
            yearSummary["attendedHours"] = "{:.1f}".format(
                total_attended_seconds.total_seconds() / 3600)
            yearSummary["totalClasses"] = total_classes
            yearSummary["attendedClasses"] = total_passes

        summary_day = {
            "day": class_data.date, "value": attended_percentage}
        summary.append(summary_day)
    return thirtyDaysSummary, yearSummary, summary


def make_students_summary_data(total_attendance, total_classes):
    students_list = get_students()
    classes_duration_list = get_duration_by_class(total_classes)
    classes_duration_summary = get_total_classes_duration(
        classes_duration_list)
    for student in students_list:
        student_id_key = str(student.id)
        student_full_name = f"{student.last_name} {student.name}"
        # Check if student attended each class
        student_exists_in_class = total_attendance.get(student_id_key)
        if not student_exists_in_class:
            attended_percentage = 0
            total_attendance.setdefault(
                student_id_key, {"attendancePercentage": attended_percentage})
        else:
            attended_percentage = calc_attendance_percentage(
                total_attendance[student_id_key].get("attended_seg"), classes_duration_summary)
            total_attendance[student_id_key].pop("attended_seg")

        total_attendance[student_id_key].update(
            {
                "id": student_id_key,
                "dni": student.dni,
                "personName": student_full_name,
                "attendancePercentage": attended_percentage,
                "status": 1 if attended_percentage >= 80 else 0
            })
