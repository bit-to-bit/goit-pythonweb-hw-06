from src.database.db import session
from src.database.models import Student, Group, Teacher, Subject, Assessment
from sqlalchemy.sql import func

DELIMITER = 42 * "-  " + 2 * "\n"


def select_1():
    """Find the 5 students with the highest average score in all subjects"""
    students = None
    try:
        with session:
            students = (
                session.query(Student, func.round(func.avg(Assessment.assessment), 3))
                .join(Assessment, Student.id == Assessment.student_id)
                .group_by(Student)
                .order_by(func.avg(Assessment.assessment).desc())
                .limit(5)
                .all()
            )
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return students


def select_2(subject: Subject):
    """Find the student with the highest GPA in a particular subject"""
    students = None
    if not subject:
        return students
    try:
        with session:
            students = (
                session.query(Student, func.round(func.avg(Assessment.assessment), 3))
                .join(Assessment, Student.id == Assessment.student_id)
                .join(Subject, Assessment.subject_id == Subject.id)
                .filter(Subject.id == subject.id)
                .group_by(Student)
                .order_by(func.avg(Assessment.assessment).desc())
                .first()
            )
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return students


def select_3(subject: Subject):
    """Find the average score in groups in a specific subject"""
    groups = None
    if not subject:
        return groups
    try:
        with session:
            groups = (
                session.query(Group, func.round(func.avg(Assessment.assessment), 3))
                .join(Student, Group.id == Student.group_id)
                .join(Assessment, Student.id == Assessment.student_id)
                .filter(Assessment.subject_id == subject.id)
                .group_by(Group)
                .order_by(func.avg(Assessment.assessment).desc())
                .all()
            )
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return groups


def select_4():
    """Find the average score on the stream (across the entire grade table)"""
    assessments = None
    try:
        with session:
            assessments = session.query(func.avg(Assessment.assessment)).first()
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return assessments


def select_5(teacher: Teacher):
    """Find which courses a particular teacher teaches"""
    subjects = None
    if not teacher:
        return subjects
    try:
        with session:
            subjects = (
                session.query(Subject).filter(Subject.teacher_id == teacher.id).all()
            )
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return subjects


def select_6(group: Group):
    """Find a list of students in a specific group"""
    students = None
    if not group:
        return students
    try:
        with session:
            students = (
                session.query(Student)
                .filter(Student.group_id == group.id)
                .order_by(Student.name)
                .all()
            )
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return students


def select_7(group: Group, subject: Subject):
    """Find the grades of students in a particular group in a specific subject"""
    assessments = None
    if not subject:
        return assessments
    if not group:
        return assessments
    try:
        with session:
            assessments = (
                session.query(Student.name, Assessment)
                .join(Assessment, Student.id == Assessment.student_id)
                .join(Subject, Assessment.subject_id == Subject.id)
                .filter(
                    Student.group_id == group.id, Assessment.subject_id == subject.id
                )
                .order_by(Student.name, Assessment.assessment.desc())
                .all()
            )
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return assessments


def select_8(teacher: Teacher):
    """Find the average score that a certain teacher gives in their subjects"""
    assessments = None
    if not teacher:
        return assessments
    try:
        with session:
            assessments = (
                session.query(Subject, func.round(func.avg(Assessment.assessment), 3))
                .join(Assessment, Subject.id == Assessment.subject_id)
                .filter(Subject.teacher_id == teacher.id)
                .group_by(Subject)
                .all()
            )
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return assessments


def select_9(student: Student):
    """Find a list of courses a specific student is taking"""
    subjects = None
    if not student:
        return subjects
    try:
        with session:
            subjects = (
                session.query(Subject)
                .distinct()
                .join(Assessment, Subject.id == Assessment.subject_id)
                .filter(Assessment.student_id == student.id)
                .all()
            )
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return subjects


def select_10(student: Student, teacher: Teacher):
    """A list of courses taught by a specific teacher to a specific student"""
    subjects = None
    if not student:
        return subjects
    try:
        with session:
            subjects = (
                session.query(Subject)
                .distinct()
                .join(Assessment, Subject.id == Assessment.subject_id)
                .filter(
                    Assessment.student_id == student.id,
                    Subject.teacher_id == teacher.id,
                )
                .all()
            )
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return subjects


def select_subject_with_min_id():
    """Select subject with min id"""
    subject = None
    try:
        with session:
            subject = session.query(Subject).order_by(Subject.id).first()
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return subject


def select_teacher_with_max_id():
    """Select teacher with min id"""
    teacher = None
    try:
        with session:
            teacher = session.query(Teacher).order_by(Teacher.id.desc()).first()
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return teacher


def select_group_with_min_id():
    """Select group with min id"""
    group = None
    try:
        with session:
            group = session.query(Group).order_by(Group.id).first()
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return group


def select_student_with_min_id():
    """Select student with min id"""
    student = None
    try:
        with session:
            student = session.query(Student).order_by(Student.id).first()
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    return student


def execute_all_selects():
    """Print result of all selects"""
    print(DELIMITER, "Select_1:")
    print("<Find the 5 students with the highest average score in all subjects>\n")
    print(*select_1(), sep="\n")

    print(DELIMITER, "Select_2:")
    print("<Find the student with the highest GPA in a particular subject>\n")
    subject = select_subject_with_min_id()
    print(f"subject = {subject}\n")
    print(select_2(subject))

    print(DELIMITER, "Select_3:")
    print("<Find the average score in groups in a specific subject>\n")
    print(f"subject = {subject}\n")
    print(*select_3(subject), sep="\n")

    print(DELIMITER, "Select_4:")
    print("<Find the average score on the stream (across the entire grade table)>\n")
    print(select_4())

    print(DELIMITER, "Select_5:")
    print("<Find which courses a particular teacher teaches>\n")
    teacher = select_teacher_with_max_id()
    print(f"teacher = {teacher}\n")
    print(*select_5(teacher), sep="\n")

    print(DELIMITER, "Select_6:")
    print("<Find a list of students in a specific group>\n")
    group = select_group_with_min_id()
    print(f"group = {group}\n")
    print(*select_6(group), sep="\n")

    print(DELIMITER, "Select_7:")
    print("<Find the grades of students in a particular group in a specific subject>\n")
    print(f"group = {group}\n")
    print(f"subject = {subject}\n")
    print(*select_7(group, subject), sep="\n")

    print(DELIMITER, "Select_8:")
    print("<Find the average score that a certain teacher gives in their subjects>\n")
    print(f"teacher = {teacher}\n")
    print(*select_8(teacher), sep="\n")

    print(DELIMITER, "Select_9:")
    print("<Find a list of courses a specific student is taking>\n")
    student = select_student_with_min_id()
    print(f"student = {student}\n")
    print(*select_9(student), sep="\n")

    print(DELIMITER, "Select_10:")
    print("<A list of courses taught by a specific teacher to a specific student>\n")
    print(f"student = {student}\n")
    print(f"teacher = {teacher}\n")
    print(*select_10(student, teacher), sep="\n")
