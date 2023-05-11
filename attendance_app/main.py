import datetime

from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from attendance_app.models.data_access.utils import get_students, get_classes_data_from_student_id, get_classes_by_subject_id
from attendance_app.schemas.influx_db import StudentSummaryOutput, StudentOutput
from .models.connection.influxdb import InfluxDBConn
from .schemas.influx_db import AttendanceInputData
from .utils.create_attendance_point import create_attendance_point
from .utils.summary import get_class_summary, make_students_summary_data
from .utils.logger import logger
from .utils.students_list import students_list_data, get_student_data_by_id


app = FastAPI()
influx_conn = InfluxDBConn(token="attendance-student-token",
                           org="snake", bucket="attendance-bucket")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/attendance")
async def generate_attendace(data: AttendanceInputData | List[AttendanceInputData]):
    try:
        if (isinstance(data, list)):
            record = [create_attendance_point(
                data_entry) for data_entry in data]
        else:
            record = create_attendance_point(data)
        influx_conn.write_data(record)
        return {"status": "Sucess"}
    except Exception as e:
        logger.error(str(e), exc_info=True)
        raise HTTPException(
            status_code=500, detail='An internal server error occurred')


@app.get("/studentsList", response_model=List[StudentOutput])
async def students_list(start_date: datetime.date, end_date: datetime.date, subject_id: str):
    flux_end_date = end_date + datetime.timedelta(days=1)
    query = f"""
    from(bucket: "attendance-bucket")
        |> range(start: {start_date}, stop: {flux_end_date})
        |> filter(fn: (r) =>
            r._measurement == "student_attendance"
            and r._field == "attendance")
        |> sort(columns: ["_time"], desc: true)
        |> group(columns: ["id_person"])
    """
    try:
        # Read Influx DB
        result = influx_conn.read_query(query)
        # Get total Attendance data for each student
        total_attendance = students_list_data(result)
        # Get total Classes Data
        total_classes_data = get_classes_by_subject_id(
            subject_id, start_date, end_date)
        make_students_summary_data(total_attendance, total_classes_data)

        return [attendance for _, attendance in total_attendance.items()]
    except Exception as e:
        logger.error(str(e), exc_info=True)
        raise HTTPException(
            status_code=500, detail='An internal server error occurred')


@app.get("/student/{id}", response_model=StudentSummaryOutput)
async def students_list(id: str):
    current_year = datetime.date.today().year
    query = f"""
    from(bucket: "attendance-bucket")
        |> range(start: {current_year}-01-01T00:00:00Z, stop: {current_year}-12-31T23:59:00Z)
        |> filter(fn: (r) =>
            r._measurement == "student_attendance"
            and r._field == "attendance" and r.id_person == "{id}")
        |> sort(columns: ["_time"], desc: true)
        |> group(columns: ["id_class"])
    """
    try:
        result = influx_conn.read_query(query)
        # Gets the list of clases that the Student Attended
        total_attendance = get_student_data_by_id(result)
        # Get Student information
        student_data = get_students(id)
        # Get the duration of each class
        classes_duration = get_classes_data_from_student_id(id)
        # Get the Summary of the Student
        thirtyDaysSummary, yearSummary, summary = get_class_summary(
            total_attendance, classes_duration)
        student = {"id": student_data.id, "dni": student_data.dni, "personName": f"{student_data.last_name} {student_data.name}",
                   "thirtyDaysSummary": thirtyDaysSummary, "yearSummary": yearSummary, "summary": summary}

        return student

    except Exception as e:
        logger.error(str(e), exc_info=True)
        raise HTTPException(
            status_code=500, detail='An internal server error occurred')
