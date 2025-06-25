"""Models module"""

from datetime import date
from sqlalchemy import Date, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

Base = declarative_base()


class Group(Base):
    """Group db model"""

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    students: Mapped[list["Student"]] = relationship(back_populates="group")

    def __repr__(self) -> str:
        return f"<Group: {self.name}, ID = {self.id}>"


class Student(Base):
    """Student db model"""

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    group_id: Mapped[int] = mapped_column(Integer(), ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="students")
    student_assessments: Mapped[list["Assessment"]] = relationship(
        back_populates="student"
    )

    def __repr__(self) -> str:
        return f"<Student: {self.name}, ID = {self.id}>"


class Teacher(Base):
    """Teacher db model"""

    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    subjects: Mapped[list["Subject"]] = relationship(back_populates="teacher")

    def __repr__(self) -> str:
        return f"<Teacher: {self.name}, ID = {self.id}>"


class Subject(Base):
    """Subject db model"""

    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    teacher_id: Mapped[int] = mapped_column(Integer(), ForeignKey("teachers.id"))
    teacher: Mapped["Teacher"] = relationship(back_populates="subjects")
    subject_assessments: Mapped[list["Assessment"]] = relationship(
        back_populates="subject"
    )

    def __repr__(self) -> str:
        return f"<Subject: {self.name}, ID = {self.id}>"


class Assessment(Base):
    """Assessment db model"""

    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer(), ForeignKey("students.id"))
    subject_id: Mapped[int] = mapped_column(Integer(), ForeignKey("subjects.id"))
    assessment: Mapped[int] = mapped_column(Integer(), nullable=False)
    assessment_date: Mapped[date] = mapped_column(Date(), nullable=False)
    student: Mapped["Student"] = relationship(back_populates="student_assessments")
    subject: Mapped["Subject"] = relationship(back_populates="subject_assessments")

    def __repr__(self) -> str:
        return f"<Assessment: {self.assessment}, {self.assessment_date}>"
