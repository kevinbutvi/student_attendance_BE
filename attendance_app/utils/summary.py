from datetime import timedelta


def get_total_hours(time: timedelta) -> float:
    return round((time.total_seconds() / 3600), 2)


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
    return round((stay_time * 100 / duration), 0)


def get_total_seconds_time_delta(hours, minutes, seconds):
    total_seconds = hours * 3600 + \
        minutes * 60 + seconds
    return timedelta(seconds=total_seconds)


def get_class_summary(total_attendance, classes_duration):
    total_classes_count = 0
    total_summary = dict()
    summary = list()
    total_classes_duration, total_attended_seconds = timedelta(
        seconds=0), timedelta(seconds=0)
    total_passes = 0
    total_summary["totalHours"], total_summary["attendedHoursPercentage"], total_summary[
        "totalClasses"], total_summary["attendedClasses"], total_summary["attendedHours"] = 0, 0, 0, 0, 0

    if (classes_duration is None):
        return total_summary, None

    total_classes = len(classes_duration)
    for class_data in classes_duration:
        class_duration = class_data.duration
        class_duration = get_total_seconds_time_delta(
            class_duration.hour, class_duration.minute, class_duration.second)
        student_attended_class_data = total_attendance.get(str(class_data.id))
        if student_attended_class_data:
            attended = student_attended_class_data.get("attended_seg")
        else:
            attended = timedelta(seconds=0)
        attended_percentage = calc_attendance_percentage(
            attended, class_duration)
        if (attended_percentage >= 80):
            total_passes += 1
        if (attended < class_duration):
            total_attended_seconds += attended
        else:
            total_attended_seconds += class_duration

        total_classes_duration += class_duration

        total_classes_count += 1
        total_summary["totalHours"] = get_total_hours(total_classes_duration)
        total_summary["attendedHours"] = get_total_hours(
            total_attended_seconds)
        total_summary["attendedHoursPercentage"] += attended_percentage

        total_summary["totalClasses"] = total_classes
        total_summary["attendedClasses"] = total_passes
        total_summary["totalClassesPercentage"] = (
            total_passes * 100) / total_classes

        summary_day = {
            "day": class_data.date, "value": attended_percentage}
        summary.append(summary_day)
    else:
        total_summary["attendedHoursPercentage"] = round(
            (total_summary["attendedHoursPercentage"] / total_classes), 2)
    return total_summary, summary


def make_students_summary_data(total_attendance, students_list, classes_duration_list):
    classes_duration_summary = get_total_classes_duration(
        classes_duration_list)
    for student in students_list:
        student_id_key = str(student.id)
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
                "personName": f"{student.last_name} {student.name}",
                "attendancePercentage": attended_percentage,
                "status": 1 if attended_percentage >= 80 else 0
            })
