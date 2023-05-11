from datetime import timedelta

from attendance_app.models.data_access.mappers import map_record_into_student_object


def students_list_data(influx_data_list):
    students_data = dict()
    for table in influx_data_list:
        # This checks if number of attendance == odd that means that that meet is in progress, because the student never left the call
        if (len(table.records) % 2 != 0):
            continue
        student_summary = dict()
        student_summary.setdefault("attended_seg", timedelta(seconds=0))
        student_summary.setdefault("class_id_list", list())
        for result in table:
            student_data = map_record_into_student_object(result)
            value = student_data.value
            if (value == 0):
                left = student_data.date_time
            if (value == 1 and left is not None):
                join = student_data.date_time
                attended_seg = left - join
                student_summary["attended_seg"] += attended_seg
                student_summary["class_id_list"] += student_data.id_class
                left = None
        else:
            students_data.update({student_data.id_person: student_summary})
    return students_data


def get_student_data_by_id(influx_data_list):
    student_summary = dict()
    for table in influx_data_list:
        # This checks if number of attendance == odd that means that that meet is in progress, because the student never left the call
        if (len(table.records) % 2 != 0):
            continue
        attended_seg = timedelta(seconds=0)
        for result in table:
            student_data = map_record_into_student_object(result)
            value = student_data.value
            student_date = student_data.date_time
            if (value == 0):
                left = student_date
            if (value == 1 and left != None):
                join = student_date
                date = student_date.date()
                attended_seg += left - join
                left = None

        student_summary.update(
            {student_data.id_class: {'date': date, 'attended_seg': attended_seg}})
    return student_summary
