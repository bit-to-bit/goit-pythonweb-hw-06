"""Seed module"""

import random
from datetime import datetime
from faker import Faker
from src.database.db import session
from src.database.models import Student, Group, Teacher, Subject, Assessment

NUMBER_OF_STUDENTS = 50
NUMBER_OF_TEACHERS = 4
NUMBER_OF_GROUPS = 3
MIN_NUMBER_OF_ASSESSMENT = 16
MAX_NUMBER_OF_ASSESSMENT = 20
MIN_ASSESSMENT = 1
MAX_ASSESSMENT = 5
SUBJECT_NAMES = [
    "Mathematics",
    "History",
    "English",
    "Computer Science",
    "Art",
    "Economics",
    "Music",
    "Drama",
    "Physical Education",
]
MIN_DATE = datetime(2025, 1, 1)
MAX_DATE = datetime(2025, 5, 31)


def generate_data():
    """Generate fake data for db"""

    fake = Faker()

    groups = []

    for i in range(NUMBER_OF_GROUPS):
        group = Group(name=f"Group {fake.random_letter().upper()}-{i+1}")
        groups.append(group)
        session.add(group)
    print(f"groups = {groups}")

    students = []

    for i in range(NUMBER_OF_STUDENTS):
        student = Student(name=fake.name(), group=random.choice(groups))
        students.append(student)
        session.add(student)

    teachers = []

    for i in range(NUMBER_OF_TEACHERS):
        teacher = Teacher(name=fake.name())
        teachers.append(teacher)
        session.add(teacher)

    subjects = []

    for e in SUBJECT_NAMES:
        subject = Subject(name=e, teacher=random.choice(teachers))
        subjects.append(subject)
        session.add(subject)

    for e in students:
        n = fake.random_int(min=MIN_NUMBER_OF_ASSESSMENT, max=MAX_NUMBER_OF_ASSESSMENT)
        for i in range(n):
            assessment = Assessment(
                student=e,
                subject=random.choice(subjects),
                assessment=fake.random_int(min=MIN_ASSESSMENT, max=MAX_ASSESSMENT),
                assessment_date=fake.date_between_dates(MIN_DATE, MAX_DATE),
            )
            session.add(assessment)

    session.commit()
    session.close()
