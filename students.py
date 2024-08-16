from flask import abort, make_response

from config import db
from models import Student, students_schema, student_schema
from datetime import datetime

def read_all():
    students = Student.query.all()
    return students_schema.dump(students)

def create(student):
    regNo = student.get("regNo")
    existing_student = Student.query.filter(Student.regNo == regNo).one_or_none()

    if existing_student is None:
        new_student = student_schema.load(student, session=db.session)
        new_student.DOE = datetime.strptime(new_student.DOE, "%Y-%m-%d").date()  # Convert DOE to date object
        db.session.add(new_student)
        db.session.commit()
        return student_schema.dump(new_student), 201
    else:
        abort(
            406,
            f"Student with registration number {regNo} already exists",
        )

def read_one(regNo):
    student = Student.query.filter(Student.regNo == regNo).one_or_none()

    if student is not None:
        return student_schema.dump(student)
    else:
        abort(
            404, f"Student with registration number {regNo} not found"
        )

def update(regNo, student):
    existing_student = Student.query.filter(Student.regNo == regNo).one_or_none()

    if existing_student:
        update_student = student_schema.load(student, session=db.session)
        existing_student.fname = update_student.fname
        existing_student.lname = update_student.lname
        existing_student.DOE = datetime.strptime(update_student.DOE, "%Y-%m-%d").date()  # Convert DOE to datetime
        existing_student.st_email = update_student.st_email
        existing_student.phoneNo = update_student.phoneNo
        existing_student.level = update_student.level
        existing_student.department = update_student.department
        existing_student.program = update_student.program
        existing_student.company = update_student.company
        existing_student.com_city = update_student.com_city
        existing_student.com_email = update_student.com_email
        existing_student.com_phone = update_student.com_phone
        db.session.merge(existing_student)
        db.session.commit()
        return student_schema.dump(existing_student), 201
    else:
        abort(
            404,
            f"Student with registration number {regNo} not found"
        )
def delete(regNo):
    existing_student = Student.query.filter(Student.regNo == regNo).one_or_none()

    if existing_student:
        db.session.delete(existing_student)
        db.session.commit()
        return make_response(f"{regNo} successfully deleted", 200)
    else:
        abort(
            404,
            f"Person with last name {regNo} not found"
        )