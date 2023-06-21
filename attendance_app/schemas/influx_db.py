from datetime import datetime
from pydantic import BaseModel, validator
from typing import List, Dict


def verify_if_is_one_or_zero(value):
    if (value == 1 or value == 0):
        return True
    return False


class AttendanceInputData(BaseModel):
    status: int
    id_person: int
    id_class: int
    datetime: datetime

    @validator("status")
    def status_must_be_1_or_0(cls, v):
        if verify_if_is_one_or_zero(v):
            return v
        raise ValueError(
            "The status Value mas be '1' for 'JOIN' or '0' for 'LEFT'")


class BasePerson(BaseModel):
    id: int
    dni: int
    personName: str


class StudentOutput(BasePerson):
    attendancePercentage: float
    status: int


class StudentSummaryOutput(BasePerson):
    totalSummary: Dict
    summary: List | None
