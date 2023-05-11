from sqlalchemy import Column, String, Time, BigInteger, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Students(Base):
    __tablename__ = "Students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))
    lastName = Column(String(45))
    dni = Column(BigInteger)
    studentSubject = relationship(
        "Student_Subject", back_populates="student", cascade="all")


class Subjects(Base):
    __tablename__ = "Subjects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))
    myClass = relationship("Classes", back_populates="subject", cascade="all")
    studentSubject = relationship(
        "Student_Subject", back_populates="subject", cascade="all")


class Classes(Base):
    __tablename__ = "Classes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    duration = Column(Time)
    date = Column(Date)
    subjectId = Column(ForeignKey("Subjects.id"))
    subject = relationship("Subjects", back_populates="myClass", cascade="all")


class Student_Subject(Base):
    __tablename__ = "Student_Subject"
    studentId = Column(Integer, ForeignKey("Students.id"), primary_key=True)
    subjectId = Column(Integer, ForeignKey("Subjects.id"), primary_key=True)
    student = relationship(
        "Students", back_populates="studentSubject", cascade="all")
    subject = relationship(
        "Subjects", back_populates="studentSubject", cascade="all")
