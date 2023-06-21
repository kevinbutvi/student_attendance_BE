from datetime import datetime


class StudentData():
    def __init__(self, date_time: datetime, value: str, id_class: int, id_person: int):
        self.date_time = date_time
        self.value = value
        self.id_class = id_class
        self.id_person = id_person


class LessonClass():
    def __init__(self, id: int, duration: datetime.time, date: datetime.date):
        self.id = id
        self.duration = duration
        self.date = date


class Student():
    def __init__(self, id: int, dni: int, name: str, lastName: str):
        self.id = id
        self.dni = dni
        self.name = name
        self.last_name = lastName
